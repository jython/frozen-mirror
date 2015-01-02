########################################################################
#
# File Name:            Document.py
#
#
"""

WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import re, string


from DOMImplementation import implementation
from FtNode import FtNode, get_name_pattern
from ext import SplitQName

from xml.dom import Node
from xml.dom import XML_NAMESPACE
from xml.dom import XMLNS_NAMESPACE
from xml.dom import EMPTY_NAMESPACE
from xml.dom import HierarchyRequestErr
from xml.dom import InvalidCharacterErr
from xml.dom import NotSupportedErr
from xml.dom import NamespaceErr

class Document(FtNode):
    #Base node type for this class
    nodeType = Node.DOCUMENT_NODE
    nodeName = "#document"

    #This is for validation that the proper nodes are added
    _allowedChildren = [Node.PROCESSING_INSTRUCTION_NODE,
        Node.COMMENT_NODE,
        Node.ELEMENT_NODE,
        Node.DOCUMENT_TYPE_NODE
        ]

    def __init__(self, doctype):
        FtNode.__init__(self, None)
        self.__dict__['__doctype'] = None
        self.__dict__['__implementation'] = implementation
        self.__dict__['__documentElement'] = None
        self.__dict__['_singleChildren'] = {Node.ELEMENT_NODE:'__documentElement',
                                            Node.DOCUMENT_TYPE_NODE:'__doctype'
                                            }
        self._4dom_setDocumentType(doctype)

    ### Attribute Methods ###

    def _get_doctype(self):
        return self.__dict__['__doctype']

    def _get_implementation(self):
        return self.__dict__['__implementation']

    def _get_documentElement(self):
        return self.__dict__['__documentElement']

    def _get_ownerDocument(self):
        return self

    ### Methods ###

    def createAttribute(self, name):
        if not get_name_pattern().match(name):
            raise InvalidCharacterErr()
        import Attr
        return Attr.Attr(self, name, EMPTY_NAMESPACE, None, None)

    def createCDATASection(self, data):
        from CDATASection import CDATASection
        return CDATASection(self, data)

    def createComment(self, data):
        from Comment import Comment
        return Comment(self, data)

    def createDocumentFragment(self):
        from DocumentFragment import DocumentFragment
        return DocumentFragment(self)

    def createElement(self, tagname):
        if not get_name_pattern().match(tagname):
            raise InvalidCharacterErr()
        from Element import Element
        return Element(self, tagname, EMPTY_NAMESPACE, None, None)

    def createEntityReference(self, name):
        if not get_name_pattern().match(name):
            raise InvalidCharacterErr()
        from EntityReference import EntityReference
        return EntityReference(self, name)

    def createProcessingInstruction(self, target, data):
        if not get_name_pattern().match(target):
            raise InvalidCharacterErr()

        #FIXME: Unicode support
        # Technically, chacters from the unicode surrogate blocks are illegal.
        #for c in target:
        #    if c in unicode_surrogate_blocks:
        #        raise InvalidCharacterErr()

        from ProcessingInstruction import ProcessingInstruction
        return ProcessingInstruction(self, target, data);

    def createTextNode(self, data):
        from Text import Text
        return Text(self, data)

    def getElementById(self, elementId):
        #FIXME: Must be implemented in the parser first
        return None

    def getElementsByTagName(self, tagName):
        nodeList = implementation._4dom_createNodeList([])
        root = self.documentElement
        if root:
            if tagName == '*' or root.tagName == tagName:
                nodeList.append(root)
            nodeList.extend(list(root.getElementsByTagName(tagName)))
        return nodeList

    ### DOM Level 2 Methods ###

    def createAttributeNS(self, namespaceURI, qualifiedName):
        if not get_name_pattern().match(qualifiedName):
            raise InvalidCharacterErr()
        from Attr import Attr
        (prefix, localName) = SplitQName(qualifiedName)
        if prefix == 'xml' and namespaceURI != XML_NAMESPACE:
            raise NamespaceErr()
        if localName == 'xmlns':
            if namespaceURI != XMLNS_NAMESPACE:
                raise NamespaceErr()
            return Attr(self, qualifiedName, XMLNS_NAMESPACE, 'xmlns', prefix)
        elif namespaceURI == '':
            raise NamespaceErr("Use None instead of '' for empty namespace")
        else:
            if (not namespaceURI and prefix) or (not prefix and namespaceURI):
                raise NamespaceErr()
            return Attr(self, qualifiedName, namespaceURI, prefix, localName)

    def importNode(self, importedNode, deep):
        importType = importedNode.nodeType

        # No import allow per spec
        if importType in [Node.DOCUMENT_NODE, Node.DOCUMENT_TYPE_NODE]:
            raise NotSupportedErr()

        # Only the EntRef itself is copied since the source and destination
        # documents might have defined the entity differently
        #FIXME: If the document being imported into provides a definition for
        #       this entity name, its value is assigned.
        #       Need entity support for this!!
        elif importType == Node.ENTITY_REFERENCE_NODE:
            deep = 0

        return importedNode.cloneNode(deep, newOwner=self)

    def createElementNS(self, namespaceURI, qualifiedName):
        from Element import Element
        if not get_name_pattern().match(qualifiedName):
            raise InvalidCharacterErr()
        (prefix, localName) = SplitQName(qualifiedName)
        if prefix == 'xml' and namespaceURI != XML_NAMESPACE:
            raise NamespaceErr()
        if prefix and not namespaceURI:
            raise NamespaceErr()
        elif namespaceURI == '':
            raise NamespaceErr("Use None instead of '' for empty namespace")
        return Element(self, qualifiedName, namespaceURI, prefix, localName)

    def getElementsByTagNameNS(self,namespaceURI,localName):
        if namespaceURI == '':
            raise NamespaceErr("Use None instead of '' for empty namespace")
        nodeList = implementation._4dom_createNodeList([])
        root = self.documentElement
        if root:
            if ((namespaceURI == '*' or namespaceURI == root.namespaceURI) and
                (localName == '*' or localName == root.localName)):
                nodeList.append(root)
            nodeList.extend(list(root.getElementsByTagNameNS(namespaceURI,
                                                             localName)))
        return nodeList

    ### Document Traversal Factory Functions ###

    def createNodeIterator(self, root, whatToShow, filter, entityReferenceExpansion):
        from NodeIterator import NodeIterator
        return  NodeIterator(root, whatToShow, filter, entityReferenceExpansion)

    def createTreeWalker(self, root, whatToShow, filter, entityReferenceExpansion):
        from TreeWalker import TreeWalker
        return TreeWalker(root, whatToShow, filter, entityReferenceExpansion)

    ### Document Event Factory Functions ###

    def createEvent(self,eventType):
        import Event
        if eventType in Event.supportedEvents:
            #Only mutation events are supported
            return Event.MutationEvent(eventType)
        else:
            raise NotSupportedErr()

    ### Document Range Factory Functions ###
    def createRange(self):
        if not self.implementation.hasFeature('RANGE','2.0'):
            raise NotSupportedErr()
        import Range
        return Range.Range(self)

    ### Overridden Methods ###

    def appendChild(self, newChild):
        self._4dom_addSingle(newChild)
        return FtNode.appendChild(self, newChild)

    def insertBefore(self, newChild, oldChild):
        self._4dom_addSingle(newChild)
        return FtNode.insertBefore(self, newChild, oldChild)

    def replaceChild(self, newChild, oldChild):
        if newChild.nodeType != Node.DOCUMENT_FRAGMENT_NODE:
            root = self.__dict__['__documentElement']
            if root in [oldChild, newChild]:
                self.__dict__['__documentElement'] = None
            else:
                raise HierarchyRequestErr()
        replaced = FtNode.replaceChild(self, newChild, oldChild)
        if newChild.nodeType == Node.ELEMENT_NODE:
            self.__dict__['__documentElement'] = newChild
            if self.__dict__['__doctype']:
                self.__dict__['__doctype']._4dom_setName(newChild.nodeName)
        return replaced

    def removeChild(self,oldChild):
        node = FtNode.removeChild(self, oldChild)
        if self.documentElement == node:
            self.__dict__['__documentElement'] = None
        if self.__dict__['__doctype'] == node:
            self.__dict__['__doctype'] = None
        return node

    def cloneNode(self, deep):
        doc = self.__class__(None)
        if deep:
            for child in self.childNodes:
                clone = child.cloneNode(deep, newOwner=doc)
                if child.nodeType == Node.DOCUMENT_TYPE_NODE:
                    doc._4dom_setDocumentType(clone)
                else:
                    doc.appendChild(clone)
        return doc

    def __repr__(self):
        return "<%s Document at %x>" % (
            (self.isXml() and 'XML' or 'HTML'),
            id(self)
            )

    ### Internal Methods ###

    def _4dom_createEntity(self, publicId, systemId, notationName):
        from Entity import Entity
        return Entity(self, publicId, systemId, notationName)

    def _4dom_createNotation(self, publicId, systemId, name):
        from Notation import Notation
        return Notation(self, publicId, systemId, name)

    def _4dom_setDocumentType(self, doctype):
        if not self.__dict__['__doctype'] and doctype is not None:
            self.__dict__['__doctype'] = doctype
            doctype._4dom_setOwnerDocument(self)
            return FtNode.appendChild(self, doctype)

    def _4dom_addSingle(self, node):
        '''Make sure only one Element node is added to a Document'''
        if node.nodeType == Node.ELEMENT_NODE:
            self._4dom_validateNode(node)
            if node.parentNode != None:
                node.parentNode.removeChild(node)
            if self.__dict__['__documentElement']:
                raise HierarchyRequestErr()
            self.__dict__['__documentElement'] = node
            if self.__dict__['__doctype']:
                self.__dict__['__doctype']._4dom_setName(node.nodeName)

    ### Helper Functions for Pickling ###

    def __getinitargs__(self):
        return (None,)

    def __getstate__(self):
        return (self.childNodes, self.doctype, self.documentElement)

    def __setstate__(self, (children, doctype, root)):
        FtNode.__setstate__(self, children)
        self.__dict__['__doctype'] = doctype
        self.__dict__['__documentElement'] = root
        return

    ### Convenience Functions ###

    def isXml(self):
        return 1

    def isHtml(self):
        return 0

    ### Attribute Access Mappings ###

    _readComputedAttrs = FtNode._readComputedAttrs.copy()
    _readComputedAttrs.update({'doctype':_get_doctype,
                               'implementation':_get_implementation,
                               'documentElement':_get_documentElement,
                               'ownerDocument':_get_ownerDocument,
                               })


    _writeComputedAttrs = FtNode._writeComputedAttrs.copy()

    # Create the read-only list of attributes
    _readOnlyAttrs = filter(lambda k,m=_writeComputedAttrs: not m.has_key(k),
                            FtNode._readOnlyAttrs + _readComputedAttrs.keys())
