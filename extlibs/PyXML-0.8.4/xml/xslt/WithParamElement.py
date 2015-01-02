########################################################################
#
# File Name:            WithParamElement.py
#
#
"""
Implementation of the XSLT Spec with-param stylesheet element.
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import xml.dom.ext
import xml.dom.Element
import xml.xslt
from xml.xslt import XsltElement, XsltException, Error
from xml.xpath import CoreFunctions
from xml.xpath import Util
from xml.xpath import XPathParser
from xml.dom import EMPTY_NAMESPACE

class WithParamElement(XsltElement):
    legalAttrs = ('select', 'name')

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE, localName='with-param', prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        self.__dict__['_nss'] = xml.dom.ext.GetAllNs(self)
        name_attr = self.getAttributeNS(EMPTY_NAMESPACE, 'name')
        split_name = Util.ExpandQName(
            name_attr,
            namespaces=self._nss
            )
        self.__dict__['_name'] = split_name
        select = self.getAttributeNS(EMPTY_NAMESPACE, 'select')
        if select:
            parser = XPathParser.XPathParser()
            self.__dict__['_expr'] = parser.parseExpression(select)
        else:
            self.__dict__['_expr'] = None
        return

    def instantiate(self, context, processor):
        #original = context.processorNss
        original = context.copy()
        
        #origNss = context.processorNss
        context.processorNss = self._nss
        
        if self._expr:
            result = self._expr.evaluate(context)
        else:
            processor.pushResult()
            for child in self.childNodes:
                context = child.instantiate(context, processor)[0]
            result = processor.popResult()
            context.rtfs.append(result)

        #context.processorNss = origNss
        context.set(original)

        return (context, (self._name, result))

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix, self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         new_state = (base_state, self._nss, self._name, self._expr)
         return new_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state[0])
        self._nss = state[1]
        self._name = state[2]
        self._expr = state[3]
        return

