########################################################################
#
# File Name:            HTMLTableSectionElement.py
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import string
from xml.dom import implementation
from xml.dom.html.HTMLElement import HTMLElement
from xml.dom import IndexSizeErr

class HTMLTableSectionElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName):
        HTMLElement.__init__(self, ownerDocument, nodeName)

    ### Attribute Methods ###

    def _get_align(self):
        return string.capitalize(self.getAttribute('ALIGN'))

    def _set_align(self,align):
        self.setAttribute('ALIGN',align)

    def _get_ch(self):
        return self.getAttribute('CHAR')

    def _set_ch(self,char):
        self.setAttribute('CHAR',char)

    def _get_chOff(self):
        return self.getAttribute('CHAROFF')

    def _set_chOff(self,offset):
        self.setAttribute('CHAROFF',offset)

    def _get_rows(self):
        rows = []
        for child in self.childNodes:
            if child.tagName == 'TR':
                rows.append(child)
        return implementation._4dom_createHTMLCollection(rows)

    def _get_vAlign(self):
        return string.capitalize(self.getAttribute('VALIGN'))

    def _set_vAlign(self,valign):
        self.setAttribute('VALIGN',valign)

    ### Methods ###

    def deleteRow(self,index):
        rows = self._get_rows()
        if index < 0 or index > len(rows):
            raise IndexSizeErr()
        rows[index].parentNode.removeChild(rows[index])

    def insertRow(self,index):
        rows = self._get_rows()
        if index < 0 or index > len(rows):
            raise IndexSizeErr()
        rows = self._get_rows()
        newRow = self.ownerDocument.createElement('TR')
        if index == len(rows):
            ref = None
        else:
            ref = rows[index]
        return self.insertBefore(newRow, ref)

    ### Attribute Access Mappings ###

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy()
    _readComputedAttrs.update ({
         'rows'          : _get_rows,
         'align'         : _get_align,
         'ch'            : _get_ch,
         'chOff'         : _get_chOff,
         'vAlign'        : _get_vAlign,
      })

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy()
    _writeComputedAttrs.update ({
         'align'         : _set_align,
         'ch'            : _set_ch,
         'chOff'         : _set_chOff,
         'vAlign'        : _set_vAlign,
      })

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                     HTMLElement._readOnlyAttrs + _readComputedAttrs.keys())
