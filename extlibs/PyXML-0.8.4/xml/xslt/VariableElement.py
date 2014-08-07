########################################################################
#
# File Name:            VariableElement.py
#
#
"""
Implementation of the XSLT Spec variable stylesheet element.
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom import EMPTY_NAMESPACE
import xml.dom.ext
import xml.dom.Element
import xml.xslt
from xml.xslt import XsltElement, XsltException, Error
from xml.xpath import CoreFunctions, Util
from xml.xpath import XPathParser

class VariableElement(XsltElement):
    legalAttrs = ('name', 'select')

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE, localName='variable', prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)
        return

    def setup(self):
        self._nss = xml.dom.ext.GetAllNs(self)
        name_attr = self.getAttributeNS(EMPTY_NAMESPACE, 'name')
        split_name = Util.ExpandQName(
            name_attr,
            namespaces=self._nss
            )
        self._name = split_name
        self._select = self.getAttributeNS(EMPTY_NAMESPACE, 'select')
        if self._select:
            parser = XPathParser.XPathParser()
            self._expr = parser.parseExpression(self._select)
        else:
            self._expr = None
        return

    def instantiate(self, context, processor):
        #Note all we want to do is change the varBindings
        origState = context.copy()
        context.setNamespaces(self._nss)
        text = ''
        if self._select:
            result = self._expr.evaluate(context)
        else:
            processor.pushResult()
            for child in self.childNodes:
                context = child.instantiate(context, processor)[0]
            result = processor.popResult()
            context.rtfs.append(result)

        context.set(origState)
        context.varBindings[self._name] = result

        return (context,)

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix, self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         new_state = (base_state, self._nss, self._name, self._select, self._expr)
         return new_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state[0])
        self._nss = state[1]
        self._name = state[2]
        self._select = state[3]
        self._expr = state[4]
        return

