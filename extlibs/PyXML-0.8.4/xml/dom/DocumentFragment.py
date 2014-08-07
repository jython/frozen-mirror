########################################################################
#
# File Name:            DocumentFragment.py
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom import Node
from FtNode import FtNode

class DocumentFragment(FtNode):
    nodeType = Node.DOCUMENT_FRAGMENT_NODE
    _allowedChildren = [Node.ELEMENT_NODE,
                        Node.PROCESSING_INSTRUCTION_NODE,
                        Node.COMMENT_NODE,
                        Node.TEXT_NODE,
                        Node.CDATA_SECTION_NODE,
                        Node.ENTITY_REFERENCE_NODE]

    def __init__(self, ownerDocument):
        FtNode.__init__(self, ownerDocument)
        self.__dict__['__nodeName'] = '#document-fragment'

    ### Overridden Methods ###

    def __repr__(self):
        return '<DocumentFragment Node at %x: with %d children>' % (
                id(self),
                len(self.childNodes),
                )

    ### Helper Functions For Cloning ###

    def _4dom_clone(self, owner):
        return self.__class__(owner)

    def __getinitargs__(self):
        return (self.ownerDocument,
                )
