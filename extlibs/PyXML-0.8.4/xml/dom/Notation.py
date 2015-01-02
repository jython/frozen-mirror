########################################################################
#
# File Name:            Notation.py
#
#
"""
Implementation of DOM Level 2 Notation interface
WWW: http://4suite.org/4DOM         e-mail: support@4suite.org

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""

from xml.dom import Node
from FtNode import FtNode

class Notation(FtNode):
    nodeType = Node.NOTATION_NODE

    def __init__(self, ownerDocument, publicId, systemId, name):
        FtNode.__init__(self, ownerDocument)
        self.__dict__['__nodeName'] = name
        self.__dict__['publicId'] = publicId
        self.__dict__['systemId'] = systemId

    ### Attribute Methods ###

    def _get_systemId(self):
        return self.systemId

    def _get_publicId(self):
        return self.publicId

    ### Overridden Methods ###

    def __repr__(self):
        return '<Notation Node at %x: PublicId="%s" SystemId="%s" Name="%s">' % (
            id(self),
            self.publicId,
            self.systemId,
            self.nodeName)

    ### Helper Functions For Cloning ###

    def _4dom_clone(self, owner):
        return self.__class__(owner,
                              self.publicId,
                              self.systemId,
                              self.nodeName)

    def __getinitargs__(self):
        return (self.ownerDocument,
                self.publicId,
                self.systemId,
                self.nodeName
                )

    ### Attribute Access Mappings ###

    _readComputedAttrs = FtNode._readComputedAttrs.copy()
    _readComputedAttrs.update({'publicId':_get_publicId,
                               'systemId':_get_systemId
                               })


    _writeComputedAttrs = FtNode._writeComputedAttrs.copy()

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                            FtNode._readOnlyAttrs + _readComputedAttrs.keys())
