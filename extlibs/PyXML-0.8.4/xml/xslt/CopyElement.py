########################################################################
#
# File Name:            CopyElement.py
#
#
"""
Implementation of the XSLT Spec copy stylesheet element.
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 FourThought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import string
from xml.dom import EMPTY_NAMESPACE
import xml.dom.ext
from xml.dom import Node, XMLNS_NAMESPACE
import xml.xslt
from xml.xslt import XsltElement, XsltException, Error
from xml.xpath import CoreFunctions, Util

class CopyElement(XsltElement):
    legalAttrs = ('use-attribute-sets',)

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE, localName='copy',
                 prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        self.__dict__['_useAttributeSets'] = string.splitfields(self.getAttributeNS(EMPTY_NAMESPACE, 'use-attribute-sets'))
        self.__dict__['_nss'] = xml.dom.ext.GetAllNs(self)
        return
        
    def instantiate(self, context, processor):
        origState = context.copy()
        context.setNamespaces(self._nss)
        
        node = context.node
        if node.nodeType == Node.TEXT_NODE:
            processor.writers[-1].text(node.data)
        elif node.nodeType == Node.ELEMENT_NODE:
            #FIXME: Use proper pysax AttributeList objects
            processor.writers[-1].startElement(node.nodeName,
                                               node.namespaceURI)
            for attr_set_name in self._useAttributeSets:
                split_name = Util.ExpandQName(attr_set_name,
                                              namespaces=context.processorNss)
                try:
                    attr_set = processor.attributeSets[split_name]
                except KeyError:
                    raise XsltException(Error.UNDEFINED_ATTRIBUTE_SET, attr_set_name)
                attr_set.use(context, processor)
            for child in self.childNodes:
                context = child.instantiate(context, processor)[0]
            processor.writers[-1].endElement(node.nodeName)
        elif node.nodeType == Node.DOCUMENT_NODE:
            for child in self.childNodes:
                context = child.instantiate(context, processor)[0]
        elif node.nodeType == Node.ATTRIBUTE_NODE:
            if node.namespaceURI == XMLNS_NAMESPACE:
                nodeName = 'xmlns' + (node.localName and ':' + node.localName)
                processor.writers[-1].attribute(nodeName,
                                                node.nodeValue,
                                                node.namespaceURI)
            else:
                processor.writers[-1].attribute(node.nodeName,
                                                node.nodeValue,
                                                node.namespaceURI)
        elif node.nodeType == Node.PROCESSING_INSTRUCTION_NODE:
            processor.writers[-1].processingInstruction(node.target, node.data)
        elif node.nodeType == Node.COMMENT_NODE:
            processor.writers[-1].comment(node.data)
        else:
            raise Exception("Unknown Node Type %d" % node.nodeType)

        context.set(origState)

        return (context,)

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         new_state = (base_state, self._nss, self._useAttributeSets)
         return new_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state[0])
        self._nss = state[1]
        self._useAttributeSets = state[2]
        return

