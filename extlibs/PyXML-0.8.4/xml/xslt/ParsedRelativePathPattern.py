########################################################################
#
# File Name:            ParsedRelativePathPattern.py
#
#
"""
Parse class to handle XSLT RelativePathPattern patterns
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom import Node
from xml.xpath import ParsedToken
from xml.xslt import XsltException, Error, XPattern


class RelativePathPattern(ParsedToken.ParsedToken):
    def __init__(self, op, parent, step):
        ParsedToken.ParsedToken.__init__(self, 'RELATIVE_PATH_PATTERN')
        self._op = op
        self._parent = parent
        self._step = step
        self.priority = self._step.priority

    def getShortcut(self):
        return (self, None)

    def pprint(self, indent=''):
        print indent + str(self)
        self._parent.pprint(indent + '  ')
        self._step.pprint(indent + '  ')

    def __str__(self):
        return '<%s(RelativePathPattern) at %x: %s>' % (
            self.__class__.__name__,
            id(self),
            repr(self))

    def __repr__(self):
        return repr(self._parent) + self._op + repr(self._step)

class RelativeParentPattern(RelativePathPattern):
    """RelativePathPattern: RelativePathPattern '/' StepPattern"""
    def __init__(self, parent, step):
        RelativePathPattern.__init__(self, '/', parent, step)

    def match(self, context, node):
        if self._step.match(context, node):
            if node.nodeType == Node.ATTRIBUTE_NODE:
                node = node.ownerElement
            else:
                node = node.parentNode
            if node:
                return self._parent.match(context, node)
        return 0

class RelativeAncestorPattern(RelativePathPattern):
    """RelativePathPattern: RelativePathPattern '//' StepPattern"""
    def __init__(self, parent, step):
        RelativePathPattern.__init__(self, '//', parent, step)

    def match(self, context, node):
        if self._step.match(context, node):
            if node.nodeType == Node.ATTRIBUTE_NODE:
                node = node.ownerElement
            else:
                node = node.parentNode
            while node:
                if self._parent.match(context, node):
                    return 1
                node = node.parentNode
        return 0
