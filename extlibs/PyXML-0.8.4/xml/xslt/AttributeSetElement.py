########################################################################
#
# File Name:            AttributeSetElement.py
#
#
"""
Implementation of the XSLT Spec attribute-set stylesheet element.
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 FourThought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import string
from xml.dom import EMPTY_NAMESPACE
import xml.dom.Element
import xml.dom.ext
import xml.xslt
from xml.xslt import XsltElement, XsltException, Error
from xml.xpath import Util

class AttributeSetElement(XsltElement):
    legalAttrs = ['name', 'use-attribute-sets']

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE,
                 localName='attribute-set', prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        self.__dict__['_name'] = self.getAttributeNS(EMPTY_NAMESPACE, 'name')
        if not self._name:
            raise XsltException(Error.ATTRIBUTESET_REQUIRES_NAME)
        self.__dict__['_useAttributeSets'] = string.splitfields(self.getAttributeNS(EMPTY_NAMESPACE, 'use-attribute-sets'))
        self.__dict__['_varBindings'] = {}
        self.__dict__['_nss'] = xml.dom.ext.GetAllNs(self)

        #Check that all children are attribute instructions
        for child in self.childNodes:
            if (child.namespaceURI, child.localName) != (xml.xslt.XSL_NAMESPACE, 'attribute'):
                raise XsltException(Error.ILLEGAL_ATTRIBUTESET_CHILD)
        return

    def instantiate(self, context, processor):
        origState = context.copy()
        context.setNamespaces(self._nss)        
        split_name = Util.ExpandQName(self._name, namespaces=self._nss)
        processor.attributeSets[split_name] = self
        self._varBindings = context.varBindings

        context.set(origState)

        return (context,)

    def use(self, context, processor, used=None):
        if used is None:
            used = []
        origState = context.copy()
        context.varBindings = self._varBindings
        for attr_set_name in self._useAttributeSets:
            split_name = Util.ExpandQName(attr_set_name, namespaces=context.processorNss)
            try:
                attr_set = processor.attributeSets[split_name]
            except KeyError:
                raise XsltException(Error.UNDEFINED_ATTRIBUTE_SET, attr_set_name)
            attr_set.use(context, processor)
        for child in self.childNodes:
            context = child.instantiate(context, processor)[0]
        context.set(origState)
        return context

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         new_state = (base_state, self._nss, self._name,
                      self._useAttributeSets, self._varBindings)
         return new_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state[0])
        self._nss = state[1]
        self._name = state[2]
        self._useAttributeSets = state[3]
        self._varBindings = state[4]
        return

