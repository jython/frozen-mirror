########################################################################
#
# File Name:            HTMLMapElement.py
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom.html.HTMLElement import HTMLElement
from xml.dom import implementation

class HTMLMapElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName='MAP'):
        HTMLElement.__init__(self, ownerDocument, nodeName)

    ### Attribute Methods ###

    def _get_areas(self):
        rt =  self.getElementsByTagName('AREA')
        return implementation._4dom_createHTMLCollection(rt)

    def _get_name(self):
        return self.getAttribute('NAME')

    def _set_name(self,name):
        self.setAttribute('NAME',name)

    ### Attribute Access Mappings ###

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy()
    _readComputedAttrs.update ({
        'areas' : _get_areas,
        'name'  : _get_name
        })

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy()
    _writeComputedAttrs.update ({
        'name'  : _set_name
        })

    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                            HTMLElement._readOnlyAttrs + _readComputedAttrs.keys())
