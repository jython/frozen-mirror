########################################################################
#
# File Name:            ElementElement.py
#
#
"""
Implementation of the XSLT Spec element stylesheet element.
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 FourThought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import string
from xml.dom import EMPTY_NAMESPACE
import xml.dom.ext
import xml.dom.Element
import xml.xslt
from xml.xslt import XsltElement, XsltException, Error, AttributeValueTemplate
from xml.xpath import CoreFunctions, Util

class ElementElement(XsltElement):
    legalAttrs = ('name', 'namespace', 'use-attribute-sets')

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE, localName='element',
                 prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        self.__dict__['_name'] = AttributeValueTemplate.AttributeValueTemplate(self.getAttributeNS(EMPTY_NAMESPACE, 'name'))
        self.__dict__['_namespace'] = AttributeValueTemplate.AttributeValueTemplate(self.getAttributeNS(EMPTY_NAMESPACE, 'namespace'))
        self.__dict__['_useAttributeSets'] = string.splitfields(self.getAttributeNS(EMPTY_NAMESPACE, 'use-attribute-sets'))
        self.__dict__['_nss'] = xml.dom.ext.GetAllNs(self)
        return

    def instantiate(self, context, processor):
        origState = context.copy()
        context.setNamespaces(self._nss)
        
        name = self._name.evaluate(context)
        namespace = self._namespace.evaluate(context)
        (prefix, local) = xml.dom.ext.SplitQName(name)
        if not namespace and prefix:
            namespace = context.processorNss[prefix]
        #FIXME: Use proper pysax AttributeList objects
        processor.writers[-1].startElement(name, namespace)
        for attr_set_name in self._useAttributeSets:
            split_name = Util.ExpandQName(attr_set_name, namespaces=context.processorNss)
            try:
                attr_set = processor.attributeSets[split_name]
            except KeyError:
                raise XsltException(Error.UNDEFINED_ATTRIBUTE_SET, attr_set_name)
            attr_set.use(context, processor)
        for child in self.childNodes:
            context = child.instantiate(context, processor)[0]
        processor.writers[-1].endElement(name)

        context.set(origState)

        return (context,)

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         new_state = (base_state, self._nss, self._name,
                      self._namespace, self._useAttributeSets)
         return new_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state[0])
        self._nss = state[1]
        self._name = state[2]
        self._namespace = state[3]
        self._useAttributeSets = state[4]
        return

