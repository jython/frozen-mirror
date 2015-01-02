########################################################################
#
# File Name:            ApplyTemplatesElement.py
#
#
"""
Implementation of the XSLT Spec apply-templates stylesheet element.
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 FourThought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom import EMPTY_NAMESPACE
import xml.dom.Element
import xml.dom.ext
import xml.xslt
from xml.xslt import XsltElement, XSL_NAMESPACE, XsltException, Error
from xml.xpath import XPathParser
from xml.xpath import Util, g_xpathRecognizedNodes

class ApplyTemplatesElement(XsltElement):

    legalAttrs = ['select', 'mode']

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE,
                 localName='apply-templates', prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):

        self.__dict__['_nss'] = xml.dom.ext.GetAllNs(self)
        mode_attr = self.getAttributeNS(EMPTY_NAMESPACE, 'mode')
        if mode_attr == '':
            self.__dict__['_mode'] = None
        else:
            split_name = Util.ExpandQName(
                mode_attr,
                namespaces=self._nss
                )
            self.__dict__['_mode'] = split_name



        select = self.getAttributeNS(EMPTY_NAMESPACE, 'select')
        if select:
            parser = XPathParser.XPathParser()
            self.__dict__['_expr'] = parser.parseExpression(select)
        else:
            self.__dict__['_expr'] = None

        self.__dict__['_sortSpecs'] = []
        self.__dict__['_params'] = []
        for child in self.childNodes:
            #All children should be sort and with-param
            if child.namespaceURI == XSL_NAMESPACE:
                if child.localName == 'sort':
                    self._sortSpecs.append(child)
                elif child.localName == 'with-param':
                    self._params.append(child)
                else:
                    raise XsltException(Error.ILLEGAL_APPLYTEMPLATE_CHILD)
            else:
                raise XsltException(Error.ILLEGAL_APPLYTEMPLATE_CHILD)
        return

    def instantiate(self, context, processor):

        origState = context.copy()
        context.setNamespaces(self._nss)


        params = {}

        mode = self._instantiateMode(context)

        for param in self._params:
            (name, value) = param.instantiate(context, processor)[1]
            params[name] = value

        if self._expr:
            node_set = self._expr.evaluate(context)
        else:
            node_set = context.node.childNodes

        size = len(node_set)
        if size > 1 and len(self._sortSpecs):
            node_set = self._sortSpecs[0].instantiate(context, processor, node_set, self._sortSpecs[1:])[1]

        pos = 1
        for node in node_set:
            context.setNodePosSize((node,pos,size))
            processor.applyTemplates(context, mode, params)
            pos = pos + 1

        context.set(origState)

        return (context,)

    def _instantiateMode(self,context):
        return self._mode

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         new_state = (base_state, self._nss, self._sortSpecs, self._params,self._expr,self._mode)
         return new_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state[0])
        self._nss = state[1]
        self._sortSpecs = state[2]
        self._params = state[3]
        self._expr = state[4]
        self._mode = state[5]
        return

