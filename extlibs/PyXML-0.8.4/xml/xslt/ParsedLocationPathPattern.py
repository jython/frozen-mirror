########################################################################
#
# File Name:            ParsedLocationPathPattern.py
#
#
"""
Parse class to handle XSLT LocationPathPattern patterns
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom import Node

class RootPattern:
    """LocationPathPattern: '/'"""
    def __init__(self):
        self.priority = 0.5

    def getShortcut(self):
        return (self, None)
    
    def match(self, context, node, axisType):
        # In some DOM implementations, ownerDocument of the root document
        # is the document itself
        if node.ownerDocument == node:
            return 1
        # According to the DOM spec, ownerDocument is None for the root
        return node.ownerDocument is None

    def pprint(self, indent=''):
        print indent + '<%s at %x: %s>' % (
            self.__class__.__name__,
            id(self),
            repr(self))

    def __repr__(self):
        return '/'

class IdKeyPattern:
    """LocationPathPattern: IdKeyPattern"""
    def __init__(self, idKey, nodeTest=None, axisType=None):
        self._idKey = idKey
        self._nodeTest = nodeTest
        self._axisType = axisType
        self.priority = nodeTest and nodeTest.priority or 0.5

    def getShortcut(self):
        return (self, None)

    def match(self, context, node, axisType):
        return (node in self._idKey.evaluate(context))

    def pprint(self, indent=''):
        print indent + '<%s at %x: %s>' % (
            self.__class__.__name__,
            id(self),
            repr(self))
        self._nodeTest and self._nodeTest.pprint(indent + '  ')
        self._idKey.pprint(indent + '  ')

    def __repr__(self):
        return repr(self._idKey)

class IdKeyParentPattern(IdKeyPattern):
    """LocationPathPattern: IdKeyPattern '/' RelativePathPattern"""
    def match(self, context, node, axisType):
        if self._nodeTest.match(context, node, self._axisType):
            return (node.parentNode in self._idKey.evaluate(contenxt))
        return 0
    
    def __repr__(self):
        st = '/' + (self._axisType == Node.ATTRIBUTE_NODE and '@' or '')
        return repr(self._idKey) + st + repr(self._nodeTest)


class IdKeyAncestorPattern(IdKeyPattern):
    """LocationPathPattern: IdKeyPattern '//' RelativePathPattern"""
    def match(self, context, node, axisType):
        if self._nodeTest.match(context, node, self._axisType):
            nodeset = self._idKey.evaluate(context)
            while node:
                if node.parentNode in nodeset:
                    return 1
                node = node.parentNode
        return 0

    def __repr__(self):
        st = '//' + (self._axisType == Node.ATTRIBUTE_NODE and '@' or '')
        return repr(self._idKey) + st + repr(self._nodeTest)
