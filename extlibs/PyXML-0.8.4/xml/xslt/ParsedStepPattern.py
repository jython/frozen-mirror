########################################################################
#
# File Name:            ParsedStepPattern.py
#
#
"""
Parse class to handle XSLT StepPatterns
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom import Node
from xml.xpath import ParsedToken
from xml.xslt import XsltException, Error

class StepPattern:
    def __init__(self, nodeTest, axisType, parent=None, parentAxis=None):
        self.nodeTest = nodeTest
        self.axisType = axisType
        self.priority = nodeTest.priority
        self.parent = parent
        self.parentAxis = parentAxis

    def getShortcut(self):
        return (self.nodeTest, self.axisType)

    def match(self, context, node, nodeType):
        raise Exception('subclass should override')
        
    def pprint(self, indent=''):
        print indent + str(self)
        self.nodeTest.pprint(indent + '  ')
        self.parent and self.parent.pprint(indent + '  ')

    def __str__(self):
        return '<%s at %x: %s>' % (
            self.__class__.__name__,
            id(self),
            repr(self))

    def __repr__(self):
        st = (self.axisType == Node.ATTRIBUTE_NODE and '@' or '')
        return st + repr(self.nodeTest)

class ParentStepPattern(StepPattern):
    def getShortcut(self):
        return (self, self.axisType)

    def match(self, context, node, axisType):
        # Called when there is another step following
        if self.nodeTest.match(context, node, self.axisType):
            if node.parentNode:
                node = node.parentNode
            elif node.nodeType == Node.ATTRIBUTE_NODE:
                node = node.ownerElement
            return self.parent.match(context, node, self.parentAxis)
        return 0

    def __repr__(self):
        st = '/' + (self.axisType == Node.ATTRIBUTE_NODE and '@' or '')
        return repr(self.parent) + st + repr(self.nodeTest)

class RootParentStepPattern(StepPattern):
    def getShortcut(self):
        return (self, self.axisType)

    def match(self, context, node, axisType):
        if self.nodeTest.match(context, node, axisType):
            return node.parentNode == node.ownerDocument
        return 0

    def __repr__(self):
        prefix = '/' + (self.axisType == Node.ATTRIBUTE_NODE and '@' or '')
        suffix = self.parent and repr(self.parent) or ''
        return prefix + repr(self.nodeTest) + suffix
    
class AncestorStepPattern(StepPattern):
    def getShortcut(self):
        return (self, self.axisType)

    def match(self, context, node, axisType):
        # Called when there is another step following
        if self.nodeTest.match(context, node, self.axisType):
            if node.parentNode:
                node = node.parentNode
            elif node.nodeType == Node.ATTRIBUTE_NODE:
                node = node.ownerElement
            while node:
                if self.parent.match(context, node, self.parentAxis):
                    return 1
                node = node.parentNode
        return 0

    def __repr__(self):
        st = '//' + (self.axisType == Node.ATTRIBUTE_NODE and '@' or '')
        return repr(self.parent) + st + repr(self.nodeTest)
        
class PredicateStepPattern:
    def __init__(self, nodeTest, axisType, predicates):
        self.nodeTest = nodeTest
        self.axisType = axisType
        self.predicates = predicates
        self.priority = 0.5
        
    def getShortcut(self):
        return (self, None)

    def match(self, context, node, axisType):
        if node.parentNode:
            parent = node.parentNode
            node_set = parent.childNodes
        elif node.nodeType == Node.ATTRIBUTE_NODE == self.axisType:
            parent = node.ownerElement
            node_set = parent.attributes.values()
        else:
            # Must be a document, it only matches '/'
            return 0

        # Pass through the NodeTest
        node_set = filter(lambda node,
                                 match=self.nodeTest.match,
                                 context=context,
                                 principalType=self.axisType:
                          match(context, node, principalType),
                          node_set)
        
        # Our axes are forward only
        if node_set:
            original = context.node
            context.node = parent
            node_set = self.predicates.filter(node_set, context, 0)
            context.node = original
        return node in node_set

    def pprint(self, indent=''):
        print indent + '<%s at %x: %s>' % (
            self.__class__.__name__,
            id(self),
            repr(self))
        self.nodeTest.pprint(indent + '  ')
        self.predicates.pprint(indent + '  ')

    def __repr__(self):
        prefix = self.axisType == Node.ATTRIBUTE_NODE and '@' or ''
        return prefix + repr(self.nodeTest) + repr(self.predicates)
