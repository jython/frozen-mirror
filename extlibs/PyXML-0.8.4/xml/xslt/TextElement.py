########################################################################
#
# File Name:            TextElement.py
#
#
"""
Implementation of the XSLT Spec text stylesheet element.
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom import EMPTY_NAMESPACE
import xml.dom.ext
import xml.dom.Element
from xml.xpath import CoreFunctions
from xml.xslt import XsltElement, XsltException, Error
from xml.dom import Node

class TextElement(XsltElement):
    legalAttrs = ('disable-output-escaping',)

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE, localName='text', prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)
        return

    def setup(self):
        self.__dict__['_disable_output_escaping'] = self.getAttributeNS(EMPTY_NAMESPACE, 'disable-output-escaping') == 'yes'
        self.__dict__['_nss'] = xml.dom.ext.GetAllNs(self)
        for child in self.childNodes:
            if child.nodeType == Node.ELEMENT_NODE:
                raise XsltException(Error.ILLEGAL_TEXT_CHILD)
        self.normalize()
        return

    def instantiate(self, context, processor):
        if not self.firstChild:
            return (context,)

        if context.processorNss != self._nss:
            origState = context.copyNamespaces()
            context.setNamespaces(self._nss)
        else:
            origState = None
        
        value = self.firstChild and self.firstChild.data or ''
        if self._disable_output_escaping:
            processor.writers[-1].text(value, escapeOutput=0)
        else:
            processor.writers[-1].text(value)

        origState and context.setNamespaces(origState)
        return (context,)

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         new_state = (base_state, self._nss, self._disable_output_escaping)
         return new_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state[0])
        self._nss = state[1]
        self._disable_output_escaping = state[2]
        return

