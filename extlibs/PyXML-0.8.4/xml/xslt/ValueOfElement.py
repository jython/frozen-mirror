########################################################################
#
# File Name:            ValueOfElement.py
#
#
"""
Implementation of the XSLT Spec import stylesheet element.
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom import EMPTY_NAMESPACE
import xml.dom.ext
import xml.dom.Element
from xml.xslt import XsltElement, XsltException, Error
from xml.xpath import XPathParser, CoreFunctions, Conversions

class ValueOfElement(XsltElement):
    legalAttrs = ('select', 'disable-output-escaping')

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE, localName='value-of', prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        self.__dict__['_select'] = self.getAttributeNS(EMPTY_NAMESPACE, 'select')
        if not self._select:
            raise XsltException(Error.VALUEOF_MISSING_SELECT)
        self.__dict__['_disable_output_escaping'] = self.getAttributeNS(EMPTY_NAMESPACE, 'disable-output-escaping') == 'yes'
        self.__dict__['_nss'] = xml.dom.ext.GetAllNs(self)
        parser = XPathParser.XPathParser()
        self.__dict__['_expr'] = parser.parseExpression(self._select)
        return

    def instantiate(self, context, processor):
        #original = context.processorNss
        original = context.copy()
        context.processorNss = self._nss

        result = self._expr.evaluate(context)
        text = Conversions.StringValue(result)
        if self._disable_output_escaping:
            processor.writers[-1].text(text, escapeOutput=0)
        else:
            processor.writers[-1].text(text)

        #context.processorNss = original
        context.set(original)
        return (context,)

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         new_state = (base_state, self._nss, self._select,
                      self._disable_output_escaping, self._expr)
         return new_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state[0])
        self._nss = state[1]
        self._select = state[2]
        self._disable_output_escaping = state[3]
        self._expr = state[4]
        return

