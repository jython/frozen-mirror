########################################################################
#
# File Name:            Attr.py
#
#
"""
DOM Level 2 Attribute Node
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom import Node
from DOMImplementation import implementation
from FtNode import FtNode
from Event import MutationEvent

class Attr(FtNode):
    nodeType = Node.ATTRIBUTE_NODE
    _allowedChildren = [Node.TEXT_NODE,
                        Node.ENTITY_REFERENCE_NODE
                        ]

    def __init__(self, ownerDocument, name, namespaceURI, prefix, localName):
        FtNode.__init__(self, ownerDocument, namespaceURI, prefix, localName)
        self.__dict__['__nodeName'] = name
        self._ownerElement = None

    ### Attribute Methods ###

    def _get_name(self):
        return self.__dict__['__nodeName']

    def _get_specified(self):
        #True if this attribute was explicitly given a value in the document
        return self._get_value() != ''

    def _get_value(self):
        return reduce(lambda value, child:
                      value + child.nodeValue,
                      self.childNodes, '')

    def _set_value(self, value):
        old_value = self.value
        if value != old_value or len(self.childNodes) > 1:
            # Remove previous childNodes
            while self.firstChild:
                self.removeChild(self.firstChild)
            if value:
                self.appendChild(self.ownerDocument.createTextNode(value))
            owner = self._ownerElement
            if owner:
                owner._4dom_fireMutationEvent('DOMAttrModified',
                                              relatedNode=self,
                                              prevValue=old_value,
                                              newValue=value,
                                              attrName=self.name,
                                              attrChange=MutationEvent.MODIFICATION)
                owner._4dom_fireMutationEvent('DOMSubtreeModified')


    def _get_ownerElement(self):
        return self._ownerElement

    ### Overridden Methods ###

    def _get_nodeValue(self):
        return self._get_value()

    def _set_nodeValue(self, value):
        self._set_value(value)

    def __repr__(self):
        return '<Attribute Node at %x: Name="%s", Value="%s">' % (
            id(self),
            self.name,
            self.value
            )

    ### Helper Functions For Cloning ###

    def _4dom_clone(self, owner):
        a = self.__class__(owner,
                           self.nodeName,
                           self.namespaceURI,
                           self.prefix,
                           self.localName)
        for child in self.childNodes:
            a.appendChild(child._4dom_clone(owner))
        return a

    def __getinitargs__(self):
        return (self.ownerDocument,
                self.nodeName,
                self.namespaceURI,
                self.prefix,
                self.localName
                )

    def __getstate__(self):
        return self.childNodes

    def __setstate__(self, children):
        self.childNodes.extend(list(children))
        for i in range(1, len(children)):
            children[i]._4dom_setHierarchy(self, children[i-1], None)

    ### Internal Methods ###

    def _4dom_setOwnerElement(self, owner):
        self.__dict__['_ownerElement'] = owner

    ### Attribute Access Mappings ###

    _readComputedAttrs = FtNode._readComputedAttrs.copy()
    _readComputedAttrs.update({
        'name':_get_name,
        'specified':_get_specified,
        'ownerElement':_get_ownerElement,
        'value':_get_value,
        'nodeValue':_get_value
        })

    _writeComputedAttrs = FtNode._writeComputedAttrs.copy()
    _writeComputedAttrs.update({
        'value':_set_value,
        'nodeValue':_set_value
        })

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                            FtNode._readOnlyAttrs + _readComputedAttrs.keys())
