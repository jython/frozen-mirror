########################################################################
#
# File Name:            Processor.py
#
#
"""
Implement the XSLT processor engine
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import string, os, sys
import traceback
import xml.dom.ext
from xml.dom import XML_NAMESPACE,EMPTY_NAMESPACE
from xml.dom.ext import reader
from xml.dom import Node
from xml.xpath import Util
from xml.xslt import XSL_NAMESPACE, XsltContext
from xml.xslt import RtfWriter, OutputHandler, OutputParameters, Error, XsltException
from xml.xslt import StylesheetReader, ReleaseNode
try:
    from Ft.Lib import pDomlette
    import Ft.Lib
    have_pDomlette = 1
except ImportError:
    from xml.dom import minidom
    have_pDomlette = 0
from xml import xpath, xslt

import os
BETA_DOMLETTE = os.environ.get("BETA_DOMLETTE")
if BETA_DOMLETTE:
    from Ft.Lib import cDomlette
    g_readerClass = cDomlette.RawExpatReader
    g_domModule = cDomlette
else:
    if have_pDomlette:
        g_readerClass = pDomlette.PyExpatReader
        g_domModule = pDomlette
    else:
        import minisupport
        g_readerClass = minisupport.MinidomReader
        g_domModule = minidom

XSLT_IMT = ['text/xml', 'application/xml']

class Processor:
    def __init__(self, reader=None):
        self._stylesheets = []
        self.writers = []
        self._reset()
        self._dummyDoc = g_domModule.Document()

        #Can be overridden
        self._styReader = StylesheetReader.StylesheetReader()
        self._docReader = reader or g_readerClass()
        self._lastOutputParams = None

        if not xslt.g_registered:
            xslt.Register()
        return

    def _reset(self):
        self.attributeSets = {}
        for sty in self._stylesheets:
            sty.reset()
        self.sheetWithCurrTemplate = [None]
        #A stack of writers, to support result-tree fragments
        self.writers = []
        #self.extensionParams = {}
        return

    def _getWsStripElements(self):
        space_rules = {}
        for a_sheet in self._stylesheets:
            space_rules.update(a_sheet.spaceRules)
        strip_elements = map(lambda x: (x[0][0], x[0][1], x[1] == 'strip'), space_rules.items())
        strip_elements.append((XSL_NAMESPACE,'text',0))
        return strip_elements

    def registerExtensionModules(self, moduleList):
        return xslt.RegisterExtensionModules(moduleList)

    def setStylesheetReader(self, readInst):
        self._styReader = readInst
        
    def setDocumentReader(self, readInst):
        self._docReader = readInst

    def appendStylesheetUri(self, styleSheetUri, baseUri=''):
        sty = self._styReader.fromUri(styleSheetUri, baseUri)
        self._stylesheets.append(sty)
        return

    appendStylesheetFile = appendStylesheetUri

    def appendStylesheetNode(self, styleSheetNode, baseUri=''):
        """Accepts a DOM node that must be a document containing the stylesheet"""
        sty = StylesheetReader.FromDocument(styleSheetNode, baseUri)
        self._stylesheets.append(sty)
        return

    def appendStylesheetString(self, text, baseUri=''):
        sty = self._styReader.fromString(text, baseUri)
        self._stylesheets.append(sty)
        return

    def appendStylesheetStream(self, stream, baseUri=''):
        sty = self._styReader.fromStream(stream, baseUri)
        self._stylesheets.append(sty)
        return

    def appendInstantStylesheet(self, sty):
        """Accepts a valid StyleDOM node"""
        self._stylesheets.append(sty)
        return

    def runString(self, xmlString, ignorePis=0, topLevelParams=None,
                  writer=None, baseUri='', outputStream=None):
        try:
            src = self._docReader.fromString(xmlString,stripElements=self._getWsStripElements())
        except Exception, e:
            raise XsltException(Error.SOURCE_PARSE_ERROR, '<Python string>', e)
        if not ignorePis and self.checkStylesheetPis(src, baseUri):
            #FIXME: should we leave this to GC in Python 2.0?
            self._docReader.releaseNode(src)
            #Do it again with updates WS strip lists
            try:
                src = self._docReader.fromString(xmlString,stripElements=self._getWsStripElements())
            except Exception, e:
                raise XsltException(Error.SOURCE_PARSE_ERROR, '<Python string>', e)
        result = self.execute(src, ignorePis, topLevelParams, writer,
                              baseUri, outputStream)

        #FIXME: should we leave this to GC in Python 2.0?
        self._docReader.releaseNode(src)
        return result

    def runUri(self, uri, ignorePis=0, topLevelParams=None, writer=None,
               outputStream=None):
        try:
            src = self._docReader.fromUri(uri, stripElements=self._getWsStripElements())
        except Exception, e:
            import traceback
            traceback.print_exc()
            raise XsltException(Error.SOURCE_PARSE_ERROR, uri, e)
        if not ignorePis and self.checkStylesheetPis(src, uri):
            self._docReader.releaseNode(src)
            #Do it again with updates WS strip lists
            try:
                src = self._docReader.fromUri(uri,stripElements=self._getWsStripElements())
            except Exception, e:
                raise XsltException(Error.SOURCE_PARSE_ERROR, uri, e)
        result = self.execute(src, ignorePis, topLevelParams,
                              writer, uri, outputStream)
        self._docReader.releaseNode(src)
        return result

    def runStream(self, stream, ignorePis=0, topLevelParams=None, writer=None,
                  baseUri='', outputStream=None):
        try:
            src = self._docReader.fromStream(
                stream, stripElements=self._getWsStripElements()
                )
        except Exception, e:
            raise XsltException(Error.SOURCE_PARSE_ERROR, '<input stream>', e)
        if not ignorePis and self.checkStylesheetPis(src, baseUri):
            #FIXME: Will this work with tty streams?
            stream.seek(0,0)
            self._docReader.releaseNode(src)
            #Do it again with updated WS strip lists
            try:
                src = self._docReader.fromStream(
                    stream, stripElements=self._getWsStripElements()
                    )
            except Exception, e:
                raise XsltException(Error.SOURCE_PARSE_ERROR, '<input stream>', e)
        result = self.execute(src, ignorePis, topLevelParams,
                              writer, baseUri, outputStream)
        self._docReader.releaseNode(src)
        return result

    def runNode(self, node, ignorePis=0, topLevelParams=None, writer=None,
               baseUri='', outputStream=None, forceStripElements = 0):
        'Note: this method could mutate the node'
        node.normalize()
        if not ignorePis and self.checkStylesheetPis(node, baseUri):
            #FIXME: should re-strip white-space
            pass
        if forceStripElements:
            #WARNING: This will mutate the source
            self._stripElements(node)

        result = self.execute(node, ignorePis, topLevelParams, writer,
                              baseUri, outputStream)
        return result
        
    def checkStylesheetPis(self, node, baseUri):
        pis_found = 0
        #Note: A Stylesheet PI can only be in the prolog, acc to the NOTE
        #http://www.w3.org/TR/xml-stylesheet/
        if node.nodeType == Node.DOCUMENT_NODE:
            ownerDoc = node
        else:
            ownerDoc = node.ownerDoc
        for child in ownerDoc.childNodes:
            if child.nodeType == Node.PROCESSING_INSTRUCTION_NODE:
                if child.target == 'xml-stylesheet':
                    data = child.data
                    data = string.splitfields(data,' ')
                    sty_info = {}
                    for d in data:
                        seg = string.splitfields(d, '=')
                        if len(seg) == 2:
                            sty_info[seg[0]] = seg[1][1:-1]
                            if sty_info.has_key('href'):
                                if not sty_info.has_key('type') \
                                   or sty_info['type'] in XSLT_IMT:
                                    self.appendStylesheetUri(sty_info['href'], baseUri)
                                    pis_found = 1
        return pis_found

    def execute(self, node, ignorePis=0, topLevelParams=None, writer=None,
                baseUri='', outputStream=None):
        """
        Run the stylesheet processor against the given XML DOM node with the
        stylesheets that have been registered.  Does not mutate the DOM
        If writer is None, use the XmlWriter, otherwise, use the
        supplied writer
        """
        #FIXME: What about ws stripping?
        topLevelParams = topLevelParams or {}

        if len(self._stylesheets) == 0:
            raise XsltException(Error.NO_STYLESHEET)

        self._outputParams = self._stylesheets[0].outputParams

        if writer:
            self.writers = [writer]
        else:
            self.addHandler(self._outputParams, outputStream, 0)

        self._namedTemplates = {}
        tlp = topLevelParams.copy()
        for sty in self._stylesheets:
            sty.processImports(node, self, tlp)
            named = sty.getNamedTemplates()
            for name,template_info in named.items():
                if not self._namedTemplates.has_key(name):
                    self._namedTemplates[name] = template_info

        for sty in self._stylesheets:
            tlp = sty.prime(node, self, tlp)

        #Run the document through the style sheets
        self.writers[-1].startDocument()
        context = XsltContext.XsltContext(node, 1, 1, None, processor=self)
        try:
            self.applyTemplates(context, None)
            self.writers[-1].endDocument()

            Util.FreeDocumentIndex(node)

            result = self.writers[-1].getResult()

        finally:
            self._reset()
            context.release()

        return result

    def applyTemplates(self, context, mode, params=None):
        params = params or {}
        for sty in self._stylesheets:
            self.sheetWithCurrTemplate.append(sty)
            found = sty.applyTemplates(context, mode, self, params)
            del self.sheetWithCurrTemplate[-1]
            if found: break
        else:
            self.applyBuiltins(context, mode)
        return

    def applyBuiltins(self, context, mode):
        if context.node.nodeType == Node.TEXT_NODE:
            self.writers[-1].text(context.node.data)
        elif context.node.nodeType in [Node.ELEMENT_NODE, Node.DOCUMENT_NODE]:
            origState = context.copyNodePosSize()
            node_set = context.node.childNodes
            size = len(node_set)
            pos = 1
            for node in node_set:
                context.setNodePosSize((node,pos,size))
                self.applyTemplates(context, mode)
                pos = pos + 1
            context.setNodePosSize(origState)
        elif context.node.nodeType == Node.ATTRIBUTE_NODE:
            self.writers[-1].text(context.node.value)
        return

    def applyImports(self, context, mode, params=None):
        params = params or {}
        if not self.sheetWithCurrTemplate[-1]:
            raise XsltException(Error.APPLYIMPORTS_WITH_NULL_CURRENT_TEMPLATE)
        self.sheetWithCurrTemplate[-1].applyImports(context, mode, self)
        return

    def xslMessage(self, msg):
        sys.stderr.write("STYLESHEET MESSAGE:\n")
        sys.stderr.write(msg+'\n')
        sys.stderr.write("END STYLESHEET MESSAGE:\n")
        return

    def callTemplate(self, name, context, params, new_level=1):
        tpl_info = self._namedTemplates.get(name)
        if tpl_info:
            (stylesheet, template) = tpl_info
            variables = stylesheet.getTopLevelVariables()
            variables.update(params)

            origState = context.copyStylesheet()
            context.setStylesheet((variables, stylesheet.namespaces, stylesheet))
        
            rec_tpl_params = template.instantiate(context, self, params, new_level)[1]
            context.setStylesheet(origState)
        else:
            rec_tpl_params = None
        
        return rec_tpl_params

    def _writerChanged(self, newWriter):
        self.writers[-1] = newWriter

    def addHandler(self, outputParams, stream=None, start=1):
        handler = OutputHandler.OutputHandler(outputParams, stream, self._writerChanged)
        self.writers.append(handler)
        start and self.writers[-1].startDocument()

    def removeHandler(self):
        self.writers[-1].endDocument()
        del self.writers[-1]

    def pushResult(self, handler=None, ownerDoc=None):
        """
        Start processing all content into a separate result-tree
        (either an rtf, or for ft:write-file)
        """
        #FIXME: Should actually use a doc fragment for the SAX handler doc
        #Q: Should the output parameters discovered at run-time (e.g html root element) be propagated back to RTFs?
        handler = handler or RtfWriter.RtfWriter(self._outputParams,
                                                 ownerDoc or self._dummyDoc)
        self.writers.append(handler)
        return

    def popResult(self):
        """End sub-result-tree and return any result"""
        result = self.writers[-1].getResult()
        del self.writers[-1]
        return result

    def releaseRtf(self, rtfRoot):
        ReleaseNode(rtfRoot)
        return

    def _stripElements(self,node):
        stripElements = self._getWsStripElements()
        self.__stripNode(node,stripElements,0)
        return

    def __stripNode(self,node,stripElements,stripState):
        if node.nodeType == Node.DOCUMENT_NODE:
            for c in node.childNodes:
                self.__stripNode(c,stripElements,stripState)
        elif node.nodeType == Node.ELEMENT_NODE:

            #See if we need to change the strip state
            if node.getAttributeNodeNS(XML_NAMESPACE,'space') == 'preserve':
                #Force the state to preserve
                stripState = 0
            elif node.getAttributeNodeNS(XML_NAMESPACE,'space'):
                #Force to strip
                stripState = 1
            elif (node.namespaceURI, node.localName) == (XSL_NAMESPACE,'text'):
                #xsl:text never get striped
                stripState = 0
            else:
                #See if it is a perserve or strip element
                for (uri, local, strip) in stripElements:
                    if (uri, local) in [(node.namespaceURI, node.localName), (EMPTY_NAMESPACE, '*'), (node.namespaceURI, '*')]:
                        stripState = strip
                        break
            
            for c in node.childNodes:
                self.__stripNode(c,stripElements,stripState)
        elif node.nodeType == Node.TEXT_NODE:
            if stripState and not string.strip(node.data):
                #Kill'em all
                node.parentNode.removeChild(node)


    def reclaim(self):
        try:
            ReleaseNode(self._dummyDoc)
        except:
            pass
        self._dummyDoc = None
        
        try:
            for sheet in self._stylesheets:
                sheet.reclaim()
                self._styReader.releaseNode(sheet.ownerDocument)
        except:
            pass
        self._stylesheets = []

    #Python 2.0 has GC, but it doesn't try to auto-reclaim classes with __del__
    if sys.version[0] != '2':
        __del__ = reclaim

