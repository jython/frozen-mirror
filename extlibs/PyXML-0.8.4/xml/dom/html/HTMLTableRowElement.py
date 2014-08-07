########################################################################
#
# File Name:            HTMLTableRowElement.py
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import string
from xml.dom import implementation
from xml.dom import IndexSizeErr
from xml.dom.html.HTMLElement import HTMLElement

class HTMLTableRowElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName='TR'):
        HTMLElement.__init__(self, ownerDocument, nodeName)

    ### Attribute Methods ###

    def _get_align(self):
        return string.capitalize(self.getAttribute('ALIGN'))

    def _set_align(self,align):
        self.setAttribute('ALIGN', align)

    def _get_bgColor(self):
        return self.getAttribute('BGCOLOR')

    def _set_bgColor(self, color):
        self.setAttribute('BGCOLOR', color)

    def _get_cells(self):
        cells = []
        for child in self.childNodes:
            if child.tagName in ['TD','TH']:
                cells.append(child)
        return implementation._4dom_createHTMLCollection(cells)

    def _get_ch(self):
        return self.getAttribute('CHAR')

    def _set_ch(self, ch):
        self.setAttribute('CHAR', ch)

    def _get_chOff(self):
        return self.getAttribute('CHAROFF')

    def _set_chOff(self, offset):
        self.setAttribute('CHAROFF', offset)

    def _get_rowIndex(self):
        #Get our index in the table
        section = self.parentNode
        if section == None:
            return -1
        table = section.parentNode
        if table == None:
            return -1
        rows = table._get_rows()
        return rows.index(self)

    def _get_sectionRowIndex(self):
        section = self.parentNode
        if section == None:
            return -1
        rows = section._get_rows()
        return rows.index(self)

    def _get_vAlign(self):
        return string.capitalize(self.getAttribute('VALIGN'))

    def _set_vAlign(self, valign):
        self.setAttribute('VALIGN', valign)

    ### Methods ###

    def insertCell(self, index):
        cells = self._get_cells()
        if index < 0 or index > len(cells):
            raise IndexSizeErr()
        cell = self.ownerDocument.createElement('TD')
        length = cells.length
        if index == len(cells):
            ref = None
        elif index < len(cells):
            ref = cells[index]
        return self.insertBefore(cell, ref)

    def deleteCell(self,index):
        cells = self._get_cells()
        if index < 0 or index >= len(cells):
            raise IndexSizeErr()
        self.removeChild(cells[index])

    ### Attribute Access Mappings ###

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy()
    _readComputedAttrs.update ({
         'rowIndex'      : _get_rowIndex,
         'sectionRowIndex' : _get_sectionRowIndex,
         'cells'         : _get_cells,
         'align'         : _get_align,
         'bgColor'       : _get_bgColor,
         'ch'            : _get_ch,
         'chOff'         : _get_chOff,
         'vAlign'        : _get_vAlign,
      })

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy()
    _writeComputedAttrs.update ({
         'align'         : _set_align,
         'bgColor'       : _set_bgColor,
         'ch'            : _set_ch,
         'chOff'         : _set_chOff,
         'vAlign'        : _set_vAlign,
      })

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                     HTMLElement._readOnlyAttrs + _readComputedAttrs.keys())
