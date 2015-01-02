########################################################################
#
# File Name:            ForEachElement.py
#
#
"""
Implementation of the XSLT Spec for-each stylesheet element.
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom import EMPTY_NAMESPACE
import xml.dom.Element
import xml.dom.ext
import xml.xslt
from xml.xslt import XsltElement, XsltException, Error, XSL_NAMESPACE
from xml.xpath import XPathParser

class ForEachElement(XsltElement):
    legalAttrs = ('select',)

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE, localName='for-each',
                 prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        self.__dict__['_select'] = self.getAttributeNS(EMPTY_NAMESPACE, 'select')
        self.__dict__['_nss'] = xml.dom.ext.GetAllNs(self)

        if self._select:
            parser = XPathParser.XPathParser()
            self.__dict__['_expr'] = parser.parseExpression(self._select)
        else:
            self.__dict__['_expr'] = None

        self.__dict__['_sortSpecs'] = []
        for child in self.childNodes:
            if (child.namespaceURI, child.localName) == (XSL_NAMESPACE, 'sort'):
                self._sortSpecs.append(child)
        return

    def instantiate(self, context, processor):
        origState = context.copy()
        context.setNamespaces(self._nss)
        if self._select:
            result = self._expr.evaluate(context)
            #Check the result type.  Note: we should really normalize the data typing so that we can throw an error if the result is not a node-set
            if type(result) != type([]):
                raise XsltException(Error.INVALID_FOREACH_SELECT)
        else:
            result = context.node.childNodes
        size = len(result)
        if size > 1 and self._sortSpecs:
            result = self._sortSpecs[0].instantiate(context, processor, result, self._sortSpecs[1:])[1]

        for ctr in range(size):
            node = result[ctr]
            context.setNodePosSize((node,ctr+1,size))
            context.currentNode = node
            for child in self.childNodes:
                child.instantiate(context, processor)[0]

        context.set(origState)
        return (context,)

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         new_state = (base_state, self._nss, self._select, self._sortSpecs, self._expr)
         return new_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state[0])
        self._nss = state[1]
        self._select = state[2]
        self._sortSpecs = state[3]
        self._expr = state[4]
        return

