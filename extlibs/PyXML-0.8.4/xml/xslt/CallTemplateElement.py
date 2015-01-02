########################################################################
#
# File Name:            CallTemplateElement.py
#
#
"""
Implementation of the XSLT Spec call-template stylesheet element.
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom import EMPTY_NAMESPACE
from xml.dom import Node
import xml.dom.ext
import xml.xslt
from xml.xslt import XsltElement, XsltException, Error, XSL_NAMESPACE
from xml.xpath import Util

class CallTemplateElement(XsltElement):
    legalAttrs = ('name', )

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE,
                 localName='call-template', prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        self.__dict__['_nss'] = xml.dom.ext.GetAllNs(self)
        split_name = Util.ExpandQName(
            self.getAttributeNS(EMPTY_NAMESPACE, 'name'),
            namespaces=self._nss
            )
        self.__dict__['_name'] = split_name
        self.__dict__['_tailRecursive'] = "unknown"
        self.__dict__['_params'] = filter(lambda node:
                                          node.nodeType == Node.ELEMENT_NODE,
                                          self.childNodes)
        for child in self.__dict__['_params']:
            if child.nodeType == Node.ELEMENT_NODE:
                if child.namespaceURI == XSL_NAMESPACE:
                    if child.localName != 'with-param':
                        raise XsltException(Error.ILLEGAL_CALLTEMPLATE_CHILD)
                else:
                    raise XsltException(Error.ILLEGAL_CALLTEMPLATE_CHILD)
        return
        
    def instantiate(self, context, processor, new_level=1):

        if self._tailRecursive == 'unknown':
            self.__dict__['_tailRecursive'] = CheckTailRecursion(self, self._name)

        origState = context.copy()
        context.setNamespaces(self._nss)
        
        params = {}
        for child in self._params:
            param = child.instantiate(context, processor)[1]
            params[param[0]] = param[1]

        if self._tailRecursive:
            if not new_level:
                context.set(origState)
                return (context, params)
            while params is not None:
                params = processor.callTemplate(self._name, context, params, 0)
                if params:
                    context.varBindings.update(params)
        else:
            processor.callTemplate(self._name, context, params, 1)

        context.set(origState)
        return (context, None)

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         new_state = (base_state,
                      self._nss,
                      self._name,
                      self._tailRecursive,
                      self._params)
         return new_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state[0])
        self._nss = state[1]
        self._name = state[2]
        self._tailRecursive = state[3]
        self._params = state[4]
        return


def CheckTailRecursion(node, name):
    if node.nextSibling and node.nodeType == Node.ELEMENT_NODE:
        return 0
    p = node.nodeType == Node.ATTRIBUTE_NODE and node.ownerElement or node.parentNode
    if p and p.nodeType == Node.ELEMENT_NODE and p.namespaceURI == XSL_NAMESPACE:
        if p.localName in ['if', 'choose']:
            return CheckTailRecursion(p, name)
        elif p.localName == 'template' and name == p._name:
            return 1
    return 0

