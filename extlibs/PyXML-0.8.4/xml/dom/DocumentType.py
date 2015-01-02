########################################################################
#
# File Name:            DocumentType.py
#
#
"""
WWW: http://4suite.org/4DOM         e-mail: support@4suite.org

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""

from xml.dom import Node
from DOMImplementation import implementation
from FtNode import FtNode

class DocumentType(FtNode):
    nodeType = Node.DOCUMENT_TYPE_NODE

    def __init__(self, name, entities, notations, publicId, systemId):
        FtNode.__init__(self, None)
        self.__dict__['__nodeName'] = name
        self._entities = entities
        self._notations = notations
        self._publicId = publicId
        self._systemId = systemId
        #FIXME: Text repr of the entities
        self._internalSubset = ''

    ### Attribute Methods ###

    def _get_name(self):
        return self.__dict__['__nodeName']

    def _get_entities(self):
        return self._entities

    def _get_notations(self):
        return self._notations

    def _get_publicId(self):
        return self._publicId

    def _get_systemId(self):
        return self._systemId

    def _get_internalSubset(self):
        return self._internalSubset

    ### Overridden Methods ###

    def __repr__(self):
        return "<DocumentType Node at %x: Name='%s' with %d entities and %d notations>" % (
            id(self),
            self.nodeName,
            len(self._entities),
            len(self._notations)
            )

    ### Internal Methods ###

    # Behind the back setting of doctype's ownerDocument
    # Also sets the owner of the NamedNodeMaps
    def _4dom_setOwnerDocument(self, newOwner):
        self.__dict__['__ownerDocument'] = newOwner
        #self._entities._4dom_setOwnerDocument(newOwner)
        #self._notations._4dom_setOwnerDocument(newOwner)

    def _4dom_setName(self, name):
        # Used to keep the root element and doctype in sync
        self.__dict__['__nodeName'] = name

    ### Helper Functions For Cloning ###

    def _4dom_clone(self, owner):
        return self.__class__(self.name,
                              self.entities._4dom_clone(owner),
                              self.notations._4dom_clone(owner),
                              self._publicId,
                              self._systemId)

    def __getinitargs__(self):
        return (self.nodeName,
                self._entities,
                self._notations,
                self._publicId,
                self._systemId
                )

    ### Attribute Access Mappings ###

    _readComputedAttrs = FtNode._readComputedAttrs.copy()
    _readComputedAttrs.update({'name':_get_name,
                               'entities':_get_entities,
                               'notations':_get_notations,
                               'publicId':_get_publicId,
                               'systemId':_get_systemId,
                               'internalSubset':_get_internalSubset
                               })


    _writeComputedAttrs = FtNode._writeComputedAttrs.copy()
    _writeComputedAttrs.update({
                                })

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                            FtNode._readOnlyAttrs + _readComputedAttrs.keys())
