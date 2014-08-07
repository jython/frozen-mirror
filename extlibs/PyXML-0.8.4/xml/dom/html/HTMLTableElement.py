########################################################################
#
# File Name:            HTMLTableElement.py
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom.html.HTMLElement import HTMLElement
from xml.dom import IndexSizeErr
from xml.dom import implementation
from xml.dom.NodeFilter import NodeFilter
import string

class HTMLTableElement(HTMLElement):
    """
    Operations follow the DOM spec, and the 4.0 DTD for TABLE
    <!ELEMENT TABLE (CAPTION?, (COL*|COLGROUP*), THEAD?, TFOOT?, TBODY+)>
    """
    def __init__(self, ownerDocument, nodeName='TABLE'):
        HTMLElement.__init__(self, ownerDocument, nodeName)

    ### Attribute Methods ###

    def _get_align(self):
        return string.capitalize(self.getAttribute('ALIGN'))

    def _set_align(self,align):
        self.setAttribute('ALIGN',align)

    def _get_bgColor(self):
        return self.getAttribute('BGCOLOR')

    def _set_bgColor(self,bgcolor):
        self.setAttribute('BGCOLOR',bgcolor)

    def _get_border(self):
        return self.getAttribute('BORDER')

    def _set_border(self,border):
        self.setAttribute('BORDER',border)

    def _get_caption(self):
        nl = self.getElementsByTagName('CAPTION')
        if len(nl):
            return nl[0]
        return None

    def _set_caption(self,capt):
        nl = self.getElementsByTagName('CAPTION')
        if len(nl):
            self.replaceChild(capt, nl[0])
        else:
            self.insertBefore(capt, self.firstChild)

    def _get_cellPadding(self):
        return self.getAttribute('CELLPADDING')

    def _set_cellPadding(self,cellpadding):
        self.setAttribute('CELLPADDING',cellpadding)

    def _get_cellSpacing(self):
        return self.getAttribute('CELLSPACING')

    def _set_cellSpacing(self,cellspacing):
        self.setAttribute('CELLSPACING',cellspacing)

    def _get_frame(self):
        return string.capitalize(self.getAttribute('FRAME'))

    def _set_frame(self,frame):
        self.setAttribute('FRAME',frame)

    def _get_rows(self):
        rows = []
        tHead = self._get_tHead()
        if tHead:
            rows.extend(list(tHead._get_rows()))
        tFoot = self._get_tFoot()
        if tFoot:
            rows.extend(list(tFoot._get_rows()))
        for tb in self._get_tBodies():
            rows.extend(list(tb._get_rows()))
        return implementation._4dom_createHTMLCollection(rows)

    def _get_rules(self):
        return string.capitalize(self.getAttribute('RULES'))

    def _set_rules(self,rules):
        self.setAttribute('RULES',rules)

    def _get_summary(self):
        return self.getAttribute('SUMMARY')

    def _set_summary(self,summary):
        self.setAttribute('SUMMARY',summary)

    def _get_tBodies(self):
        bodies = []
        for child in self.childNodes:
            if child.nodeName == 'TBODY':
                bodies.append(child)
        return implementation._4dom_createHTMLCollection(bodies)

    def _get_tFoot(self):
        for child in self.childNodes:
            if child.nodeName == 'TFOOT':
                return child
        return None

    def _set_tFoot(self, newFooter):
        oldFooter = self._get_tFoot()
        if not oldFooter:
            # TFoot goes after THead
            iter = self.ownerDocument.createNodeIterator(self.firstChild,
                                                         NodeFilter.SHOW_ELEMENT,
                                                         None, 0)
            ref = None
            node = iter.nextNode()
            while not ref and node:
                tagName = node.tagName
                if tagName == 'THEAD':
                    ref = iter.nextNode()
                elif tagName == 'TBODY':
                    ref = node
                node = iter.nextNode()
            self.insertBefore(newFooter, ref)
        else:
            self.replaceChild(newFooter, oldFooter)

    def _get_tHead(self):
        for child in self.childNodes:
            if child.nodeName == 'THEAD':
                return child
        return None

    def _set_tHead(self, newHead):
        oldHead = self._get_tHead()
        if oldHead:
            self.replaceChild(newHead, oldHead)
        else:
            # We need to put the new Thead in the correct spot
            # Look for a TFOOT or a TBODY
            iter = self.ownerDocument.createNodeIterator(self.firstChild,
                                                         NodeFilter.SHOW_ELEMENT,
                                                         None, 0)
            ref = None
            node = iter.nextNode()
            while not ref and node:
                tagName = node.tagName
                if tagName == 'TFOOT':
                    ref = node
                elif tagName == 'TBODY':
                    ref = node
                elif tagName in ['COL','COLGROUP']:
                    node = iter.nextNode()
                    while node.tagName == tagName:
                        node = iter.nextNode()
                    ref = node
                elif tagName == 'CAPTION':
                    ref = iter.nextNode()
                node = iter.nextNode()
            self.insertBefore(newHead, ref)

    def _get_width(self):
        return self.getAttribute('WIDTH')

    def _set_width(self,width):
        self.setAttribute('WIDTH',width)

    ### Methods ###

    def createCaption(self):
        #Create a new CAPTION if one does not exist
        caption = self._get_caption()
        if not caption:
            caption = self.ownerDocument.createElement('CAPTION')
            self._set_caption(caption)
        return caption

    def createTHead(self):
        #Create a new THEAD if one does not exist
        thead = self._get_tHead()
        if not thead:
            thead = self.ownerDocument.createElement('THEAD')
            self._set_tHead(thead)
        return thead

    def createTFoot(self):
        #Create a new TFOOT if one does not exist
        tfoot = self._get_tFoot()
        if not tfoot:
            tfoot = self.ownerDocument.createElement('TFOOT')
            self._set_tFoot(tfoot)
        return tfoot

    def deleteCaption(self):
        caption = self._get_caption()
        if caption:
            self.removeChild(caption)

    def deleteRow(self,index):
        rows = self._get_rows()
        if index < 0 or index >= len(rows):
            raise IndexSizeErr()
        rows[index].parentNode.removeChild(rows[index])

    def deleteTHead(self):
        thead = self._get_tHead()
        if thead != None:
            self.removeChild(thead)

    def deleteTFoot(self):
        tfoot = self._get_tFoot()
        if tfoot:
            self.removeChild(tfoot)

    def insertRow(self,index):
        rows = self._get_rows()
        if index < 0 or index > len(rows):
            raise IndexSizeErr()
        newRow = self.ownerDocument.createElement('TR')
        if not rows:
            # An empty table, create a body in which to insert the row
            body = self.ownerDocument.createElement('TBODY')
            # The body is the last element according to DTD
            self.appendChild(body)
            parent = body
            ref = None
        elif index == len(rows):
            parent = rows[-1].parentNode
            ref = None
        else:
            ref = rows[index]
            parent = ref.parentNode
        return parent.insertBefore(newRow, ref)

    ### Attribute Access Mappings ###

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy()
    _readComputedAttrs.update ({
         'rows'          : _get_rows,
         'tBodies'       : _get_tBodies,
         'caption'       : _get_caption,
         'tHead'         : _get_tHead,
         'tFoot'         : _get_tFoot,
         'align'         : _get_align,
         'bgColor'       : _get_bgColor,
         'border'        : _get_border,
         'cellPadding'   : _get_cellPadding,
         'cellSpacing'   : _get_cellSpacing,
         'frame'         : _get_frame,
         'rules'         : _get_rules,
         'summary'       : _get_summary,
         'width'         : _get_width,
      })

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy()
    _writeComputedAttrs.update ({
         'caption'       : _set_caption,
         'tHead'         : _set_tHead,
         'tFoot'         : _set_tFoot,
         'align'         : _set_align,
         'bgColor'       : _set_bgColor,
         'border'        : _set_border,
         'cellPadding'   : _set_cellPadding,
         'cellSpacing'   : _set_cellSpacing,
         'frame'         : _set_frame,
         'rules'         : _set_rules,
         'summary'       : _set_summary,
         'width'         : _set_width,
      })

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                     HTMLElement._readOnlyAttrs + _readComputedAttrs.keys())
