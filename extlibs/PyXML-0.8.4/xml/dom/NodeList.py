########################################################################
#
# File Name:            NodeList.py
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import UserList

from xml.dom import NoModificationAllowedErr

class NodeList(UserList.UserList):
    def __init__(self, list=None):
        UserList.UserList.__init__(self, list)
        return

    ### Attribute Access Methods ###

    def __getattr__(self, name):
        if name == 'length':
            return len(self)
        #Pass-through
        return getattr(NodeList, name)

    def __setattr__(self, name, value):
        if name == 'length':
            raise NoModificationAllowedErr()
        #Pass-through
        self.__dict__[name] = value

    ### Attribute Methods ###

    def _get_length(self):
        return len(self)

    ### Methods ###

    def item(self, index):
        if 0 <= index < len(self):
            return self[int(index)]
        return None

    #Not defined in the standard
    def contains(self, node):
        return node in self

    def __repr__(self):
        st = "<NodeList at %x: [" % id(self)
        if len(self):
            for i in self[:-1]:
                st = st + repr(i) + ', '
            st = st + repr(self[-1])
        st = st + ']>'
        return st
