########################################################################
#
# File Name:            CopyOfElement.py
#
#
"""
Implementation of the XSLT Spec copy-of element.
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom import EMPTY_NAMESPACE
import xml.dom.ext
from xml.dom import Node
import xml.xslt
from xml.xslt import XsltElement, XsltException, Error
from xml.xslt import g_xsltRecognizedNodes
from xml.xpath import XPathParser, Conversions
from xml.dom import XMLNS_NAMESPACE

class CopyOfElement(XsltElement):
    legalAttrs = ('select',)

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE, localName='copy-of',
                 prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)
        return

    def setup(self):
        parser = XPathParser.XPathParser()
        self.__dict__['_select'] = self.getAttributeNS(EMPTY_NAMESPACE, 'select')
        if not self._select:
            raise XsltException(Error.COPYOF_MISSING_SELECT)
        self.__dict__['_expr'] = parser.parseExpression(self._select)
        self.__dict__['_nss'] = xml.dom.ext.GetAllNs(self)
        return

    def instantiate(self, context, processor):
        origState = context.copy()
        context.setNamespaces(self._nss)
        
        expResult = self._expr.evaluate(context)
        if hasattr(expResult, "nodeType") and expResult.nodeType in g_xsltRecognizedNodes:
            expResult = [expResult]
        if type(expResult) == type([]) :
            for child in expResult:
                self.__copyNode(processor, child)
        else:
            st = Conversions.StringValue(expResult)
            processor.writers[-1].text(st)

        context.set(origState)
        return (context,)

    def __copyNode(self, processor, node):
        if node.nodeType == Node.DOCUMENT_NODE:
            for child in node.childNodes:
                self.__copyNode(processor, child)
        if node.nodeType == Node.DOCUMENT_FRAGMENT_NODE:
            for child in node.childNodes:
                self.__copyNode(processor, child)
        if node.nodeType == Node.TEXT_NODE:
            processor.writers[-1].text(node.data)
        elif node.nodeType == Node.ELEMENT_NODE:
            #FIXME: check if its a root element, and copy its children only, as the spec requires
            processor.writers[-1].startElement(node.nodeName,node.namespaceURI)
            for k in node.attributes.keys():
                if k[0] != XMLNS_NAMESPACE:
                    self.__copyNode(processor, node.attributes[k])
            for child in node.childNodes:
                self.__copyNode(processor, child)
            processor.writers[-1].endElement(node.nodeName)
        elif node.nodeType == Node.ATTRIBUTE_NODE:
            if node.namespaceURI != XMLNS_NAMESPACE:
                processor.writers[-1].attribute(node.name, node.value, node.namespaceURI)
        elif node.nodeType == Node.COMMENT_NODE:
            processor.writers[-1].comment(node.data)
        elif node.nodeType == Node.PROCESSING_INSTRUCTION_NODE:
            processor.writers[-1].processingInstruction(node.target, node.data)
        else:
            pass
        return

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         new_state = (base_state, self._nss, self._select, self._expr)
         return new_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state[0])
        self._nss = state[1]
        self._select = state[2]
        self._expr = state[3]
        return

