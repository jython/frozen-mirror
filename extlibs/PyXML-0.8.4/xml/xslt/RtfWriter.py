########################################################################
#
# File Name:            RtfWriter.py
#
#

"""
A special, simple writer for capturing result-tree fragments
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2001 Fourthought Inc., USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import string, os
import NullWriter
from xml.dom import EMPTY_NAMESPACE
from xml.xslt import XSL_NAMESPACE
from xml.xpath import Util
from xml.dom.ext import SplitQName
from xml.dom import XMLNS_NAMESPACE, Node

class RtfWriter(NullWriter.NullWriter):
    def __init__(self, outputParams, ownerDoc):
        self._ownerDoc = ownerDoc
        self._root = ownerDoc.createDocumentFragment()
        self._root.stringValue = ""
        self._nodeStack = [self._root]
        self._currElement = None
        self._outputParams = outputParams

    def getResult(self):
        return self._root

    def startElement(self, name, namespace=EMPTY_NAMESPACE, extraNss=None):
        extraNss = extraNss or {}
        prefix, localName = SplitQName(name)
        new_element = self._ownerDoc.createElementNS(namespace, name)
        self._nodeStack.append(new_element)
        for prefix in extraNss.keys():
            if prefix:
                new_element.setAttributeNS(XMLNS_NAMESPACE, 'xmlns:'+prefix,
                                           extraNss[prefix])
            else:
                new_element.setAttributeNS(XMLNS_NAMESPACE, 'xmlns',
                                           extraNss[prefix])
        new_element.stringValue = ""
        return

    def endElement(self, name):
        new_element = self._nodeStack[-1]
        del self._nodeStack[-1]
        self._nodeStack[-1].appendChild(new_element)
        return

    def text(self, text, escapeOutput=1):
        new_text = self._ownerDoc.createTextNode(text)
        top_node = self._nodeStack[-1]
        top_node.appendChild(new_text)
        top_node.stringValue = top_node.stringValue + text
        return

    def attribute(self, name, value, namespace=EMPTY_NAMESPACE):
        prefix, localName = SplitQName(name)
        attr = self._ownerDoc.createAttributeNS(namespace, name)
        attr.value = value
        if self._nodeStack[-1].nodeType == Node.ELEMENT_NODE:
            self._nodeStack[-1].attributes[(namespace, localName)] = attr
        else:
            #Document-fragment parent
            self._nodeStack[-1].appendChild(attr)
        return

    def processingInstruction(self, target, data):
        pi = self._ownerDoc.createProcessingInstruction(target, data)
        self._nodeStack[-1].appendChild(pi)
        return

    def comment(self, data):
        comment = self._ownerDoc.createComment(data)
        self._nodeStack[-1].appendChild(comment)
        return

