########################################################################
#
# File Name:            HTMLSelectElement.py
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom import implementation
from xml.dom import IndexSizeErr
from xml.dom.html.HTMLElement import HTMLElement
import string

class HTMLSelectElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName='SELECT'):
        HTMLElement.__init__(self, ownerDocument, nodeName)

    def _get_type(self):
        if self._get_multiple():
            return 'select-multiple'
        return 'select-one'

    def _get_selectedIndex(self):
        options = self._get_options()
        for ctr in range(len(options)):
            node = options.item(ctr)
            if node._get_selected() == 1:
                return ctr
        return -1

    def _set_selectedIndex(self,index):
        options = self._get_options()
        if index < 0 or index >= len(options):
            raise IndexSizeErr()

        for ctr in range(len(options)):
            node = options.item(ctr)
            if ctr == index:
                node._set_selected(1)
            else:
                node._set_selected(0)

    def _get_value(self):
        options = self._get_options()
        node = options.item(self._get_selectedIndex())
        if node.hasAttribute('VALUE'):
            value = node.getAttribute('VALUE')
        elif node.firstChild:
            value = node.firstChild.data
        else:
            value = ''
        return value

    def _set_value(self,value):
        # This doesn't seem to do anything in browsers
        pass

    def _get_length(self):
        return self._get_options()._get_length()

    def _get_options(self):
        children = self.getElementsByTagName('OPTION')
        return implementation._4dom_createHTMLCollection(children)

    def _get_disabled(self):
        if self.getAttributeNode('DISABLED'):
            return 1
        return 0

    def _set_disabled(self,disabled):
        if disabled:
            self.setAttribute('DISABLED', 'DISABLED')
        else:
            self.removeAttribute('DISABLED')

    def _get_multiple(self):
        if self.getAttributeNode('MULTIPLE'):
            return 1
        return 0

    def _set_multiple(self,mult):
        if mult:
            self.setAttribute('MULTIPLE', 'MULTIPLE')
        else:
            self.removeAttribute('MULTIPLE')

    def _get_name(self):
        return self.getAttribute('NAME')

    def _set_name(self,name):
        self.setAttribute('NAME',name)

    def _get_size(self):
        rt = self.getAttribute('SIZE')
        if rt != None:
            return string.atoi(rt)
        return -1

    def _set_size(self,size):
        self.setAttribute('SIZE',str(size))

    def _get_tabIndex(self):
        return string.atoi(self.getAttribute('TABINDEX'))

    def _set_tabIndex(self,tabindex):
        self.setAttribute('TABINDEX',str(tabindex))

    def add(self,newElement,beforeElement):
        self.insertBefore(newElement,beforeElement)

    def remove(self,index):
        if index < 0 or index >= self._get_length:
            return
        hc = self._get_options()
        node = hc.item(index)
        self.removeChild(node)

    def _get_form(self):
        parent = self.parentNode
        while parent:
            if parent.nodeName == "FORM":
                return parent
            parent = parent.parentNode
        return None

    ### Attribute Access Mappings ###

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy()
    _readComputedAttrs.update ({
         'type'          : _get_type,
         'length'        : _get_length,
         'options'       : _get_options,
         'form'          : _get_form,
         'selectedIndex' : _get_selectedIndex,
         'value'         : _get_value,
         'disabled'      : _get_disabled,
         'multiple'      : _get_multiple,
         'name'          : _get_name,
         'size'          : _get_size,
         'tabIndex'      : _get_tabIndex,
      })

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy()
    _writeComputedAttrs.update ({
         'selectedIndex' : _set_selectedIndex,
         'value'         : _set_value,
         'disabled'      : _set_disabled,
         'multiple'      : _set_multiple,
         'name'          : _set_name,
         'size'          : _set_size,
         'tabIndex'      : _set_tabIndex,
      })

    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                     HTMLElement._readOnlyAttrs + _readComputedAttrs.keys())
