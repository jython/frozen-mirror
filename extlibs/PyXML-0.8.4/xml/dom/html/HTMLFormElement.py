#
# File Name:            HTMLFormElement.py
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import string
from xml.dom import ext
from xml.dom import implementation
from xml.dom.html.HTMLElement import HTMLElement
from xml.dom.html.HTMLCollection import HTMLCollection

FORM_CHILDREN = ['INPUT',
                 'SELECT',
                 'OPTGROUP',
                 'OPTION',
                 'TEXTAREA',
                 'LABEL',
                 'BUTTON',
                 'FIELDSET',
                 'LEGEND',
                 'OBJECT',
                 'ISINDEX'
                 ]

class HTMLFormElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName='FORM'):
        HTMLElement.__init__(self, ownerDocument, nodeName)

    ### Attribute Methods ###

    def _get_acceptCharset(self):
        return self.getAttribute('ACCEPT-CHARSET')

    def _set_acceptCharset(self,acceptcharset):
        self.setAttribute('ACCEPT-CHARSET',acceptcharset)

    def _get_action(self):
        return self.getAttribute('ACTION')

    def _set_action(self,action):
        self.setAttribute('ACTION',action)

    def _get_elements(self):
        #Make a collection of control elements
        nl = self.getElementsByTagName('*')
        l = []
        for child in nl:
            if child.tagName in FORM_CHILDREN:
                l.append(child)
        return implementation._4dom_createHTMLCollection(l)

    def _get_encType(self):
        return self.getAttribute('ENCTYPE')

    def _set_encType(self,enctype):
        self.setAttribute('ENCTYPE',enctype)

    def _get_length(self):
        return self._get_elements().length

    def _get_method(self):
        return string.capitalize(self.getAttribute('METHOD'))

    def _set_method(self,method):
        self.setAttribute('METHOD',method)

    def _get_name(self):
        return self.getAttribute('NAME')

    def _set_name(self,name):
        self.setAttribute('NAME',name)

    def _get_target(self):
        return self.getAttribute('TARGET')

    def _set_target(self,target):
        self.setAttribute('TARGET',target)

    ### Methods ###

    def reset(self):
        pass

    def submit(self):
        pass

    ### Attribute Access Mappings ###

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy()
    _readComputedAttrs.update ({
        'acceptCharset' : _get_acceptCharset,
        'action'        : _get_action,
        'elements'      : _get_elements,
        'encType'       : _get_encType,
        'length'        : _get_length,
        'method'        : _get_method,
        'name'          : _get_name,
        'target'        : _get_target
        })

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy()
    _writeComputedAttrs.update ({
        'acceptCharset' : _set_acceptCharset,
        'action'        : _set_action,
        'encType'       : _set_encType,
        'method'        : _set_method,
        'name'          : _set_name,
        'target'        : _set_target
        })

    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                     HTMLElement._readOnlyAttrs + _readComputedAttrs.keys())
