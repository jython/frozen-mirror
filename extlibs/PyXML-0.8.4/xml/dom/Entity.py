########################################################################
#
# File Name:            Entity.py
#
#
"""
Implementation of DOM Level 2 Entity interface
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom import Node
from DOMImplementation import implementation
from FtNode import FtNode

class Entity(FtNode):
    nodeType = Node.ENTITY_NODE
    _allowedChildren = [Node.ELEMENT_NODE,
                        Node.PROCESSING_INSTRUCTION_NODE,
                        Node.COMMENT_NODE,
                        Node.TEXT_NODE,
                        Node.CDATA_SECTION_NODE,
                        Node.ENTITY_REFERENCE_NODE
                        ]

    def __init__(self, ownerDocument, publicId, systemId, notationName):
        FtNode.__init__(self, ownerDocument)
        self.__dict__['__nodeName'] = '#entity'
        self.__dict__['publicId'] = publicId
        self.__dict__['systemId'] = systemId
        self.__dict__['notationName'] = notationName

    ### Attribute Methods ###

    def _get_systemId(self):
        return self.systemId

    def _get_publicId(self):
        return self.publicId

    def _get_notationName(self):
        return self.notationName

   ### Overridden Methods ###

    def __repr__(self):
        return '<Entity Node at %x: Public="%s" System="%s" Notation="%s">' % (
            id(self),
            self.publicId,
            self.systemId,
            self.notationName)

    ### Helper Functions For Cloning ###

    def _4dom_clone(self, owner):
        return self.__class__(owner,
                              self.publicId,
                              self.systemId,
                              self.notationName)

    def __getinitargs__(self):
        return (self.ownerDocument,
                self.publicId,
                self.systemId,
                self.notationName
                )

    ### Attribute Access Mappings ###

    _readComputedAttrs = FtNode._readComputedAttrs.copy()
    _readComputedAttrs.update({'publicId':_get_publicId,
                               'systemId':_get_systemId,
                               'notationName':_get_notationName
                               })


    _writeComputedAttrs = FtNode._writeComputedAttrs.copy()

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                            FtNode._readOnlyAttrs + _readComputedAttrs.keys())
