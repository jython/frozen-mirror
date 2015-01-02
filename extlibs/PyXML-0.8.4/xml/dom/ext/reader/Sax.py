########################################################################
#
# File Name:            Sax.py
#
#
"""
Components for reading XML files from a SAX producer.
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import sys, string, cStringIO, urllib2
from xml.sax import saxlib, saxexts, drivers
from xml.dom import Entity, DocumentType, Document
from xml.dom import DocumentType, Document
from xml.dom import implementation
from xml.dom.ext import SplitQName, ReleaseNode
from xml.dom.ext import reader

class XmlDomGenerator(saxlib.HandlerBase):
    def __init__(self, keepAllWs=0):
        self._keepAllWs = keepAllWs
        return

    def initState(self, ownerDoc=None):
        """
        If None is passed in as the doc, set up an empty document to act
        as owner and also add all elements to this document
        """
        if ownerDoc == None:
            dt = implementation.createDocumentType('', '', '')
            self._ownerDoc = implementation.createDocument('', None, dt)
            self._rootNode = self._ownerDoc
        else:
            self._ownerDoc = ownerDoc
            #Create a docfrag to hold all the generated nodes.
            self._rootNode = self._ownerDoc.createDocumentFragment()

        #Set up the stack which keeps track of the nesting of DOM nodes.
        self._nodeStack = []
        self._nodeStack.append(self._rootNode)
        self._currText = ''
        return

    def getRootNode(self):
        self._completeTextNode()
        return self._rootNode

    def _completeTextNode(self):
        if self._currText:
            new_text = self._ownerDoc.createTextNode(self._currText)
            self._nodeStack[-1].appendChild(new_text)
            self._currText = ''

    #Overridden DTDHandler methods
    def notationDecl (self, name, publicId, systemId):
        new_notation = self._ownerDoc.createNotation(self._ownerDoc,  publicId, systemId, name)
        self._ownerDoc.documentType.notations.setNamedItem(new_notation)

    def unparsedEntityDecl (self, name, publicId, systemId, notationName):
        new_notation = implementation.createEntity(self._ownerDoc,  publicId, systemId, notationName)
        self._ownerDoc.documentType.entities.setNamedItem(new_notation)

    #Overridden DocumentHandler methods
    def processingInstruction (self, target, data):
        self._completeTextNode()
        p = self._ownerDoc.createProcessingInstruction(target,data);
        self._nodeStack[-1].appendChild(p)

    def startElement(self, name, attribs):
        self._completeTextNode()
        new_element = self._ownerDoc.createElement(name)

        for curr_attrib_key in attribs.keys():
            new_element.setAttribute(
                curr_attrib_key,
                attribs[curr_attrib_key]
                )
        self._nodeStack.append(new_element)

    def endElement(self, name):
        self._completeTextNode()
        new_element = self._nodeStack[-1]
        del self._nodeStack[-1]
        self._nodeStack[-1].appendChild(new_element)

    def ignorableWhitespace(self, ch, start, length):
        """
        If 'keepAllWs' permits, add ignorable white-space as a text node.
        A Document node cannot contain text nodes directly.
        If the white-space occurs outside the root element, there is no place
        for it in the DOM and it must be discarded.
        """
        if self._keepAllWs:
            self._currText = self._currText + ch[start:start+length]

    def characters(self, ch, start, length):
        self._currText = self._currText + ch[start:start+length]

    #Overridden ErrorHandler methods
    #def warning(self, exception):
    #   raise exception

    def error(self, exception):
        raise exception

    def fatalError(self, exception):
        raise exception


class Reader(reader.Reader):
    def __init__(self, validate=0, keepAllWs=0, catName=None,
                 saxHandlerClass=XmlDomGenerator, parser=None):
        #Create an XML DOM from SAX events
        self.parser = parser or (validate and saxexts.XMLValParserFactory.make_parser()) or saxexts.XMLParserFactory.make_parser()
        if catName:
            #set up the catalog, if there is one
            from xml.parsers.xmlproc import catalog
            cat_handler = catalog.SAX_catalog(catName, catalog.CatParserFactory())
            self.parser.setEntityResolver(cat_handler)
        self.handler = saxHandlerClass(keepAllWs)
        self.parser.setDocumentHandler(self.handler)
        self.parser.setDTDHandler(self.handler)
        self.parser.setErrorHandler(self.handler)
        return

    def releaseNode(self, node):
        ReleaseNode(node)

    def fromStream(self, stream, ownerDocument=None):
        self.handler.initState(ownerDoc=ownerDocument)
        self.parser.parseFile(stream)
        return self.handler.getRootNode()


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
