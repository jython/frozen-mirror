########################################################################
#
# File Name:            ChooseElement.py
#
#
"""
Implementation of the XSLT Spec choose instruction
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 FourThought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import xml.dom.ext
from xml.xslt import XSL_NAMESPACE
from xml.xslt import XsltElement, XsltException, Error
from xml.xslt.WhenElement import WhenElement
from xml.xslt.OtherwiseElement import OtherwiseElement
from xml.xpath import CoreFunctions
from xml.dom import Node

class ChooseElement(XsltElement):
    legalAttrs = ()

    def __init__(self, doc, uri=XSL_NAMESPACE, localName='choose',
                 prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        self.__dict__['_nss'] = xml.dom.ext.GetAllNs(self)
        when_other_allowed = 1
        when_found = 0
        for child in self.childNodes:
            if child.nodeType == Node.ELEMENT_NODE:
                if child.namespaceURI == XSL_NAMESPACE:
                    if child.localName == 'when':
                        when_found = 1
                        if not when_other_allowed:
                            raise XsltException(Error.CHOOSE_WHEN_AFTER_OTHERWISE)
                    elif child.localName == 'otherwise':
                        if when_other_allowed:
                            when_other_allowed = 0
                        else:
                            raise XsltException(Error.CHOOSE_MULTIPLE_OTHERWISE)
                    else:
                        raise XsltException(Error.ILLEGAL_CHOOSE_CHILD)
                else:
                    raise XsltException(Error.ILLEGAL_CHOOSE_CHILD)
        if not when_found:
            raise XsltException(Error.CHOOSE_REQUIRES_WHEN_CHILD)
            
        return

    def instantiate(self, context, processor, new_level=1):
        origState = context.copy()
        context.setNamespaces(self._nss)
        
        rec_tpl_params = None
        for child in self.childNodes:
            context, chosen, rec_tpl_params = child.instantiate(context, processor, new_level)
            if chosen: break

        context.set(origState)
        
        return (context, rec_tpl_params)

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         new_state = (base_state, self._nss, )
         return new_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state[0])
        self._nss = state[1]
        return

