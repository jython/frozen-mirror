########################################################################
#
# File Name:            SortElement.py
#
#
"""
Implementation of the XSLT Spec sort stylesheet element.
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import string
from xml.dom import EMPTY_NAMESPACE
import xml.dom.ext
import xml.dom.Element
import xml.xslt
from xml.xslt import XsltElement, XsltException, Error, AttributeValueTemplate
from xml.xpath import XPathParser
from xml.xpath import Conversions

class SortElement(XsltElement):
    legalAttrs = ('select', 'lang', 'data-type', 'case-order', 'order')

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE, localName='sort', prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        self.__dict__['_select'] = self.getAttributeNS(EMPTY_NAMESPACE, 'select') or '.'
        data_type = self.getAttributeNS(EMPTY_NAMESPACE, 'data-type')
        self.__dict__['_data_type'] = data_type and AttributeValueTemplate.AttributeValueTemplate(data_type) or None
        case_order = self.getAttributeNS(EMPTY_NAMESPACE, 'case-order')
        self.__dict__['_case_order'] = case_order and AttributeValueTemplate.AttributeValueTemplate(case_order) or None
        order = self.getAttributeNS(EMPTY_NAMESPACE, 'order')
        self.__dict__['_order'] = order and AttributeValueTemplate.AttributeValueTemplate(order) or None
        self.__dict__['_nss'] = xml.dom.ext.GetAllNs(self)
        parser = XPathParser.XPathParser()
        self.__dict__['_expr'] = parser.parseExpression(self._select)
        return

    def instantiate(self, context, processor, nodeList=None, specList=None):
  
        if nodeList is None:
            nodeList = []
        if specList is None:
            specList = []

        origState = context.copy()
        context.setNamespaces(self._nss)

        if self._data_type:
            data_type = self._data_type.evaluate(context)
            if data_type not in ['text', 'number']:
                raise XsltException(Error.ILLEGAL_SORT_DATA_TYPE_VALUE)
        else:
            data_type = 'text'
        if self._case_order:
            case_order = self._case_order.evaluate(context)
            if case_order not in ['upper-first', 'lower-first']:
                raise XsltException(Error.ILLEGAL_SORT_CASE_ORDER_VALUE)
        else:
            case_order = 'lower-first'
        if self._order:
            order = self._order.evaluate(context)
            if order not in ['ascending', 'descending']:
                raise XsltException(Error.ILLEGAL_SORT_ORDER_VALUE)
        else:
            order = 'ascending'

        keys = []
        node_dict = {}
        pos = 1
        size = len(nodeList)
        tempState = context.copyNodePosSize()
        for node in nodeList:
            context.setNodePosSize((node,pos,size))
            result = self._expr.evaluate(context)
            key = Conversions.StringValue(result)
            if not key in keys:
                keys.append(key)
            if node_dict.has_key(key):
                node_dict[key].append(node)
            else:
                node_dict[key] = [node]
            pos = pos + 1
            context.setNodePosSize(tempState)

        keys.sort(lambda x, y, o=order, d=data_type, c=case_order: Cmp(x, y, o, d, c))
        sorted_list = []
        for key in keys:
            sub_list = node_dict[key]
            if len(sub_list) > 1 and specList:
                sub_list = specList[0].instantiate(context, processor, sub_list, specList[1:])[1]
            sorted_list = sorted_list + sub_list
        context.set(origState)
        return (context, sorted_list)

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         new_state = (base_state, self._nss, self._select, self._data_type,
                      self._case_order, self._order, self._expr)
         return new_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state[0])
        self._nss = state[1]
        self._select = state[2]
        self._data_type = state[3]
        self._case_order = state[4]
        self._order = state[5]
        self._expr = state[6]
        return


def Cmp(a, b, order, dataType, caseOrder):
    if dataType == 'number':
        a = float(a or 0)
        b = float(b or 0)
    elif caseOrder == 'lower-first':
        if a: a = string.swapcase(a[0])+a[1:]
        if b: b = string.swapcase(b[0])+b[1:]
    if order == 'ascending':
        return cmp(a,b)
    else:
        return cmp(b,a)

