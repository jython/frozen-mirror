########################################################################
#
# File Name:            NodeIterator.py
#
#
"""
Node Iterators from DOM Level 2.  Allows "flat" iteration over nodes.
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from NodeFilter import NodeFilter

from xml.dom import NoModificationAllowedErr
from xml.dom import InvalidStateErr

class NodeIterator:

    def __init__(self, root, whatToShow, filter, expandEntityReferences):
        self.__dict__['root'] = root
        self.__dict__['filter'] = filter
        self.__dict__['expandEntityReferences'] = expandEntityReferences
        self.__dict__['whatToShow'] = whatToShow
        self.__dict__['_atStart'] = 1
        self.__dict__['_atEnd'] = 0
        self.__dict__['_current'] = root
        self.__dict__['_nodeStack'] = []
        self.__dict__['_detached'] = 0

    def __setattr__(self, name, value):
        if name in ['root', 'filter', 'expandEntityReferences', 'whatToShow']:
            raise NoModificationAllowedErr()
        self.__dict__[name] = value

    def _get_root(self):
        return self.root

    def _get_filter(self):
        return self.filter

    def _get_expandEntityReferences(self):
        return self.expandEntityReferences

    def _get_whatToShow(self):
        return self.whatToShow

    def nextNode(self):
        if self._detached:
            raise InvalidStateErr()
        next_node = self._advance()
        while (next_node and not (
            self._checkWhatToShow(next_node) and
            self._checkFilter(next_node) == NodeFilter.FILTER_ACCEPT)):
            next_node = self._advance()
        return next_node

    def previousNode(self):
        if self._detached:
            raise InvalidStateErr()
        prev_node = self._regress()
        while (prev_node and not (
            self._checkWhatToShow(prev_node) and
            self._checkFilter(prev_node) == NodeFilter.FILTER_ACCEPT)):
            prev_node = self._regress()
        return prev_node

    def detach(self):
        self._detached = 1

    def _advance(self):
        node = None
        if self._atStart:
            # First time through
            self._atStart = 0
            node = self._current
        elif not self._atEnd:
            current = self._current
            if current.firstChild:
                # Do children first
                node = current.firstChild
            else:
                # Now try the siblings
                while current is not self.root:
                    if current.nextSibling:
                        node = current.nextSibling
                        break
                    # We are at the end of a branch, starting going back up
                    current = current.parentNode
                else:
                    node = None
            if node:
                self._current = node
            else:
                self._atEnd = 1
        return node

    def _regress(self):
        node = None
        if self._atEnd:
            self._atEnd = 0
            node = self._current
        elif not self._atStart:
            current = self._current
            if current is self.root:
                node = None
            elif current.previousSibling:
                node = current.previousSibling
                if node.lastChild:
                    node = node.lastChild
            else:
                node = current.parentNode
            if node:
                self._current = node
            else:
                self._atStart = 1
        return node

    def _checkWhatToShow(self, node):
        show_bit = 1 << (node.nodeType - 1)
        return self.whatToShow & show_bit

    def _checkFilter(self, node):
        if self.filter:
            return self.filter.acceptNode(node)
        else:
            return NodeFilter.FILTER_ACCEPT
