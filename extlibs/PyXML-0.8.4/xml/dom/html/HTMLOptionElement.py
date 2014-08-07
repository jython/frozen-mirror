########################################################################
#
# File Name:            HTMLOptionElement.py
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom.html.HTMLElement import HTMLElement
from xml.dom import Node

class HTMLOptionElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName='OPTION'):
        HTMLElement.__init__(self, ownerDocument, nodeName)

    ### Attribute Methods ###

    def _get_defaultSelected(self):
        return self._get_selected()

    def _set_defaultSelected(self, selected):
        self._set_selected(selected)

    def _get_disabled(self):
        return self.getAttributeNode('DISABLED') and 1 or 0

    def _set_disabled(self,disabled):
        if disabled:
            self.setAttribute('DISABLED', 'DISABLED')
        else:
            self.removeAttribute('DISABLED')

    def _get_form(self):
        parent = self.parentNode
        while parent:
            if parent.nodeName == "FORM":
                return parent
            parent = parent.parentNode
        return None

    def _get_index(self):
        p = self.parentNode
        if p.tagName != 'SELECT':
            return -1
        options = p._get_options()
        try:
            return options.index(self)
        except:
            return -1

    def _get_label(self):
        return self.getAttribute('LABEL')

    def _set_label(self,label):
        self.setAttribute('LABEL',label)

    def _get_selected(self):
        return self.hasAttribute('SELECTED')

    def _set_selected(self, selected):
        if selected:
            self.setAttribute('SELECTED', 'SELECTED')
        else:
            self.removeAttribute('SELECTED')

    def _get_text(self):
        if not self.firstChild:
            return
        if self.firstChild == self.lastChild:
            return self.firstChild.data
        self.normalize()
        text = filter(lambda x: x.nodeType == Node.TEXT_NODE, self.childNodes)
        return text[0].data

    def _set_text(self, value):
        text = None
        for node in self.childNodes:
            if not text and node.nodeType == Node.TEXT_NODE:
                text = node
            else:
                self.removeChild(node)
        if text:
            text.data = value
        else:
            text = self.ownerDocument.createTextNode(value)
            self.appendChild(text)

    def _get_value(self):
        return self.getAttribute('VALUE')

    def _set_value(self,value):
        self.setAttribute('VALUE',value)

    ### Attribute Access Mappings ###

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy()
    _readComputedAttrs.update ({
         'defaultSelected' : _get_defaultSelected,
         'disabled'        : _get_disabled,
         'form'            : _get_form,
         'index'           : _get_index,
         'label'           : _get_label,
         'selected'        : _get_selected,
         'text'            : _get_text,
         'value'           : _get_value,
      })

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy()
    _writeComputedAttrs.update ({
         'defaultSelected' : _set_defaultSelected,
         'disabled'      : _set_disabled,
         'label'         : _set_label,
         'selected'      : _set_selected,
         'value'         : _set_value,
      })

    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                     HTMLElement._readOnlyAttrs + _readComputedAttrs.keys())
