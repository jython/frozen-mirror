########################################################################
#
# File Name:            IfElement.py
#
#
"""
Implementation of the XSLT Spec if instruction
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom import EMPTY_NAMESPACE
import xml.dom.ext
import xml.dom.Element
import xml.xslt
from xml.xslt import XsltElement, XSL_NAMESPACE
from xml.xpath import CoreFunctions, Conversions
from xml.xpath import XPathParser

class IfElement(XsltElement):
    legalAttrs = ('test',)

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE, localName='if',
                 prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        parser = XPathParser.XPathParser()
        self.__dict__['_test'] = self.getAttributeNS(EMPTY_NAMESPACE, 'test')
        self.__dict__['_nss'] = xml.dom.ext.GetAllNs(self)
        self.__dict__['_expr'] = parser.parseExpression(self._test)
        self.__dict__['_elements'] = []
        for child in self.childNodes:
            if (child.namespaceURI == XSL_NAMESPACE and
                child.localName in ['call-template', 'if', 'choose']):
                self.__dict__['_elements'].append((1,child))
            else:
                self.__dict__['_elements'].append((0,child))
        return

    def instantiate(self, context, processor, new_level=1):
        origState = context.copy()
        context.setNamespaces(self._nss)
        
        rec_tpl_params = None
        result = self._expr.evaluate(context)
        test = Conversions.BooleanValue(result)
        if test:
            for (recurse,child) in self._elements:
                if recurse:
                    context, rec_tpl_params = child.instantiate(context, processor, new_level)
                else:
                    context = child.instantiate(context, processor)[0]

        context.set(origState)
        return (context, rec_tpl_params)

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         new_state = (base_state, self._nss, self._test, self._expr,
                      self._elements)
         return new_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state[0])
        self._nss = state[1]
        self._test = state[2]
        self._expr = state[3]
        self._elements = state[4]
        return

