########################################################################
#
# File Name:            StylesheetReader.py
#
#

"""
Create a stylesheet object
WWW: http://4suite.org/4XSLT        e-mail: support@4suite.org

Copyright (c) 1999-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""

import string, os, urllib, cStringIO
try:
    from Ft.Lib.ReaderBase import DomletteReader
    _ReaderBase = DomletteReader
except ImportError:
    from minisupport import MinidomReader
    _ReaderBase = MinidomReader

#FIXME: we might want to do some meta-magic to __import__ element modules on demand
from xml.xslt.ApplyTemplatesElement import ApplyTemplatesElement
from xml.xslt.AttributeElement import AttributeElement
from xml.xslt.AttributeSetElement import AttributeSetElement
from xml.xslt.CallTemplateElement import CallTemplateElement
from xml.xslt.ChooseElement import ChooseElement
from xml.xslt.CopyElement import CopyElement
from xml.xslt.CopyOfElement import CopyOfElement
from xml.xslt.CommentElement import CommentElement
from xml.xslt.ElementElement import ElementElement
from xml.xslt.ForEachElement import ForEachElement
from xml.xslt.IfElement import IfElement
from xml.xslt.LiteralElement import LiteralElement
from xml.xslt.LiteralText import LiteralText
from xml.xslt.MessageElement import MessageElement
from xml.xslt.NumberElement import NumberElement
from xml.xslt.OtherwiseElement import OtherwiseElement
from xml.xslt.ParamElement import ParamElement
from xml.xslt.ProcessingInstructionElement import ProcessingInstructionElement
from xml.xslt.SortElement import SortElement
from xml.xslt.TemplateElement import TemplateElement
from xml.xslt.TextElement import TextElement
from xml.xslt.VariableElement import VariableElement
from xml.xslt.ValueOfElement import ValueOfElement
from xml.xslt.WhenElement import WhenElement
from xml.xslt.WithParamElement import WithParamElement

from xml.xslt.OtherXslElement import ImportElement, IncludeElement, DecimalFormatElement, KeyElement, NamespaceAliasElement, OutputElement, PreserveSpaceElement, StripSpaceElement, FallbackElement

from xml.xslt.Stylesheet import StylesheetElement
from xml.xslt import XSL_NAMESPACE, XsltElement
from xml.xslt import XsltException, Error, ReleaseNode, RegisterExtensionModules

from xml import xslt

from xml.dom import Node
from xml.dom.ext import StripXml, GetAllNs, SplitQName
from xml.dom import implementation, ext, XML_NAMESPACE, XMLNS_NAMESPACE, EMPTY_NAMESPACE

try:
    from Ft.Lib import FtException
    import Ft.Lib
    XML_PARSE_ERROR = Ft.Lib.Error.XML_PARSE_ERROR
except ImportError:
    XML_PARSE_ERROR = "XML_PARSE_ERROR"
    # XXX need better definition
    class FtException(Exception):
        pass

import cPickle

try:
    from Ft.Lib import pDomlette
    createDocument = pDomlette.Document
    def CreateInstantStylesheet(sheet):
        return pDomlette.PickleDocument(sheet.ownerDocument)

    def FromInstant(dump, forceBaseUri=None):
        return UnpickleDocument(dump, forceBaseUri).documentElement

except ImportError:
    from xml.dom import minitraversal
    import pickle
    createDocument = minitraversal.Document
    def CreateInstantStylesheet(sheet):
        return pickle.dumps(sheet, 1)
    def FromInstant(dump, forceBaseUri=None):
        assert not forceBaseUri
        return pickle.loads(dump)


g_mappings = {XSL_NAMESPACE: {
    'apply-templates': ApplyTemplatesElement
    , 'attribute': AttributeElement
    , 'attribute-set': AttributeSetElement
    , 'call-template': CallTemplateElement
    , 'choose': ChooseElement
    , 'copy': CopyElement
    , 'copy-of': CopyOfElement
    , 'comment': CommentElement
    , 'element': ElementElement
    , 'for-each': ForEachElement
    , 'if': IfElement
    , 'message': MessageElement
    , 'number': NumberElement
    , 'otherwise': OtherwiseElement
    , 'param': ParamElement
    , 'processing-instruction': ProcessingInstructionElement
    , 'sort': SortElement
    , 'stylesheet': StylesheetElement
    , 'transform': StylesheetElement
    , 'template': TemplateElement
    , 'text': TextElement
    , 'variable': VariableElement
    , 'value-of': ValueOfElement
    , 'when': WhenElement
    , 'fallback': FallbackElement
    , 'with-param': WithParamElement
    , 'import': ImportElement
    , 'include': IncludeElement
    , 'key': KeyElement
    , 'namespace-alias': NamespaceAliasElement
    , 'output': OutputElement
    , 'preserve-space': PreserveSpaceElement
    , 'strip-space': StripSpaceElement
    }}



def FromDocument(oldDoc, baseUri='',stylesheetReader = None):
    #FIXME: We really shouldn't mutate the given doc, but this is the easiest way to strip whitespace
    if baseUri and baseUri[-1] == '/':
        modBaseUri = baseUri
    else:
        modBaseUri = baseUri + '/'
    oldDoc.normalize()
    extElements = xslt.g_extElements
    source_root = oldDoc.documentElement
    #Set up a new document for the stylesheet nodes
    if source_root.namespaceURI == XSL_NAMESPACE:
        if source_root.localName not in ['stylesheet', 'transform']:
            raise XsltException(Error.STYLESHEET_ILLEGAL_ROOT, source_root.nodeName)
        result_elem_root = 0
    else:
        result_elem_root = 1
    xsl_doc = createDocument()
    ext_uris = []
    if result_elem_root:
        vattr = source_root.getAttributeNodeNS(XSL_NAMESPACE, 'version')
        if not vattr:
            root_nss = GetAllNs(source_root)
            if filter(lambda x, n=root_nss: n[x] == XSL_NAMESPACE, root_nss.keys()):
                raise XsltException(Error.STYLESHEET_MISSING_VERSION)
            else:
                raise XsltException(Error.STYLESHEET_MISSING_VERSION_NOTE1)

        sheet = StylesheetElement(xsl_doc, XSL_NAMESPACE,
                                  'transform', vattr.prefix,
                                  baseUri)
        sheet.setAttributeNS(EMPTY_NAMESPACE, 'version', vattr.value)
        tpl = TemplateElement(xsl_doc, XSL_NAMESPACE, 'template',
                              vattr.prefix, baseUri)

        tpl.setAttributeNS(EMPTY_NAMESPACE, 'match', '/')
        sheet.appendChild(tpl)
        sheet.__dict__['extensionNss'] = []
        xsl_doc.appendChild(sheet)
        DomConvert(source_root, tpl, xsl_doc, [], extElements, 0)
    else:
        sheet = StylesheetElement(xsl_doc, source_root.prefix, source_root.localName, baseUri=baseUri)
        sty_nss = GetAllNs(source_root)
        for attr in source_root.attributes.values():
            if (attr.namespaceURI, attr.localName) == ('', 'extension-element-prefixes'):
                ext_prefixes = string.splitfields(attr.value)
                for prefix in ext_prefixes:
                    if prefix == '#default': prefix = ''
                    ext_uris.append(sty_nss[prefix])
            sheet.setAttributeNS(attr.namespaceURI, attr.nodeName, attr.value)
        sheet.__dict__['extensionNss'] = ext_uris
        if not sheet.getAttributeNS(EMPTY_NAMESPACE, 'version'):
            raise XsltException(Error.STYLESHEET_MISSING_VERSION)
        xsl_doc.appendChild(sheet)
        for child in source_root.childNodes:
            DomConvert(child, sheet, xsl_doc, ext_uris, extElements, 0)
    #Handle includes
    includes = filter(lambda x: x.nodeType == Node.ELEMENT_NODE and (x.namespaceURI, x.localName) == (XSL_NAMESPACE, 'include'), sheet.childNodes)
    for inc in includes:
        href = inc.getAttributeNS(EMPTY_NAMESPACE,'href')
        if stylesheetReader is None:
            stylesheetReader = StylesheetReader()
        docfrag = stylesheetReader.fromUri(href,baseUri = baseUri, ownerDoc=xsl_doc)
        sty = docfrag.firstChild
        included_nss = GetAllNs(sty)
        for child in sty.childNodes[:]:
            if child.nodeType != Node.ELEMENT_NODE:
                continue
            sheet.insertBefore(child, inc)
            #migrate old nss from stylesheet directly to new child
            for prefix in included_nss.keys():
                if prefix:
                    child.setAttributeNS(XMLNS_NAMESPACE, 'xmlns:'+prefix,
                                                 included_nss[prefix])
                else:
                    child.setAttributeNS(XMLNS_NAMESPACE, 'xmlns',
                                         included_nss[prefix])

        sheet.removeChild(inc)
        ReleaseNode(inc)
        #sty.reclaim()
    try:
        sheet.setup()
    except:
        ReleaseNode(sheet.ownerDocument)
        raise
    return sheet


def DomConvert(node, xslParent, xslDoc, extUris, extElements, preserveSpace):
    if node.nodeType == Node.ELEMENT_NODE:
        mapping = g_mappings.get(node.namespaceURI, None)
        if mapping:
            if not mapping.has_key(node.localName):
                raise XsltException(Error.XSLT_ILLEGAL_ELEMENT, node.localName)
            xsl_class = mapping[node.localName]

            xsl_instance = xsl_class(xslDoc, baseUri=xslParent.baseUri)
            for attr in node.attributes.values():
                if not attr.namespaceURI and attr.localName not in xsl_instance.__class__.legalAttrs:
                    raise XsltException(Error.XSLT_ILLEGAL_ATTR,
                                        attr.nodeName, xsl_instance.nodeName)
                xsl_instance.setAttributeNS(attr.namespaceURI, attr.nodeName,
                                            attr.value)
            xslParent.appendChild(xsl_instance)
        elif node.namespaceURI in extUris:
            name = (node.namespaceURI, node.localName)
            if name in extElements.keys():
                ext_class = extElements[name]
            else:
                #Default XsltElement behavior effects fallback
                ext_class = XsltElement
            xsl_instance = ext_class(xslDoc, node.namespaceURI,
                                     node.localName, node.prefix,
                                     xslParent.baseUri)
            for attr in node.attributes.values():
                if (attr.namespaceURI, attr.localName) == (XSL_NAMESPACE, 'extension-element-prefixes'):
                    ext_prefixes = string.splitfields(attr.value)
                    for prefix in ext_prefixes:
                        if prefix == '#default': prefix = ''
                        extUris.append(node_nss[prefix])
                xsl_instance.setAttributeNS(attr.namespaceURI, attr.nodeName,
                                            attr.value)
            xslParent.appendChild(xsl_instance)
        else:
            xsl_instance = LiteralElement(xslDoc, node.namespaceURI,
                                          node.localName, node.prefix,
                                          xslParent.baseUri)
            node_nss = GetAllNs(node)
            for attr in node.attributes.values():
                if (attr.namespaceURI, attr.localName) == (XSL_NAMESPACE, 'extension-element-prefixes'):
                    ext_prefixes = string.splitfields(attr.value)
                    for prefix in ext_prefixes:
                        if prefix == '#default': prefix = ''
                        extUris.append(node_nss[prefix])
                xsl_instance.setAttributeNS(attr.namespaceURI,
                                            attr.nodeName,
                                            attr.value
                                            )
            xslParent.appendChild(xsl_instance)
        ps = (xsl_instance.namespaceURI, xsl_instance.localName) == (XSL_NAMESPACE, 'text') or xsl_instance.getAttributeNS(XML_NAMESPACE,'space') == 'preserve'
        #ps = (xsl_instance.namespaceURI, xsl_instance.localName) == (XSL_NAMESPACE, 'text')
        for child in node.childNodes:
            DomConvert(child, xsl_instance, xslDoc, extUris, extElements, ps)
    elif node.nodeType == Node.TEXT_NODE:
        if string.strip(node.data) or preserveSpace:
            xsl_instance = LiteralText(xslDoc, node.data)
            xslParent.appendChild(xsl_instance)
    return



### Domlette Parser Interface ###

from xml.parsers import expat

class StylesheetReader(_ReaderBase):
    def __init__(self, force8Bit=0):
        _ReaderBase.__init__(self)
        self.force8Bit = force8Bit
        self._ssheetUri = ''
        return

    def fromUri(self, uri, baseUri='', ownerDoc=None, stripElements=None):
        self._ssheetUri = urllib.basejoin(baseUri, uri)
        result = _ReaderBase.fromUri(self, uri, baseUri,
                                     ownerDoc, stripElements)
        return result

    def fromStream(self, stream, baseUri='', ownerDoc=None,
                   stripElements=None):
        if not xslt.g_registered:
            xslt.Register()
        self.initParser()
        self.initState(ownerDoc, baseUri)
        p = self.parser
        try:
            success = self.parser.ParseFile(stream)
        except XsltException:
            raise
        except Exception, e:
            for s in self._nodeStack:
                self.releaseNode(s)
            if p.ErrorCode:
                raise FtException(XML_PARSE_ERROR,
                                  p.ErrorLineNumber,
                                  p.ErrorColumnNumber,
                                  expat.ErrorString(p.ErrorCode))
            else:
                raise
        self._ssheetUri = ''
        self.killParser()
        if not success:
            self.releaseNode(self._rootNode)
            self.releaseNode(self._ownerDoc)
            raise XsltException(Error.STYLESHEET_PARSE_ERROR, baseUri, p.ErrorLineNumber, p.ErrorColumnNumber, expat.ErrorString(p.ErrorCode))
        self._completeTextNode()

        root = self._rootNode or self._ownerDoc
        if root.nodeType == Node.DOCUMENT_NODE:
            sheet = root.documentElement
            try:
                sheet.setup()
            except:
                sheet.reclaim()
                self.releaseNode(root)
                raise
        else:
            sheet = None
        rt = sheet or root
        return rt

    def initParser(self):
        if self.force8Bit:
            self.handler = Utf8OnlyHandler(self)
        else:
            self.handler = self
        self.parser=expat.ParserCreate()
        self.parser.StartElementHandler = self.handler.startElement
        self.parser.EndElementHandler = self.handler.endElement
        self.parser.CharacterDataHandler = self.handler.characters
        self.parser.ProcessingInstructionHandler = self.handler.processingInstruction
        self.parser.CommentHandler = self.handler.comment
        self.parser.ExternalEntityRefHandler = self.handler.entityRef
        return

    def initState(self, ownerDoc, refUri):
        pDomlette.Handler.initState(self, ownerDoc)
        self._preserveStateStack = [0]
        self._extUris = []
        self._extUriStack = []
        self._firstElement = 1
        if not self._ssheetUri:
            self._ssheetUri = refUri
        return

    def _completeTextNode(self):
        #Note some parsers don't report ignorable white space properly
        if self._currText and len(self._nodeStack) and self._nodeStack[-1].nodeType != Node.DOCUMENT_NODE:
            if self._preserveStateStack[-1] or string.strip(self._currText):
                new_text = LiteralText(self._ownerDoc, self._currText)
                self._nodeStack[-1].appendChild(new_text)
        self._currText = ''
        return

    def _initializeSheet(self, rootNode):
        if rootNode.namespaceURI == XSL_NAMESPACE:
            if rootNode.localName in ['stylesheet', 'transform']:
                if not rootNode.getAttributeNS(EMPTY_NAMESPACE, 'version'):
                    raise XsltException(Error.STYLESHEET_MISSING_VERSION)
                #rootNode.__dict__['extensionNss'] = []
            else:
                raise XsltException(Error.STYLESHEET_ILLEGAL_ROOT, rootNode.nodeName)
        else:
            vattr = rootNode.getAttributeNodeNS(XSL_NAMESPACE, 'version')
            if not vattr:
                root_nss = GetAllNs(rootNode)
                if filter(lambda x, n=root_nss: n[x] == XSL_NAMESPACE, root_nss.keys()):
                    raise XsltException(Error.STYLESHEET_MISSING_VERSION)
                else:
                    raise XsltException(Error.STYLESHEET_MISSING_VERSION_NOTE1)
            sheet = StylesheetElement(self._ownerDoc, XSL_NAMESPACE,
                                      'transform', vattr.prefix,
                                      self._ssheetUri)
            sheet.setAttributeNS(EMPTY_NAMESPACE, 'version', vattr.value)
            tpl = TemplateElement(self._ownerDoc, XSL_NAMESPACE, 'template',
                                  vattr.prefix, self._ssheetUri)
            tpl.setAttributeNS(EMPTY_NAMESPACE, 'match', '/')
            sheet.appendChild(tpl)
            sheet.__dict__['extensionNss'] = []
            self._nodeStack[-1].appendChild(sheet)
            # Ensure the literal element is a child of the template
            # endElement appends to the end of the nodeStack
            self._nodeStack.append(tpl)
        self._firstElement = 0
        return

    def _handleExtUris(self, ns, local, value, extUri, delExtu, sheet):
        if (ns, local) == (extUri, 'extension-element-prefixes'):
            ext_prefixes = string.splitfields(value)
            for prefix in ext_prefixes:
                if prefix == '#default': prefix = ''
                uri = self._namespaces[-1].get(prefix, '')
                if uri not in self._extUris:
                    delExtu.append(uri)
                    self._extUris.append(uri)
                if sheet and not uri in sheet.extensionNss:
                    sheet.extensionNss.append(uri)
        return
    
    def processingInstruction(self, target, data):
        self._completeTextNode()
        return

    def comment(self, data):
        self._completeTextNode()
        return

    def startElement(self, name, attribs):
        self._completeTextNode()
        (name, qname, nsattribs) = self._handleStartElementNss(name, attribs)
        nsuri = name[0]
        local = name[1]
        prefix = SplitQName(qname)[0]
        mapping = g_mappings.get(nsuri, None)
        del_extu = []
        if mapping:
            if not mapping.has_key(local):
                if self._firstElement:
                    raise XsltException(Error.STYLESHEET_ILLEGAL_ROOT, name)
                else:
                    raise XsltException(Error.XSLT_ILLEGAL_ELEMENT, local)
            xsl_class = mapping[local]
            if xsl_class == IncludeElement:
                #Can the included sheet have literal result element as root?
                inc = self.clone().fromUri(nsattribs[('', 'href')],
                                           baseUri=self._ssheetUri,
                                           ownerDoc=self._ownerDoc)
                sty = inc.firstChild
                included_nss = GetAllNs(sty)
                for child in sty.childNodes[:]:
                    self._nodeStack[-1].appendChild(child)
                    #migrate old nss from stylesheet directly to new child
                    for prefix in included_nss.keys():
                        if prefix:
                            child.setAttributeNS(XMLNS_NAMESPACE,
                                                 'xmlns:'+prefix,
                                                 included_nss[prefix])
                        else:
                            child.setAttributeNS(XMLNS_NAMESPACE, 'xmlns',
                                                 included_nss[prefix])
                self._nodeStack.append(None)
                pDomlette.ReleaseNode(inc)
                return
            else:
                xsl_instance = xsl_class(self._ownerDoc,
                                         baseUri=self._ssheetUri)
            for aqname in nsattribs.getQNames():
                (ansuri, alocal) = nsattribs.getNameByQName(aqname)


                value = nsattribs.getValueByQName(aqname)
                if ansuri != XMLNS_NAMESPACE and xsl_class == StylesheetElement:
                    self._handleExtUris(ansuri, alocal, value, '',
                                        del_extu,xsl_instance)
                elif not ansuri and alocal not in xsl_instance.__class__.legalAttrs:
                    raise XsltException(Error.XSLT_ILLEGAL_ATTR,
                                        aqname, xsl_instance.nodeName)

                xsl_instance.setAttributeNS(ansuri, aqname, value)
        else:
            if nsuri in self._extUris and self._extElements:
                #Default XsltElement behavior effects fallback
                ext_class = self._extElements.get((nsuri, local), XsltElement)
                xsl_instance = ext_class(self._ownerDoc, nsuri, local,
                                         prefix, self._ssheetUri)
            else:
                xsl_instance = LiteralElement(self._ownerDoc, nsuri, local,
                                              prefix, self._ssheetUri)
            for aqname in nsattribs.getQNames():
                (ansuri, alocal) = nsattribs.getNameByQName(aqname)
                value = nsattribs.getValueByQName(aqname)
                if ansuri != XMLNS_NAMESPACE:
                    self._handleExtUris(ansuri, alocal, value, '',
                                        del_extu, xsl_instance)
                    if hasattr(xsl_instance.__class__, 'legalAttrs'):
                        if not ansuri and alocal not in xsl_instance.__class__.legalAttrs:
                            raise XsltException(Error.XSLT_ILLEGAL_ATTR,
                                                alocal, xsl_instance.nodeName)
                xsl_instance.setAttributeNS(ansuri, aqname, value)
        self._extUriStack.append(del_extu)
        if (xsl_instance.namespaceURI, xsl_instance.localName) == (XSL_NAMESPACE, 'text') or xsl_instance.getAttributeNS(XML_NAMESPACE, 'space') == 'preserve':
            self._preserveStateStack.append(1)
        elif xsl_instance.getAttributeNS(XML_NAMESPACE, 'space') == 'default':
            self._preserveStateStack.append(0)
        else:
            self._preserveStateStack.append(self._preserveStateStack[-1])
        if self._firstElement:
            self._initializeSheet(xsl_instance)
        self._nodeStack.append(xsl_instance)
        return

    def endElement(self, name):
        if not self._nodeStack[-1]:
            del self._nodeStack[-1]
            return
        self._completeTextNode()
        del self._preserveStateStack[-1]
        new_element = self._nodeStack[-1]

        del self._nodeStack[-1]
        del self._namespaces[-1]
        self._nodeStack[-1].appendChild(new_element)
        del_extu = self._extUriStack[-1]
        del self._extUriStack[-1]
        for uri in del_extu:
            self._extUris.remove(uri)
        return

    def characters(self, data):
        self._currText = self._currText + data
        return

def CreateInstantStylesheet(sheet):
    return pDomlette.PickleDocument(sheet.ownerDocument)

def FromInstant(dump, forceBaseUri=None):
    return UnpickleDocument(dump, forceBaseUri).documentElement


##FIXME
##This unpickling code is Basically a transplant from pDomlette
##with the addition of baseUri overriding in unpickling.  It is
##somewhat experimental and not intended to diverge from the pDomlette
##code, and if it ever does so, it should be nixed, and some
##genericity found between this the pDomlette code

import threading, cPickle
g_lock = threading.Lock()
def UnpickleDocument(pickledXml, forceBaseUri=None):
    g_lock.acquire()
    try:
        doc = pDomlette.Document()
        stream = cStringIO.StringIO(pickledXml)
        unpickler = cPickle.Unpickler(stream)
        _UnpickleChildren(unpickler, doc, forceBaseUri)
        return doc
    finally:
        g_lock.release()

def UnpickleNode(pickledXml, doc=None, forceBaseUri=None):
    g_lock.acquire()
    try:
        doc = doc or Document()
        stream = cStringIO.StringIO(pickledXml)
        unpickler = cPickle.Unpickler(stream)
        topLevelNode = unpickler.load()
        if forceBaseUri is None and hasattr(topLevelNode, 'baseUri'):
            topLevelNode.baseUri = forceBaseUri
        doc.appendChild(topLevelNode)
        if topLevelNode.attributes:
            for attr in topLevelNode.attributes.values():
                attr.ownerDocument = topLevelNode.ownerDocument
        _UnpickleChildren(unpickler, topLevelNode, forceBaseUri)
        return topLevelNode
    finally:
        g_lock.release()

## Helper function for unpickling ##


def _UnpickleChildren(unpickler, node, forceBaseUri=None):
    children = unpickler.load()
    while children:
        child = unpickler.load()
        if forceBaseUri is None and hasattr(child, 'baseUri'):
            child.baseUri = forceBaseUri
        node.appendChild(child)
        if child.nodeType == Node.ELEMENT_NODE:
            for attr in child.attributes:
                attr.ownerDocument = child.ownerDocument
        _UnpickleChildren(unpickler, child, forceBaseUri)
        children = children - 1



