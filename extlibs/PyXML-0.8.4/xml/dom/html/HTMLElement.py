########################################################################
#
# File Name:            HTMLElement.py
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom.Element import Element
from xml.dom import EMPTY_NAMESPACE, EMPTY_PREFIX
import string

class HTMLElement(Element):

    def __init__(self, ownerDocument, nodeName):
        tagName = string.upper(nodeName)
        Element.__init__(self, ownerDocument, tagName,
                         EMPTY_NAMESPACE, EMPTY_PREFIX,tagName)

    ### Attribute Methods ###

    def _get_id(self):
        return self.getAttribute('ID')

    def _set_id(self,ID):
        self.setAttribute('ID',ID)

    def _get_title(self):
        return self.getAttribute('TITLE')

    def _set_title(self,title):
        self.setAttribute('TITLE',title)

    def _get_lang(self):
        return self.getAttribute('LANG')

    def _set_lang(self,lang):
        self.setAttribute('LANG',lang)

    def _get_dir(self):
        return self.getAttribute('DIR')

    def _set_dir(self,dir):
        self.setAttribute('DIR',dir)

    def _get_className(self):
        return self.getAttribute('CLASSNAME')

    def _set_className(self,className):
        self.setAttribute('CLASSNAME',className)

    ### Overridden Methods ###

    def getAttribute(self, name):
        attr = self.attributes.getNamedItem(string.upper(name))
        return attr and attr.value or ''

    def getAttributeNode(self, name):
        return self.attributes.getNamedItem(string.upper(name))

    def getElementsByTagName(self, tagName):
        return Element.getElementsByTagName(self, string.upper(tagName))

    def hasAttribute(self, name):
        return self.attributes.getNamedItem(string.upper(name)) is not None

    def removeAttribute(self, name):
        attr = self.attributes.getNamedItem(string.upper(name))
        attr and self.removeAttributeNode(attr)

    def setAttribute(self, name, value):
        Element.setAttribute(self, string.upper(name), value)

    def _4dom_validateString(self, value):
        return value

    ### Helper Functions For Cloning ###

    def _4dom_clone(self, owner):
        e = self.__class__(owner,
                           self.tagName)
        for attr in self.attributes:
            clone = attr._4dom_clone(owner)
            if clone.localName is None:
                e.attributes.setNamedItem(clone)
            else:
                e.attributes.setNamedItemNS(clone)
            clone._4dom_setOwnerElement(self)
        return e

    def __getinitargs__(self):
        return (self.ownerDocument,
            self.tagName
        )

    ### Attribute Access Mappings ###

    _readComputedAttrs = Element._readComputedAttrs.copy()
    _readComputedAttrs.update ({
         'id'            : _get_id,
         'title'         : _get_title,
         'lang'          : _get_lang,
         'dir'           : _get_dir,
         'className'     : _get_className,
      })

    _writeComputedAttrs = Element._writeComputedAttrs.copy()
    _writeComputedAttrs.update ({
         'id'            : _set_id,
         'title'         : _set_title,
         'lang'          : _set_lang,
         'dir'           : _set_dir,
         'className'     : _set_className,
      })

    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                            Element._readOnlyAttrs + _readComputedAttrs.keys())
