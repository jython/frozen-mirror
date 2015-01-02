########################################################################
#
# File Name:            HTMLInputElement.py
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom.html.HTMLElement import HTMLElement
from xml.dom import InvalidAccessErr
import string

class HTMLInputElement(HTMLElement):

    def __init__(self, ownerDocument, nodeName='INPUT'):
        HTMLElement.__init__(self, ownerDocument, nodeName)

    def _get_accept(self):
        return self.getAttribute('ACCEPT')

    def _set_accept(self,accept):
        self.setAttribute('ACCEPT',accept)

    def _get_accessKey(self):
        return self.getAttribute('ACCESSKEY')

    def _set_accessKey(self,accessKey):
        self.setAttribute('ACCESSKEY',accessKey)

    def _get_align(self):
        return string.capitalize(self.getAttribute('ALIGN'))

    def _set_align(self,align):
        self.setAttribute('ALIGN',align)

    def _get_alt(self):
        return self.getAttribute('ALT')

    def _set_alt(self,alt):
        self.setAttribute('ALT',alt)

    def _get_checked(self):
        if self._get_type() in ['Radio', 'Checkbox']:
            return self.hasAttribute('CHECKED')
        else:
            raise InvalidAccessErr()

    def _set_checked(self,checked):
        if self._get_type() in ['Radio','Checkbox']:
            if checked:
                self.setAttribute('CHECKED', 'CHECKED')
            else:
                self.removeAttribute('CHECKED')
        else:
            raise InvalidAccessErr()

    def _get_defaultChecked(self):
        return self._get_checked()

    def _set_defaultChecked(self,checked):
        self._set_checked(checked)

    def _get_defaultValue(self):
        return self._get_value()

    def _set_defaultValue(self,value):
        self._set_value(value)

    def _get_disabled(self):
        return self.hasAttribute('DISABLED')

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

    def _get_maxLength(self):
        if self._get_type() in ['Text','Password']:
            rt = self.getAttribute('MAXLENGTH')
            if rt:
                return int(rt)
        raise InvalidAccessErr()

    def _set_maxLength(self,maxLength):
        if self._get_type() in ['Text','Password']:
            self.setAttribute('MAXLENGTH',str(maxLength))
        else:
            raise InvalidAccessErr()

    def _get_name(self):
        return self.getAttribute('NAME')

    def _set_name(self,name):
        self.setAttribute('NAME',name)

    def _get_readOnly(self):
        if self._get_type() in ['Text','Password']:
            return self.hasAttribute('READONLY')
        raise InvalidAccessErr()

    def _set_readOnly(self,readOnly):
        if self._get_type() in ['Text','Password']:
            if readOnly:
                self.setAttribute('READONLY', 'READONLY')
            else:
                self.removeAttribute('READONLY')
        else:
            raise InvalidAccessErr()

    def _get_size(self):
        return self.getAttribute('SIZE')

    def _set_size(self,size):
        self.setAttribute('SIZE',size)

    def _get_src(self):
        if self._get_type() == 'Image':
            return self.getAttribute('SRC')
        else:
            raise InvalidAccessErr()

    def _set_src(self,src):
        if self._get_type() == 'Image':
            self.setAttribute('SRC',src)
        else:
            raise InvalidAccessErr()

    def _get_tabIndex(self):
        rt = self.getAttribute('TABINDEX')
        if rt:
            return int(rt)
        return -1

    def _set_tabIndex(self,tabIndex):
        self.setAttribute('TABINDEX',str(tabIndex))

    def _get_type(self):
        return string.capitalize(self.getAttribute('TYPE'))

    def _get_useMap(self):
        return self.getAttribute('USEMAP')

    def _set_useMap(self,useMap):
        self.setAttribute('USEMAP',useMap)

    def _get_value(self):
        return self.getAttribute('VALUE')

    def _set_value(self,value):
        self.setAttribute('VALUE',value)

    ### Methods ###

    def blur(self):
        pass

    def click(self):
        pass

    def focus(self):
        pass

    def select(self):
        pass

    ### Attribute Access Mappings ###

    _readComputedAttrs = HTMLElement._readComputedAttrs.copy()
    _readComputedAttrs.update ({
         'accept'         : _get_accept,
         'accessKey'      : _get_accessKey,
         'align'          : _get_align,
         'alt'            : _get_alt,
         'checked'        : _get_checked,
         'defaultChecked' : _get_defaultChecked,
         'defaultValue'   : _get_defaultValue,
         'disabled'       : _get_disabled,
         'form'           : _get_form,
         'maxLength'      : _get_maxLength,
         'name'           : _get_name,
         'readOnly'       : _get_readOnly,
         'size'           : _get_size,
         'src'            : _get_src,
         'tabIndex'       : _get_tabIndex,
         'type'           : _get_type,
         'useMap'         : _get_useMap,
         'value'          : _get_value,
      })

    _writeComputedAttrs = HTMLElement._writeComputedAttrs.copy()
    _writeComputedAttrs.update ({
         'accept'         : _set_accept,
         'accessKey'      : _set_accessKey,
         'align'          : _set_align,
         'alt'            : _set_alt,
         'checked'        : _set_checked,
         'defaultChecked' : _set_defaultChecked,
         'defaultValue'   : _set_defaultValue,
         'disabled'       : _set_disabled,
         'maxLength'      : _set_maxLength,
         'name'           : _set_name,
         'readOnly'       : _set_readOnly,
         'size'           : _set_size,
         'src'            : _set_src,
         'tabIndex'       : _set_tabIndex,
         'useMap'         : _set_useMap,
         'value'          : _set_value,
      })

    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                            HTMLElement._readOnlyAttrs + _readComputedAttrs.keys())
