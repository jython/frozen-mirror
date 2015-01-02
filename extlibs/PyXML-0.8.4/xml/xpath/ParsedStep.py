########################################################################
#
# File Name:   ParsedStep.py
#
#
"""
A Parsed token that represents a step on the result tree.
WWW: http://4suite.org/XPATH        e-mail: support@4suite.org

Copyright (c) 2000-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""

from xml.dom import Node
from xml.xpath import Util
from xml.xpath import NamespaceNode

import sys

class ParsedStep:
    def __init__(self, axis, nodeTest, predicates=None):
        self._axis = axis
        self._nodeTest = nodeTest
        self._predicates = predicates
        return

    def evaluate(self, context):
        """
        Select a set of nodes from the axis, then filter through the node
        test and the predicates.
        """
        (node_set, reverse) = self._axis.select(context, self._nodeTest.match)
        if self._predicates and len(node_set):
            node_set = self._predicates.filter(node_set, context, reverse)
        return node_set
    select = evaluate
    
    def pprint(self, indent=''):
        print indent + str(self)
        self._axis.pprint(indent + '  ')
        self._nodeTest.pprint(indent + '  ')
        self._predicates and self._predicates.pprint(indent + '  ')

    def __str__(self):
        return '<Step at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        result = repr(self._axis) + '::' + repr(self._nodeTest)
        if self._predicates:
            result = result + repr(self._predicates)
        return result
        
class ParsedAbbreviatedStep:
    def __init__(self, parent):
        self.parent = parent

    def evaluate(self, context):
        if self.parent:
            if context.node.nodeType == Node.ATTRIBUTE_NODE:
                return [context.node.ownerElement]
            return context.node.parentNode and [context.node.parentNode] or []
        return [context.node]
    select = evaluate

    def pprint(self, indent=''):
        print indent + str(self)

    def __str__(self):
        return '<AbbreviatedStep at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        return self.parent and '..' or '.'
        
# From the XPath 2.0 Working Draft
# Used by XPointer
class ParsedNodeSetFunction:
    def __init__(self, function, predicates=None):
        self._function = function
        self._predicates = predicates
        return

    def evaluate(self, context):
        """
        Select a set of nodes from the node-set function then filter
        through the predicates.
        """
        node_set = self._function.evaluate(context)
        if type(node_set) != type([]):
            raise SyntaxError('%s does not evaluate to a node-set' %
                              repr(self._function))
        if self._predicates and len(node_set):
            node_set = self._predicates.filter(node_set, context, reverse)
        return node_set
    select = evaluate
    
    def pprint(self, indent=''):
        print indent + str(self)
        self._function.pprint(indent + '  ')
        self._predicates and self._predicates.pprint(indent + '  ')

    def __str__(self):
        return '<Step at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        result = repr(self._function)
        if self._predicates:
            result = result + repr(self._predicates)
        return result
