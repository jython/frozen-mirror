########################################################################
#
# File Name:            AttributeElement.py
#
#
"""
Implementation of the XSLT Spec element stylesheet element.
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999 FourThought LLC, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import cStringIO
from xml.dom import EMPTY_NAMESPACE
import xml.dom.Element
import xml.dom.ext
import xml.xslt
from xml.xslt import XsltElement, XsltException, Error
from xml.xslt.AttributeValueTemplate import AttributeValueTemplate
from xml.xpath import Conversions

#FIXME: Add check for Attribute inside an Element.

class AttributeElement(XsltElement):
    legalAttrs = ('name', 'namespace')

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE,
                 localName='attribute', prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        name = self.getAttributeNS(EMPTY_NAMESPACE, 'name')
        if not name:
            raise XsltException(Error.ATTRIBUTE_MISSING_NAME)
        self._name = AttributeValueTemplate(name)

        namespace = self.getAttributeNS(EMPTY_NAMESPACE, 'namespace')
        self._namespace = AttributeValueTemplate(namespace)

        self._nss = xml.dom.ext.GetAllNs(self)
        return
        
    def instantiate(self, context, processor):

        origState = context.copy()
        context.setNamespaces(self._nss)

        name = self._name.evaluate(context)
        namespace = self._namespace.evaluate(context)
        (prefix, local) = xml.dom.ext.SplitQName(name)
        if not namespace:
            if prefix:
                namespace = context.processorNss[prefix]
        if local == 'xmlns':
            name = prefix
        
        #FIXME: Add error checking of child nodes

        processor.pushResult()
        for child in self.childNodes:
            context = child.instantiate(context, processor)[0]
        rtf = processor.popResult()

        value = Conversions.StringValue(rtf)
        
        processor.writers[-1].attribute(name, value, namespace)
        processor.releaseRtf(rtf)

        context.set(origState)
        
        return (context,)

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix, self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         new_state = (base_state, self._nss, self._name, self._namespace)
         return new_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state[0])
        self._nss = state[1]
        self._name = state[2]
        self._namespace = state[3]
        return

