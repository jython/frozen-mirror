########################################################################
#
# File Name:            Sax2.py
#
#
"""
Components for reading XML files from a SAX2 producer.
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000, 2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import sys, string, cStringIO, os, urllib2
from xml.sax import saxlib, saxutils, sax2exts, handler
from xml.dom import Entity, DocumentType, Document
from xml.dom import Node
from xml.dom import implementation
from xml.dom.ext import SplitQName, ReleaseNode
from xml.dom import XML_NAMESPACE, XMLNS_NAMESPACE, EMPTY_NAMESPACE
from xml.dom import Element
from xml.dom import Attr
from xml.dom.ext import reader


class NsHandler:
    def initState(self, ownerDoc=None):
        self._namespaces = {'xml': XML_NAMESPACE, None: EMPTY_NAMESPACE}
        self._namespaceStack = []
        return

    def startElement(self, name, attribs):
        self._completeTextNode()
        old_nss = {}
        del_nss = []
        for curr_attrib_key, value in attribs.items():
            (prefix, local) = SplitQName(curr_attrib_key)
            if local == 'xmlns':
                if self._namespaces.has_key(prefix):
                    old_nss[prefix] = self._namespaces[prefix]
                    if value:
                        self._namespaces[prefix] = attribs[curr_attrib_key]
                    else:
                        del self._namespaces[prefix]
                elif value:
                    self._namespaces[prefix] = attribs[curr_attrib_key]
                    del_nss.append(prefix)

        self._namespaceStack.append((old_nss, del_nss))
        (prefix, local) = SplitQName(name)
        nameSpace = self._namespaces.get(prefix, None)

        if self._ownerDoc:
            new_element = self._ownerDoc.createElementNS(nameSpace, (prefix and prefix + ':' +  local) or local)
        else:
            self._initRootNode(nameSpace, name)
            new_element = self._ownerDoc.documentElement

        for curr_attrib_key,curr_attrib_value in attribs.items():
            (prefix, local) = SplitQName(curr_attrib_key)
            qname = local
            if local == 'xmlns':
                namespace = XMLNS_NAMESPACE
                if prefix:
                    qname = local + ':' + prefix
                attr = self._ownerDoc.createAttributeNS(namespace, qname)
            else:
                if prefix:
                    qname = prefix + ':' + local
                namespace = prefix and self._namespaces.get(prefix, None) or None
                attr = self._ownerDoc.createAttributeNS(namespace, qname)
            attr.value = curr_attrib_value
            new_element.setAttributeNodeNS(attr)
        self._nodeStack.append(new_element)
        return

    def endElement(self, name):
        self._completeTextNode()
        new_element = self._nodeStack[-1]
        del self._nodeStack[-1]
        old_nss, del_nss = self._namespaceStack[-1]
        del self._namespaceStack[-1]
        self._namespaces.update(old_nss)
        for prefix in del_nss:
            del self._namespaces[prefix]
        if new_element != self._ownerDoc.documentElement:
            self._nodeStack[-1].appendChild(new_element)
        return


class XmlDomGenerator(NsHandler, saxutils.DefaultHandler,
                      saxlib.LexicalHandler,
                      saxlib.DeclHandler):
    def __init__(self, keepAllWs=0, implementation=implementation):
        self._keepAllWs = keepAllWs
        self._impl = implementation
        return

    def initState(self, ownerDoc=None):
        self._ownerDoc = None
        self._rootNode = None
        #Set up the stack which keeps track of the nesting of DOM nodes.
        self._nodeStack = []
        self._nsuri2pref = {EMPTY_NAMESPACE:[None], XML_NAMESPACE: ['xml']}
        self._pref2nsuri = {None: [EMPTY_NAMESPACE], 'xml': XML_NAMESPACE}
        self._new_prefix_mappings = []
        if ownerDoc:
            self._ownerDoc = ownerDoc
            #Create a docfrag to hold all the generated nodes.
            self._rootNode = self._ownerDoc.createDocumentFragment()
            self._nodeStack.append(self._rootNode)
        self._dt = None
        self._xmlDecl = None
        self._orphanedNodes = []
        self._currText = ''
        NsHandler.initState(self, ownerDoc)
        return

    def _initRootNode(self, docElementUri, docElementName):
        if not self._dt:
            self._dt = self._impl.createDocumentType(docElementName, None, '')
        self._ownerDoc = self._impl.createDocument(docElementUri, docElementName, self._dt)
        if self._xmlDecl:
            decl_data = 'version="%s"' % (
                    self._xmlDecl['version']
                    )
            if self._xmlDecl['encoding']:
                decl_data = decl_data + ' encoding="%s"'%(
                    self._xmlDecl['encoding']
                    )
            if self._xmlDecl['standalone']:
                decl_data = decl_data + ' standalone="%s"'%(
                    self._xmlDecl['standalone']
                    )
            xml_decl_node = self._ownerDoc.createProcessingInstruction(
                'xml',
                decl_data
                )
            self._ownerDoc.insertBefore(xml_decl_node, self._ownerDoc.docType)
        before_doctype = 1
        for o_node in self._orphanedNodes:
            if o_node[0] == 'pi':
                pi = self._ownerDoc.createProcessingInstruction(
                    o_node[1],
                    o_node[2]
                    )
                if before_doctype:
                    self._ownerDoc.insertBefore(pi, self._dt)
                else:
                    self._ownerDoc.appendChild(pi)
            elif o_node[0] == 'comment':
                comment = self._ownerDoc.createComment(o_node[1])
                if before_doctype:
                    self._ownerDoc.insertBefore(comment, self._dt)
                else:
                    self._ownerDoc.appendChild(comment)
            elif o_node[0] == 'doctype':
                before_doctype = 0
            elif o_node[0] == 'unparsedentitydecl':
                apply(self.unparsedEntityDecl, o_node[1:])
            else:
                raise "Unknown orphaned node:"+o_node[0]
        self._rootNode = self._ownerDoc
        self._nodeStack.append(self._rootNode)
        return

    def _completeTextNode(self):
        #Note some parsers don't report ignorable white space properly
        if self._currText and len(self._nodeStack) and self._nodeStack[-1].nodeType != Node.DOCUMENT_NODE:
            new_text = self._ownerDoc.createTextNode(self._currText)
            self._nodeStack[-1].appendChild(new_text)
        self._currText = ''
        return

    def getRootNode(self):
        self._completeTextNode()
        return self._rootNode

    #Overridden DocumentHandler methods
    def processingInstruction(self, target, data):
        if self._rootNode:
            self._completeTextNode()
            pi = self._ownerDoc.createProcessingInstruction(target, data)
            self._nodeStack[-1].appendChild(pi)
        else:
            self._orphanedNodes.append(('pi', target, data))
        return

    def startPrefixMapping(self, prefix, uri):
        try:
            map = self._pref2nsuri[prefix]
        except:
            map = []
            self._pref2nsuri[prefix] = map
        map.append(uri)

        try:
            map = self._nsuri2pref[uri]
        except:
            map = []
            self._nsuri2pref[uri] = map
        map.append(prefix)
        self._new_prefix_mappings.append((prefix,uri))
##        print 'startPrefixMapping',prefix,uri
##        print 'pref->uri',self._pref2nsuri
##        print 'uri->pref',self._nsuri2pref

    def endPrefixMapping(self, prefix):
##        print 'endPrefixMapping',prefix
##        print 'pref->uri',self._pref2nsuri
##        print 'uri->pref',self._nsuri2pref

        uri = self._pref2nsuri[prefix][-1]
        del self._pref2nsuri[prefix][-1]
        del self._nsuri2pref[uri][-1]
        if not self._pref2nsuri[prefix]:
            del self._pref2nsuri[prefix]
        if not self._nsuri2pref[uri]:
            del self._nsuri2pref[uri]

    def startElementNS(self, name, qname, attribs):
        self._completeTextNode()
        namespace = name[0]
        local = name[1]
        if qname is None:
            if self._nsuri2pref[namespace][-1]:
                qname = string.join((self._nsuri2pref[namespace][-1], local), ':')
            else :
                qname = local
        if self._ownerDoc:
            new_element = self._ownerDoc.createElementNS(namespace, qname)
        else:
            self._initRootNode(namespace, qname)
            new_element = self._ownerDoc.documentElement

        for ((attr_ns, lname), value) in attribs.items():
            if attr_ns is not None:
                try:
                    attr_qname = attribs.getQNameByName((attr_ns, lname))
                except KeyError:# pyexpat doesn't report qnames...
                    attr_prefix = self._nsuri2pref[attr_ns][-1]
                    if attr_prefix is None: # I'm not sure that this is possible
                        attr_qname = lname
                    else:
                        attr_qname = string.join((attr_prefix,lname), ':')
            else:
                attr_qname = lname
            attr = self._ownerDoc.createAttributeNS(attr_ns, attr_qname)
            attr.value = value
            new_element.setAttributeNodeNS(attr)

        for (prefix,uri) in self._new_prefix_mappings:
            if prefix is  None :
                new_element.setAttributeNS(XMLNS_NAMESPACE,'xmlns',uri or '')
            else:
                new_element.setAttributeNS(XMLNS_NAMESPACE,'xmlns'+':'+prefix,uri)
        self._new_prefix_mappings = []
        self._nodeStack.append(new_element)
        return

    def endElementNS(self, name, qname):
        self._completeTextNode()
        new_element = self._nodeStack[-1]
        del self._nodeStack[-1]
        if new_element != self._ownerDoc.documentElement:
            self._nodeStack[-1].appendChild(new_element)
        return

    def ignorableWhitespace(self, chars):
        """
        If 'keepAllWs' permits, add ignorable white-space as a text node.
        A Document node cannot contain text nodes directly.
        If the white-space occurs outside the root element, there is no place
        for it in the DOM and it must be discarded.
        """
        if self._keepAllWs and self._nodeStack[-1].nodeType !=  Node.DOCUMENT_NODE:
            self._currText = self._currText + chars
        return

    def characters(self, chars):
        self._currText = self._currText + chars
        return

    #Overridden LexicalHandler methods
    def xmlDecl(self, version, encoding, standalone):
        self._xmlDecl = {'version': version, 'encoding': encoding, 'standalone': standalone}
        return

    def startDTD(self, doctype, publicID, systemID):
        self._dt = self._impl.createDocumentType(doctype, publicID, systemID)
        if not self._rootNode:
            self._orphanedNodes.append(('doctype',))
        #else:
            #raise Exception('Illegal DocType declaration')
        return

    def comment(self, text):
        if self._rootNode:
            self._completeTextNode()
            new_comment = self._ownerDoc.createComment(text)
            self._nodeStack[-1].appendChild(new_comment)
        else:
            self._orphanedNodes.append(('comment', text))
        return

    def startCDATA(self):
        self._completeTextNode()
        return

    def endCDATA(self):
        #NOTE: this doesn't handle the error where endCDATA is called
        #Without corresponding startCDATA.  Is this a problem?
        if self._currText:
            new_text = self._ownerDoc.createCDATASection(self._currText)
            self._nodeStack[-1].appendChild(new_text)
            self._currText = ''
        return

    #Overridden DTDHandler methods
    def notationDecl (self, name, publicId, systemId):
        new_notation = self._ownerDoc.getFactory().createNotation(self._ownerDoc,  publicId, systemId, name)
        self._ownerDoc.getDocumentType().getNotations().setNamedItem(new_notation)
        return

    def unparsedEntityDecl (self, name, publicId, systemId, ndata):
        if self._ownerDoc:
            new_notation = self._ownerDoc.getFactory().createEntity(self._ownerDoc,  publicId, systemId, name)
            self._ownerDoc.getDocumentType().getEntities().setNamedItem(new_notation)
        else:
            self._orphanedNodes.append(('unparsedentitydecl', name, publicId, systemId, ndata))
        return

    #Overridden ErrorHandler methods
    #FIXME: How do we handle warnings?

    def error(self, exception):
        raise exception

    def fatalError(self, exception):
        raise exception


class Reader(reader.Reader):
    def __init__(self, validate=0, keepAllWs=0, catName=None,
                 saxHandlerClass=XmlDomGenerator, parser=None):
        self.parser = parser or (validate and sax2exts.XMLValParserFactory.make_parser()) or sax2exts.XMLParserFactory.make_parser()
        if catName:
            #set up the catalog, if there is one
            from xml.parsers.xmlproc import catalog
            cat_handler = catalog.SAX_catalog(
                catName, catalog.CatParserFactory()
                )
            self.parser.setEntityResolver(cat_handler)
        self.handler = saxHandlerClass(keepAllWs)
        self.parser.setContentHandler(self.handler)
        self.parser.setDTDHandler(self.handler)
        self.parser.setErrorHandler(self.handler)
        try:
            #FIXME: Maybe raise a warning?
            self.parser.setProperty(handler.property_lexical_handler, self.handler)
            self.parser.setProperty(handler.property_declaration_handler, self.handler)
        except (SystemExit, KeyboardInterrupt):
            raise
        except:
            pass
        return

    def fromStream(self, stream, ownerDoc=None):
        self.handler.initState(ownerDoc=ownerDoc)
        #self.parser.parseFile(stream)
        s = saxutils.prepare_input_source(stream)
        self.parser.parse(s)
        rt = self.handler.getRootNode()
        #if hasattr(self.parser.parser,'deref'):
        #    self.parser.parser.deref()
        #self.parser.parser = None
        #self.parser = None
        #self.handler = None
        return rt

########################## Deprecated ##############################

def FromXmlStream(stream, ownerDocument=None, validate=0, keepAllWs=0,
                  catName=None, saxHandlerClass=XmlDomGenerator, parser=None):
    reader = Reader(validate, keepAllWs, catName, saxHandlerClass, parser)
    return reader.fromStream(stream, ownerDocument)


def FromXml(text, ownerDocument=None, validate=0, keepAllWs=0,
            catName=None, saxHandlerClass=XmlDomGenerator, parser=None):
    fp = cStringIO.StringIO(text)
    rv = FromXmlStream(fp, ownerDocument, validate, keepAllWs, catName,
                       saxHandlerClass, parser)
    return rv


def FromXmlFile(fileName, ownerDocument=None, validate=0, keepAllWs=0,
                catName=None, saxHandlerClass=XmlDomGenerator, parser=None):
    fp = open(fileName, 'r')
    try:
        rv = FromXmlStream(fp, ownerDocument, validate, keepAllWs, catName,
                           saxHandlerClass, parser)
    finally:
        fp.close()
    return rv


def FromXmlUrl(url, ownerDocument=None, validate=0, keepAllWs=0,
               catName=None, saxHandlerClass=XmlDomGenerator, parser=None):
    fp = urllib2.urlopen(url)
    try:
        rv = FromXmlStream(fp, ownerDocument, validate, keepAllWs, catName,
                           saxHandlerClass, parser)
    finally:
        fp.close()
    return rv
