########################################################################
#
# File Name:            HtmlSax.py
#
#
#
"""
Components for reading HTML files from a SAX-like producer.
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import sys, string, cStringIO
import xml.dom.ext
from xml.dom import Node
from xml.dom import implementation


class HtmlDomGenerator:
    def __init__(self, keepAllWs=0):
        self._keepAllWs = keepAllWs

    def initState(self, ownerDoc=None):
        """
        If None is passed in as the doc, set up an empty document to act
        as owner and also add all elements to this document
        """
        if ownerDoc == None:
            self._ownerDoc = implementation.createHTMLDocument('')
            de = self._ownerDoc.documentElement
            self._ownerDoc.removeChild(de)
            xml.dom.ext.ReleaseNode(de)
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

    #Overridden DocumentHandler methods
    def startElement(self, name, attribs):
        self._completeTextNode()
        new_element = self._ownerDoc.createElement(name)

        for curr_attrib_key in attribs.keys():
            new_element.setAttribute(curr_attrib_key, attribs[curr_attrib_key])
        self._nodeStack.append(new_element)

    def endElement(self, name):
        self._completeTextNode()
        new_element = self._nodeStack[-1]
        del self._nodeStack[-1]
        self._nodeStack[-1].appendChild(new_element)

    def ignorableWhitespace(self, ch, start, length):
        """
        If 'keepAllWs' permits, add ignorable white-space as a text node.
        Remember that a Document node cannot contain text nodes directly.
        If the white-space occurs outside the root element, there is no place
        for it in the DOM and it must be discarded.
        """
        if self._keepAllWs and self._nodeStack[-1].nodeType !=  Node.DOCUMENT_NODE:
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
