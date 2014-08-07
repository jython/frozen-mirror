########################################################################
#
# File Name:            ProcessingInstructionElement.py
#
#
"""
Implementation of the XSLT Spec processing-instruction stylesheet element.
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom import EMPTY_NAMESPACE
import xml.dom.ext
import xml.dom.Element
from xml.xslt import XsltElement, XsltException, Error, AttributeValueTemplate
from xml.xpath import Conversions


class ProcessingInstructionElement(XsltElement):
    legalAttrs = ('name',)

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE, localName='processing-instructions', prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        self.__dict__['_target'] = AttributeValueTemplate.AttributeValueTemplate(self.getAttributeNS(EMPTY_NAMESPACE, 'name'))
        self.__dict__['_nss'] = xml.dom.ext.GetAllNs(self)
        return

    def instantiate(self, context, processor):

        origState = context.copy()
        context.setNamespaces(self._nss)

        target = self._target.evaluate(context)

        #FIXME: Add error checking of child nodes
        processor.pushResult()
        for child in self.childNodes:
            context = child.instantiate(context, processor)[0]

        result = processor.popResult()

        processor.writers[-1].processingInstruction(target, Conversions.StringValue(result))
        processor.releaseRtf(result)

        context.set(origState)
        
        return (context,)

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         new_state = (base_state, self._nss, self._target)
         return new_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state[0])
        self._nss = state[1]
        self._target = state[2]
        return

