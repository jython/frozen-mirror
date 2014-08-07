########################################################################
#
# File Name:            EntityReference.py
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom import Node
from DOMImplementation import implementation
from FtNode import FtNode

class EntityReference(FtNode):
    nodeType = Node.ENTITY_REFERENCE_NODE
    _allowedChildren = [Node.ELEMENT_NODE,
                        Node.PROCESSING_INSTRUCTION_NODE,
                        Node.COMMENT_NODE,
                        Node.TEXT_NODE,
                        Node.CDATA_SECTION_NODE,
                        Node.ENTITY_REFERENCE_NODE,
                        ]

    def __init__(self, ownerDocument, name):
        #Note: the Entity's name is treated as nodeName
        FtNode.__init__(self, ownerDocument)
        self.__dict__['__nodeName'] = name

    ### Helper Functions For Cloning ###

    def _4dom_clone(self, owner):
        return self.__class__(owner, self.nodeName)

    def __getinitargs__(self):
        return (self.ownerDocument,
                self.nodeName
                )

    def __repr__(self):
        return '<EntityReference Node at %x: %s>' % (
            id(self),
            repr(self.nodeName)
            )
