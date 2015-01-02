########################################################################
#
# File Name:            MessageElement.py
#
#
"""
Implementation of the XSLT Spec import stylesheet element.
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""
import cStringIO
from xml.dom import EMPTY_NAMESPACE
import xml.dom.ext
import xml.dom.Element
import xml.xslt
from xml.xslt import XsltElement, XsltException, Error
from xml.xpath import Conversions

class MessageElement(XsltElement):
    legalAttrs = ('terminate',)

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE, localName='message',
                 prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        self.__dict__['_terminate'] = self.getAttributeNS(EMPTY_NAMESPACE, 'terminate')
        if not self._terminate:
            self.__dict__['_terminate'] = 'no'
        self.__dict__['_nss'] = xml.dom.ext.GetAllNs(self)
        return

    def instantiate(self, context, processor):

        origState = context.copy()
        context.setNamespaces(self._nss)
        
        processor.pushResult()
        for child in self.childNodes:
            context = child.instantiate(context, processor)[0]
        result = processor.popResult()
        msg = Conversions.StringValue(result)
        processor.releaseRtf(result)
        if self._terminate == 'yes':
            raise XsltException(Error.STYLESHEET_REQUESTED_TERMINATION, msg)
        else:
            processor.xslMessage(msg)
        context.set(origState)
        return (context,)

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         new_state = (base_state, self._nss, self._terminate)
         return new_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state[0])
        self._nss = state[1]
        self._terminate = state[2]
        return

