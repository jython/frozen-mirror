########################################################################
#
# File Name:            HTMLTableCellElement.py
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import string
from xml.dom.html.HTMLElement import HTMLElement

class HTMLTableCellElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName='TD'):
        HTMLElement.__init__(self, ownerDocument, nodeName)

    ### Attribute Methods ###

    def _get_abbr(self):
        return self.getAttribute('ABBR')

    def _set_abbr(self,abbr):
        self.setAttribute('ABBR',abbr)

    def _get_align(self):
        return string.capitalize(self.getAttribute('ALIGN'))

    def _set_align(self, align):
        self.setAttribute('ALIGN', align)

    def _get_axis(self):
        return self.getAttribute('AXIS')

    def _set_axis(self, axis):
        self.setAttribute('AXIS', axis)

    def _get_bgColor(self):
        return self.getAttribute('BGCOLOR')

    def _set_bgColor(self, color):
        self.setAttribute('BGCOLOR', color)

    def _get_cellIndex(self):
        #We need to find the TR we are in
        if self.parentNode == None:
            return -1
        cells = self.parentNode._get_cells()
        return cells.index(self)

    def _get_ch(self):
        return self.getAttribute('CHAR')

    def _set_ch(self,ch):
        self.setAttribute('CHAR',ch)

    def _get_chOff(self):
        return self.getAttribute('CHAROFF')

    def _set_chOff(self, offset):
        self.setAttribute('CHAROFF', offset)

    def _get_colSpan(self):
        value = self.getAttribute('COLSPAN')
        if value:
            return int(value)
        return 1

    def _set_colSpan(self, span):
        self.setAttribute('COLSPAN',str(span))

    def _get_headers(self):
        return self.getAttribute('HEADERS')

    def _set_headers(self,headers):
        self.setAttribute('HEADERS',headers)

    def _get_height(self):
        return self.getAttribute('HEIGHT')

    def _set_height(self,height):
        self.setAttribute('HEIGHT',height)

    def _get_noWrap(self):
        return self.hasAttribute('NOWRAP')

    def _set_noWrap(self,nowrap):
        if nowrap:
            self.setAttribute('NOWRAP', 'NOWRAP')
        else:
            self.removeAttribute('NOWRAP')

    def _get_rowSpan(self):
        value = self.getAttribute('ROWSPAN')
        if value:
            return int(value)
        return 1

    def _set_rowSpan(self, span):
        self.setAttribute('ROWSPAN', str(span))

    def _get_scope(self):
        return string.capitalize(self.getAttribute('SCOPE'))

    def _set_scope(self, scope):
        self.setAttribute('SCOPE', scope)

    def _get_vAlign(self):
        return string.capitalize(self.getAttribute('VALIGN'))

    def _set_vAlign(self, valign):
        self.setAttribute('VALIGN', valign)

    def _get_width(self):
        return self.getAttribute('WIDTH')

    def _set_width(self, width):
        self.setAttribute('WIDTH', width)

    ### Attribute Access Mappings ###

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy()
    _readComputedAttrs.update ({
         'cellIndex'     : _get_cellIndex,
         'abbr'          : _get_abbr,
         'align'         : _get_align,
         'axis'          : _get_axis,
         'bgColor'       : _get_bgColor,
         'ch'            : _get_ch,
         'chOff'         : _get_chOff,
         'colSpan'       : _get_colSpan,
         'headers'       : _get_headers,
         'height'        : _get_height,
         'noWrap'        : _get_noWrap,
         'rowSpan'       : _get_rowSpan,
         'scope'         : _get_scope,
         'vAlign'        : _get_vAlign,
         'width'         : _get_width,
      })

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy()
    _writeComputedAttrs.update ({
         'abbr'          : _set_abbr,
         'align'         : _set_align,
         'axis'          : _set_axis,
         'bgColor'       : _set_bgColor,
         'ch'            : _set_ch,
         'chOff'         : _set_chOff,
         'colSpan'       : _set_colSpan,
         'headers'       : _set_headers,
         'height'        : _set_height,
         'noWrap'        : _set_noWrap,
         'rowSpan'       : _set_rowSpan,
         'scope'         : _set_scope,
         'vAlign'        : _set_vAlign,
         'width'         : _set_width,
      })

    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                     HTMLElement._readOnlyAttrs + _readComputedAttrs.keys())
