########################################################################
#
# File Name:            NamedNodeMap.py
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import UserDict

class _NamedNodeMapIter:
    """Iterator class for Python 2.2. The iterator function
    is .next, the stop-iterator element is the iterator itself."""
    def __init__(self,map):
        self.pos = 0
        self.map = map

    def next(self):
        try:
            res = self.map[self.pos]
            self.pos = self.pos + 1
            return res
        except IndexError:
            return self

from xml.dom import Node
from xml.dom import EMPTY_NAMESPACE
from xml.dom import NoModificationAllowedErr
from xml.dom import NotFoundErr
from xml.dom import NotSupportedErr
from xml.dom import WrongDocumentErr
from xml.dom import InuseAttributeErr
from xml.dom import NamespaceErr

class NamedNodeMap(UserDict.UserDict):
    def __init__(self, ownerDoc=None):
        UserDict.UserDict.__init__(self)
        self._ownerDocument = ownerDoc
        self._positions = []

    ### Attribute Access Methods ###

    def __getattr__(self, name):
        if name == 'length':
            return len(self)
        return getattr(NamedNodeMap, name)

    def __setattr__(self, name, value):
        if name == 'length':
            raise NoModificationAllowedErr()
        self.__dict__[name] = value

    ### Attribute Methods ###

    def _get_length(self):
        return len(self)

    ### Methods ###

    def item(self, index):
        if 0 <= index < len(self):
            return self[self._positions[int(index)]]
        return None

    def getNamedItem(self, name):
        try:
            return self[name]
        except KeyError:
            # fall-back to namespace API
            return self.get((EMPTY_NAMESPACE, name))

    def removeNamedItem(self, name):
        old = self.get(name)
        if not old:
            # fall-back to namespace API
            return self.removeNamedItemNS(EMPTY_NAMESPACE, name)
        del self[name]
        self._positions.remove(name)
        return old

    def setNamedItem(self, arg):
        if self._ownerDocument != arg.ownerDocument:
            raise WrongDocumentErr()
        if arg.nodeType == Node.ATTRIBUTE_NODE and arg.ownerElement != None:
            raise InuseAttributeErr()
        name = arg.nodeName
        retval = self.get(name)
        UserDict.UserDict.__setitem__(self, name, arg)
        if not retval:
            retval = self.get((EMPTY_NAMESPACE, name))
            if retval:
                self._positions.remove((EMPTY_NAMESPACE, name))
                del self[(EMPTY_NAMESPACE, name)]
            self._positions.append(name)
        return retval

    def getNamedItemNS(self, namespaceURI, localName):
        if namespaceURI == '':
            raise NamespaceErr("Use None instead of '' for empty namespace")
        return self.get((namespaceURI, localName))

    def setNamedItemNS(self, arg):
        if self._ownerDocument != arg.ownerDocument:
            raise WrongDocumentErr()
        if arg.nodeType == Node.ATTRIBUTE_NODE and arg.ownerElement != None:
            raise InuseAttributeErr()
        if arg.namespaceURI == '':
            raise NamespaceErr("Use None instead of '' for empty namespace")
        name = (arg.namespaceURI, arg.localName)
        retval = self.get(name)
        UserDict.UserDict.__setitem__(self, name, arg)
        if not retval:
            self._positions.append(name)
        return retval

    def removeNamedItemNS(self, namespaceURI, localName):
        if namespaceURI == '':
            raise NamespaceErr("Use None instead of '' for empty namespace")
        name = (namespaceURI, localName)
        old = self.get(name)
        if not old:
            raise NotFoundErr()
        del self[name]
        self._positions.remove(name)
        return old

    ### Overridden Methods ###

    def __getitem__(self, index):
        if type(index) == type(0):
            index = self._positions[index]
        return UserDict.UserDict.__getitem__(self, index)

    def __setitem__(self, index, item):
        raise NotSupportedErr()

    def __iter__(self):
        i = _NamedNodeMapIter(self)
        return iter(i.next, i)

    def __repr__(self):
        st = "<NamedNodeMap at %x: {" % (id(self))
        for k in self.keys():
            st = st + repr(k) + ': ' + repr(self[k]) + ', '
        if len(self):
            st = st[:-2]
        return st + '}>'

    ### Internal Methods ###

    def _4dom_setOwnerDocument(self, newOwner):
        self._ownerDocument = newOwner

    def _4dom_clone(self, owner):
        nnm = self.__class__(owner)
        for item in self:
            if item.localName:
                nnm.setNamedItemNS(item._4dom_clone(owner))
            else:
                nnm.setNamedItem(item._4dom_clone(owner))
        return nnm
