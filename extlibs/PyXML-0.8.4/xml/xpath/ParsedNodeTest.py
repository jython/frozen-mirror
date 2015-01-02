########################################################################
#
# File Name:   ParsedNodeTest.py
#
#
"""
A Parsed Token that represents a node test.
WWW: http://4suite.org/XPATH        e-mail: support@4suite.org

Copyright (c) 2000-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""

import string
from xml.dom import Node,EMPTY_NAMESPACE
from xml.xpath import NamespaceNode
from xml.xpath import NAMESPACE_NODE, RuntimeException
from xml.xpath import g_xpathRecognizedNodes 

def ParsedNameTest(name):
    if name == '*':
        return PrincipalTypeTest()
    index = string.find(name, ':')
    if name[index:] == ':*':
        return LocalNameTest(name[:index])
    elif index >= 0:
        return QualifiedNameTest(name[:index], name[index+1:])
    return NodeNameTest(name)

def ParsedNodeTest(test, literal=None):
    if literal:
        if test != 'processing-instruction':
            raise SyntaxError('Literal only allowed in processing-instruction')
        return ProcessingInstructionNodeTest(literal)
    return g_classMap[test]()

class NodeTestBase:
    def match(self, context, node, principalType=Node.ELEMENT_NODE):
        """
        The principalType is discussed in section [2.3 Node Tests]
        of the XPath 1.0 spec.  Only attribute and namespace axes
        differ from the default of elements.
        """
        return 0

    def pprint(self, indent):
        print indent + str(self)

    def __str__(self):
        return '<%s at %x: %s>' % (
            self.__class__.__name__,
            id(self),
            repr(self),
            )


class NodeTest(NodeTestBase):
    def __init__(self):
        self.priority = -0.5
        
    def match(self, context, node, principalType=Node.ELEMENT_NODE):
        return node.nodeType in g_xpathRecognizedNodes or isinstance(node,NamespaceNode.NamespaceNode)

    def __repr__(self):
        return 'node()'

class CommentNodeTest(NodeTestBase):
    def __init__(self):
        self.priority = -0.5

    def match(self, context, node, principalType=Node.ELEMENT_NODE):
        return node.nodeType == Node.COMMENT_NODE

    def __repr__(self):
        return 'comment()'
    
class TextNodeTest(NodeTestBase):
    def __init__(self):
        self.priority = -0.5

    def match(self, context, node, principalType=Node.ELEMENT_NODE):
        return node.nodeType in [Node.TEXT_NODE, Node.CDATA_SECTION_NODE]

    def __repr__(self):
        return 'text()'

class ProcessingInstructionNodeTest(NodeTestBase):
    def __init__(self, target=None):
        if target:
            self.priority = 0
            if target[0] not in ['"', "'"]:
                raise SyntaxError("Invalid literal: %s" % target)
            self.target = target[1:-1]
        else:
            self.priority = -0.5
            self.target = ''

    def match(self, context, node, principalType=Node.ELEMENT_NODE):
        if node.nodeType != Node.PROCESSING_INSTRUCTION_NODE:
            return 0
        if self.target:
            return self.target == node.target
        return 1

    def __repr__(self):
        if self.target:
            target = repr(self.target)
        else:
            target = ''
        return 'processing-instruction(%s)' % target

# Name tests

class PrincipalTypeTest(NodeTestBase):
    def __init__(self):
        self.priority = -0.5

    def match(self, context, node, principalType=Node.ELEMENT_NODE):
        return node.nodeType == principalType

    def __repr__(self):
        return '*'

class NodeNameTest(NodeTestBase):
    def __init__(self, nodeName):
        self.priority = 0
        self._nodeName = nodeName

    def match(self, context, node, principalType=Node.ELEMENT_NODE):
        if node.nodeType == principalType:
            return node.nodeName == self._nodeName
        return 0

    def __repr__(self):
        return self._nodeName

class LocalNameTest(NodeTestBase):
    def __init__(self, prefix):
        self.priority = -0.25
        self._prefix = prefix
        
    def match(self, context, node, principalType=Node.ELEMENT_NODE):
        if node.nodeType != principalType:
            return 0
        try:
            uri = self._prefix and context.processorNss[self._prefix] or EMPTY_NAMESPACE
        except KeyError:
            raise RuntimeException(RuntimeException.UNDEFINED_PREFIX,
                                   self._prefix)
        return node.namespaceURI == uri

    def __repr__(self):
        return self._prefix + ':*'
    
class QualifiedNameTest(NodeTestBase):
    def __init__(self, prefix, localName):
        self.priority = 0
        self._prefix = prefix
        self._localName = localName

    def match(self, context, node, principalType=Node.ELEMENT_NODE):
        if node.nodeType == principalType:
            if node.localName == self._localName:
                try:
                    return node.namespaceURI == context.processorNss[self._prefix]
                except KeyError:
                    raise RuntimeException(RuntimeException.UNDEFINED_PREFIX,
                                           self._prefix)
        return 0

    def __repr__(self):
        return self._prefix + ':' + self._localName

g_classMap = {
    'node' : NodeTest,
    'comment' : CommentNodeTest,
    'text' : TextNodeTest,
    'processing-instruction' : ProcessingInstructionNodeTest,
    }
             
