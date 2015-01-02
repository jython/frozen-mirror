##############################################################################
#
# Zope Public License (ZPL) Version 1.0
# -------------------------------------
#
# Copyright (c) Digital Creations.  All rights reserved.
#
# This license has been certified as Open Source(tm).
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions in source code must retain the above copyright
#    notice, this list of conditions, and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions, and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# 3. Digital Creations requests that attribution be given to Zope
#    in any manner possible. Zope includes a "Powered by Zope"
#    button that is installed by default. While it is not a license
#    violation to remove this button, it is requested that the
#    attribution remain. A significant investment has been put
#    into Zope, and this effort will continue if the Zope community
#    continues to grow. This is one way to assure that growth.
#
# 4. All advertising materials and documentation mentioning
#    features derived from or use of this software must display
#    the following acknowledgement:
#
#      "This product includes software developed by Digital Creations
#      for use in the Z Object Publishing Environment
#      (http://www.zope.org/)."
#
#    In the event that the product being advertised includes an
#    intact Zope distribution (with copyright and license included)
#    then this clause is waived.
#
# 5. Names associated with Zope or Digital Creations must not be used to
#    endorse or promote products derived from this software without
#    prior written permission from Digital Creations.
#
# 6. Modified redistributions of any form whatsoever must retain
#    the following acknowledgment:
#
#      "This product includes software developed by Digital Creations
#      for use in the Z Object Publishing Environment
#      (http://www.zope.org/)."
#
#    Intact (re-)distributions of any official Zope release do not
#    require an external acknowledgement.
#
# 7. Modifications are encouraged but must be packaged separately as
#    patches to official Zope releases.  Distributions that do not
#    clearly separate the patches from the original work must be clearly
#    labeled as unofficial distributions.  Modifications which do not
#    carry the name Zope may be packaged in any form, as long as they
#    conform to all of the clauses above.
#
#
# Disclaimer
#
#   THIS SOFTWARE IS PROVIDED BY DIGITAL CREATIONS ``AS IS'' AND ANY
#   EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#   IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#   PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL DIGITAL CREATIONS OR ITS
#   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#   SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#   LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
#   USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#   ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#   OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
#   OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
#   SUCH DAMAGE.
#
#
# This software consists of contributions made by Digital Creations and
# many individuals on behalf of Digital Creations.  Specific
# attributions are listed in the accompanying credits file.
#
##############################################################################

from Base import *

import string
import xml.dom
from xml.dom import Node


# --- DOMImplementation

class DOMImplementationReadTestCase(TestCaseBase):

    def setUp(self):
        # self.implementation is already set.
        pass

    # Combinations to feed to the hasFeature method; some of these will always
    # return false, of course.
    # ('Core', '1.0') was never defined for DOM level 1, it was implicit. Most
    # DOM level 2 implementations return true, but this is a courtesy.
    featureMatrix = (
        ('Core', None),
        #('Core', '1.0'),
        ('Core', '2.0'),
        ('Core', '3.0'),

        ('XML', None),
        ('XML', '1.0'),
        ('XML', '2.0'),
        ('XML', '3.0'),

        ('Traversal', None),
        ('Traversal', '1.0'),
        ('Traversal', '2.0'),
        ('Traversal', '3.0'),

        ('BogusFeature', None),
        ('BogusFeature', '1.0'),
        ('BogusFeature', '2.0'),
        ('BogusFeature', '3.0'),
    )

    def checkHasFeature(self):
        impl = self.implementation
        for feature, level in self.featureMatrix:
            result1 = impl.hasFeature(feature, level)
            result2 = impl.hasFeature(string.upper(feature), level)
            result3 = impl.hasFeature(string.lower(feature), level)

            expect = ((feature, level) in self.supportedFeatures)

            self.assertEqual(
                result1, result2,
                "Different results from different case feature string.")
            self.assertEqual(
                result1, result3,
                "Different results from different case feature string.")

            self.assertEqual(
                (result1 and 1 or 0), expect,
                "Test for %s, version %s should have returned %s, "
                "returned %s" % (repr(feature), repr(level), repr(expect),
                                 repr(result1)))


# --- Node

class NodeReadTestCaseBase(TestCaseBase):

    nodeTypes = (
        'ATTRIBUTE_NODE',
        'CDATA_SECTION_NODE',
        'COMMENT_NODE',
        'DOCUMENT_FRAGMENT_NODE',
        'DOCUMENT_NODE',
        'DOCUMENT_TYPE_NODE',
        'ELEMENT_NODE',
        'ENTITY_NODE',
        'ENTITY_REFERENCE_NODE',
        'NOTATION_NODE',
        'PROCESSING_INSTRUCTION_NODE',
        'TEXT_NODE',
    )

    def checkNodeTypeConstants(self):
        for type in self.nodeTypes:
            checkAttribute(self.node, type, getattr(Node, type))

    def checkAttributes(self):
        if self.node.nodeType == Node.ELEMENT_NODE:
            checkLength(self.node.attributes, 0)
        else:
            checkAttribute(self.node, 'attributes', None)

        checkReadOnly(self.node, 'attributes')

    def checkChildNodes(self):
        if self.node.nodeType in (Node.ATTRIBUTE_NODE,
                Node.DOCUMENT_NODE,
                Node.ENTITY_NODE):
            expectedLength = 1

        else:
            expectedLength = 0

        checkLength(self.node.childNodes, expectedLength)
        checkReadOnly(self.node, 'childNodes')

    def checkFirstChild(self):
        # The following node types are expected to have one childNode.
        if self.node.nodeType not in (Node.ATTRIBUTE_NODE,
                Node.DOCUMENT_NODE,
                Node.ENTITY_NODE):
            expected = None

        else:
            expected = self.node.childNodes[0]

        checkAttributeSameNode(self.node, 'firstChild', expected)
        checkReadOnly(self.node, 'firstChild')
        if expected:
            checkAttributeSameNode(self.node.firstChild, 'parentNode',
                self.node)

    def checkLastChild(self):
        # The following node types are expected to have one childNode.
        if self.node.nodeType not in (Node.ATTRIBUTE_NODE,
                Node.DOCUMENT_NODE,
                Node.ENTITY_NODE):
            expected = None

        else:
            expected = self.node.childNodes[0]

        checkAttributeSameNode(self.node, 'lastChild', expected)
        checkReadOnly(self.node, 'lastChild')
        if expected:
            checkAttributeSameNode(self.node.lastChild, 'parentNode',
                self.node)

    def checkNextSibling(self):
        checkAttribute(self.node, 'nextSibling', None)
        checkReadOnly(self.node, 'nextSibling')

    nodeNameMap = {
        Node.CDATA_SECTION_NODE:     '#cdata-section',
        Node.COMMENT_NODE:           '#comment',
        Node.DOCUMENT_NODE:          '#document',
        Node.DOCUMENT_FRAGMENT_NODE: '#document-fragment',
        Node.TEXT_NODE:              '#text',
    }

    def checkNodeName(self):
        if self.node.nodeType in (Node.ATTRIBUTE_NODE,
                Node.DOCUMENT_TYPE_NODE):
            expected = self.node.name

        elif self.node.nodeType == Node.ELEMENT_NODE:
            expected = self.node.tagName

        elif self.node.nodeType in (Node.ENTITY_NODE,
                Node.ENTITY_REFERENCE_NODE,
                Node.NOTATION_NODE):
            expected = self.expectedNodeName

        elif self.node.nodeType == Node.PROCESSING_INSTRUCTION_NODE:
            expected = self.node.target

        else:
            expected = self.nodeNameMap[self.node.nodeType]

        checkAttribute(self.node, 'nodeName', expected)
        checkReadOnly(self.node, "nodeName")

    def checkNodeType(self):
        checkAttribute(self.node, 'nodeType', self.expectedType)
        checkReadOnly(self.node, "nodeType")

    emptyNodeValueList = (
        Node.DOCUMENT_FRAGMENT_NODE,
        Node.DOCUMENT_NODE,
        Node.DOCUMENT_TYPE_NODE,
        Node.ELEMENT_NODE,
        Node.ENTITY_NODE,
        Node.ENTITY_REFERENCE_NODE,
        Node.NOTATION_NODE,
    )

    def checkNodeValue(self):
        if self.node.nodeType in self.emptyNodeValueList:
            expected = None

        elif self.node.nodeType in (Node.CDATA_SECTION_NODE,
                Node.COMMENT_NODE,
                Node.TEXT_NODE,
                Node.PROCESSING_INSTRUCTION_NODE):
            expected = self.node.data

        elif self.node.nodeType == Node.ATTRIBUTE_NODE:
            expected = self.node.value

        checkAttribute(self.node, 'nodeValue', expected)

    def checkParentNode(self):
        checkAttribute(self.node, 'parentNode', None)
        checkReadOnly(self.node, 'parentNode')

    def checkPreviousSibling(self):
        checkAttribute(self.node, 'previousSibling', None)
        checkReadOnly(self.node, 'previousSibling')

    def hasChildNodes(self):
        if self.node.nodeType in (Node.ATTRIBUTE_NODE,
                Node.DOCUMENT_NODE,
                Node.ENTITY_NODE):
            expectTrue = 1
        else:
            expectTrue = 0

        if expectTrue:
            self.failUnless(
                self.node.hasChildNodes(),
                "hasChildNodes returned 'false' when 'true' was expected.")
        else:
            self.failIf(
                self.node.hasChildNodes(),
                "hasChildNodes returned 'true' when 'false' was expected.")


class NodeWriteTestCaseBase(TestCaseBase):

    TEST_NAME = 'somename'

    emptyNodeValueList = NodeReadTestCaseBase.emptyNodeValueList

    readOnlyNodeList = (
        Node.ENTITY_NODE,
        Node.ENTITY_REFERENCE_NODE,
        Node.NOTATION_NODE,
    )

    def checkNodeValue(self):
        # Nodetypes that are read-only.
        if self.node.nodeType in self.readOnlyNodeList:
            checkReadOnly(self.node, 'nodeValue')
            return

        # Nodetypes that should ignore changes.
        if self.node.nodeType in self.emptyNodeValueList:
            self.node.nodeValue = "Ignore this."
            checkAttribute(self.node, "nodeValue", None)
            return

        # Nodetypes where nodeValue is an alias.
        if self.node.nodeType in (Node.CDATA_SECTION_NODE,
                Node.COMMENT_NODE,
                Node.TEXT_NODE,
                Node.PROCESSING_INSTRUCTION_NODE):
            alias = 'data'

        elif self.node.nodeType == Node.ATTRIBUTE_NODE:
            alias = 'value'

        self.node.nodeValue = 'foo'
        checkAttribute(self.node, 'nodeValue', 'foo')
        checkAttribute(self.node, alias, 'foo')

    allowedChildrenMap = {
        Node.DOCUMENT_NODE: (
            Node.ELEMENT_NODE, # Maximum of one, special case
            Node.PROCESSING_INSTRUCTION_NODE,
            Node.COMMENT_NODE,
            Node.DOCUMENT_TYPE_NODE, # Maximum of one, special case
        ),

        Node.DOCUMENT_FRAGMENT_NODE: (
            Node.ELEMENT_NODE,
            Node.PROCESSING_INSTRUCTION_NODE,
            Node.COMMENT_NODE,
            Node.TEXT_NODE,
            Node.CDATA_SECTION_NODE,
            Node.ENTITY_REFERENCE_NODE,
        ),

        Node.DOCUMENT_TYPE_NODE: (),

        Node.ENTITY_REFERENCE_NODE: (
            Node.ELEMENT_NODE,
            Node.PROCESSING_INSTRUCTION_NODE,
            Node.COMMENT_NODE,
            Node.TEXT_NODE,
            Node.CDATA_SECTION_NODE,
            Node.ENTITY_REFERENCE_NODE,
        ),

        Node.ELEMENT_NODE: (
            Node.ELEMENT_NODE,
            Node.TEXT_NODE,
            Node.COMMENT_NODE,
            Node.PROCESSING_INSTRUCTION_NODE,
            Node.CDATA_SECTION_NODE,
            Node.ENTITY_REFERENCE_NODE,
        ),

        Node.ATTRIBUTE_NODE: (
           Node.TEXT_NODE,
           Node.ENTITY_REFERENCE_NODE,
        ),

        Node.PROCESSING_INSTRUCTION_NODE: (),

        Node.COMMENT_NODE: (),

        Node.TEXT_NODE: (),

        Node.CDATA_SECTION_NODE: (),

        Node.ENTITY_NODE: (
            Node.ELEMENT_NODE,
            Node.PROCESSING_INSTRUCTION_NODE,
            Node.COMMENT_NODE,
            Node.TEXT_NODE,
            Node.CDATA_SECTION_NODE,
            Node.ENTITY_REFERENCE_NODE,
        ),

        Node.NOTATION_NODE: (),
    }

    nodeCreateMap = {
        # from Document
        'createAttribute':             ('anAttr',),
        'createCDATASection':          ('a CDATA Section',),
        'createComment':               ('a Comment',),
        'createDocumentFragment':      (),
        'createElement':               ('anElement',),
        'createEntityReference':       ('anEntityReference',),
        'createProcessingInstruction': ('aPI', 'data for PI'),
        'createTextNode':              ('A Text Node',),

        # From DOMImplementation (marked as tuples)
        ('createDocument',):           (None, 'aDocument', None),
        ('createDocumentType',):       ('aDocType', 'uri:public', 'uri:system'),
    }

    def checkAppendChild(self):
        allowedChildren = self.allowedChildrenMap[self.node.nodeType]

        if self.node.nodeType == Node.DOCUMENT_NODE:
            # To create a better test for Document Nodes, we remove the
            # documentElement Node.
            self.node.removeChild(self.node.documentElement)

            # Since appending a Document Type Node to a Document Node isn't
            # allowed, we remove it from the allowed children list for now.
            allowedChildren = allowedChildren[:-1]

        # We add Document Fragment to the list if any child is allowed. Document
        # Fragments can also hold such children. This test only adds empty
        # Document Fragments.
        if allowedChildren:
            allowedChildren = allowedChildren + (Node.DOCUMENT_FRAGMENT_NODE,)

        for factoryMethod, factoryArgs in self.nodeCreateMap.items():
            if type(factoryMethod) is type(()): # DOMImplementation methods
                factory = self.implementation
                factoryMethod = factoryMethod[0]
            else:
                factory = self.document

            newNode = apply(getattr(factory, factoryMethod), factoryArgs)
            numberOfChildren = self.node.childNodes.length

            try:
                # We append two different copies to see how we fare. Esp. handy
                # with testing the restrictions of a Document Node
                returnedNode = self.node.appendChild(newNode)
                newNode = apply(getattr(factory, factoryMethod), factoryArgs)
                returnedNode = self.node.appendChild(newNode)

            except xml.dom.HierarchyRequestErr:
                if self.node.nodeType == Node.DOCUMENT_NODE:
                    if newNode.nodeType == Node.ELEMENT_NODE:
                        self.assert_(self.node.documentElement,
                                     "Couldn't add a Element node to"
                                     " an empty Document.")
                    else: # tried to append nonElement to a Document node
                        self.assert_(
                            newNode.nodeType not in allowedChildren,
                            "Couldn't append a %s Node."
                            % TYPE_NAME[newNode.nodeType])
                else: # tried to append a node to a nonDocument node
                    self.assert_(
                        newNode.nodeType not in allowedChildren,
                        "Couldn't append a %s Node."
                        % TYPE_NAME[newNode.nodeType])

            except xml.dom.NoModificationAllowedErr:
                self.assert_(self.node.nodeType in self.readOnlyNodeList,
                             "Claim of read-only-ness on a modifiable node. "
                             "Tried to append a %s Node"
                             % TYPE_NAME[newNode.nodeType])

            else:
                if newNode.nodeType != Node.DOCUMENT_FRAGMENT_NODE:
                    self.assert_(
                        isSameNode(newNode, returnedNode),
                        "Returned Node is not the same as has been added.")
                    checkAttributeSameNode(self.node, 'lastChild', newNode)
                    checkLength(self.node.childNodes, numberOfChildren + 2)
                else:
                    checkLength(self.node.childNodes, numberOfChildren)

                self.assert_(newNode.nodeType in allowedChildren,
                             "Was allowed to append a %s Node."
                             % TYPE_NAME[newNode.nodeType])

                self.assert_(
                    self.node.nodeType not in self.readOnlyNodeList,
                    "Was allowed to append a %s Node to a read-only Node"
                    % TYPE_NAME[newNode.nodeType])

    def checkAppendChildForeignNode(self):
        allowedChildren = self.allowedChildrenMap[self.node.nodeType]

        # No use when no children are allowed or read-only
        if not allowedChildren or self.node.nodeType in self.readOnlyNodeList:
            return

        foreignDoc = self.implementation.createDocument(None, 'anotherDoc',
            None)
        if Node.TEXT_NODE in allowedChildren:
            foreignNode = foreignDoc.createTextNode('a Text Node')
        else:
            foreignNode = foreignDoc.createComment('a Comment Node')

        self.assertRaises(xml.dom.WrongDocumentErr,
                          self.node.appendChild, foreignNode)

    def checkAppendChildAncestorNode(self):
        nodeType = self.node.nodeType
        if nodeType in self.readOnlyNodeList:
            return

        if Node.ELEMENT_NODE not in self.allowedChildrenMap[nodeType]:
            return
        if nodeType not in self.allowedChildrenMap[Node.ELEMENT_NODE]:
            return

        ancestorNode = self.document.createElement('foo')
        ancestorNode.appendChild(self.node)

        self.assertRaises(xml.dom.HierarchyRequestErr,
                          self.node.appendChild, ancestorNode)

    def checkAppendChildSelf(self):
        # See DOM erratum core-6
        if self.node.nodeType in self.readOnlyNodeList:
            return

        if self.node.nodeType not in self.allowedChildrenMap[
                self.node.nodeType]:
            return

        self.assertRaises(xml.dom.HierarchyRequestErr,
                          self.node.appendChild, self.node)

    def checkAppendChildWithAttachedNode(self):
        # Test appending a Node that itself is part of a tree
        allowedChildren = self.allowedChildrenMap[self.node.nodeType]

        # No use when no children are allowed or read-only
        if not allowedChildren or self.node.nodeType in self.readOnlyNodeList:
            return

        if Node.TEXT_NODE in allowedChildren:
            newNode = self.document.createTextNode('a Text Node')
        else:
            newNode = self.document.createComment('a Comment Node')

        oldParent = self.document.createElement('aParentElement')
        oldParent.appendChild(newNode)

        self.node.appendChild(newNode)

        self.failIf(oldParent.hasChildNodes(),
                    "Appended Node not removed from previous parent.")

    def checkAppendChildNodeParentReadOnly(self):
        # See DOM erratum core-2 http://www.w3.org/2000/11/DOM-Level-2-errata
        if self.node.nodeType in self.readOnlyNodeList:
            return
        if Node.TEXT_NODE not in self.allowedChildrenMap[self.node.nodeType]:
            return
        if self.node.nodeType in [Node.DOCUMENT_NODE, Node.DOCUMENT_TYPE_NODE]:
            return                      # can't import

        doc = self.parse("""
            <!DOCTYPE doc [
                <!ENTITY entity "Entity text">
            ]>
            <doc/>""")
        # This Text Node has a read-only parent.
        textNode = doc.doctype.entities.getNamedItem('entity').firstChild
        # we need self.node to have the same doc as textNode
        self.node = doc.importNode(self.node, 1)

        self.assertRaises(xml.dom.NoModificationAllowedErr,
                          self.node.appendChild, textNode)

    def checkRemoveChild(self):
        if self.node.nodeType in self.readOnlyNodeList:
            if self.node.hasChildNodes():
                # Test for read-only
                self.assertRaises(xml.dom.NoModificationAllowedErr,
                                  self.node.removeChild, self.node.firstChild)
            return

        # If this is a Document Node, let's try and remove the doctype.
        # We actually test this when we have a doctype, as the Document Node
        # created for the Document Node tests doesn't *have* a doctype.
        if self.node.nodeType == Node.DOCUMENT_TYPE_NODE:
            doc = self.implementation.createDocument('', 'foo', self.node)
            self.assertRaises(xml.dom.NoModificationAllowedErr,
                              doc.removeChild, doc.doctype)

        allowedChildren = self.allowedChildrenMap[self.node.nodeType]

        # No use when no children are allowed
        if not allowedChildren:
            return

        if Node.TEXT_NODE in allowedChildren:
            newNode = self.document.createTextNode('a Text Node')
        else:
            newNode = self.document.createComment('a Comment Node')

        self.node.appendChild(newNode)

        returnedNode = self.node.removeChild(newNode)
        self.assert_(isSameNode(newNode, returnedNode),
                     "Returned Node is not the appended Node.")
        checkAttribute(newNode, "parentNode", None)
        checkAttribute(returnedNode, "parentNode", None)


    def checkRemoveChildNotFound(self):
        if self.node.nodeType in self.readOnlyNodeList:
            return

        loseNode = self.document.createTextNode('booh')
        self.assertRaises(xml.dom.NotFoundErr,
                          self.node.removeChild, loseNode)

    def checkInsertBefore(self):
        if self.node.nodeType in self.readOnlyNodeList:
            if self.node.hasChildNodes():
                # Test for read-only
                newNode = self.document.createTextNode('a Text Node')
                self.assertRaises(
                    xml.dom.NoModificationAllowedErr,
                    self.node.insertBefore, newNode, self.node.firstChild)
            return

        allowedChildren = self.allowedChildrenMap[self.node.nodeType]

        if self.node.nodeType == Node.DOCUMENT_NODE:
            # To create a better test for Document Nodes, we remove the
            # documentElement Node.
            self.node.removeChild(self.node.documentElement)

            # Since inserting a Document Type Node into a Document Node isn't
            # allowed, we remove it from the allowed children list for now.
            allowedChildren = allowedChildren[:-1]

        # No use when no children are allowed.
        if not allowedChildren:
            return
        else:
            # Append DOCUMENT_FRAGMENT to alowed, because we'll add an empty
            # fragment.
            allowedChildren = allowedChildren + (Node.DOCUMENT_FRAGMENT_NODE,)

        if Node.TEXT_NODE in allowedChildren:
            refNode = self.document.createTextNode('a Text Node')
        else:
            refNode = self.document.createComment('a Comment Node')

        # Now create the reference to insert before.
        self.node.appendChild(refNode)

        for factoryMethod, factoryArgs in self.nodeCreateMap.items():
            if type(factoryMethod) is type(()): # DOMImplementation methods
                factory = self.implementation
                factoryMethod = factoryMethod[0]
            else:
                factory = self.document

            newNode = apply(getattr(factory, factoryMethod), factoryArgs)
            numberOfChildren = self.node.childNodes.length

            try:
                returnedNode = self.node.insertBefore(newNode, refNode)

            except xml.dom.HierarchyRequestErr:
                if self.node.nodeType == Node.DOCUMENT_NODE:
                    if newNode.nodeType == Node.ELEMENT_NODE:
                        self.assert_(
                            self.node.documentElement, 
                            "Couldn't add a Element node to an empty Document.")

                self.assert_(newNode.nodeType not in allowedChildren,
                             "Couldn't append a %s Node."
                             % TYPE_NAME[newNode.nodeType])

            except xml.dom.NoModificationAllowedErr:
                self.assert_(self.node.nodeType in self.readOnlyNodeList,
                             "Claim of read-only-ness on a modifiable node. "
                             "Tried to append a %s Node"
                             % TYPE_NAME[self.node.nodeType])

            else:
                if newNode.nodeType != Node.DOCUMENT_FRAGMENT_NODE:
                    self.assert_(
                        isSameNode(newNode, returnedNode),
                        "Returned Node is not the same as has been added.")

                    checkAttributeSameNode(newNode, 'nextSibling', refNode)
                    checkAttributeSameNode(refNode, 'previousSibling', newNode)
                    checkLength(self.node.childNodes, numberOfChildren + 1)
                else:
                    checkLength(self.node.childNodes, numberOfChildren)

                self.assert_(newNode.nodeType in allowedChildren,
                             "Was allowed to insert a %s Node."
                             % TYPE_NAME[newNode.nodeType])

    def checkInsertBeforeNotFound(self):
        allowedChildren = self.allowedChildrenMap[self.node.nodeType]

        # No use when no children are allowed or read-only
        if not allowedChildren or self.node.nodeType in self.readOnlyNodeList:
            return

        if Node.TEXT_NODE in allowedChildren:
            refNode = self.document.createTextNode('a Text Node')
        else:
            refNode = self.document.createComment('a Comment Node')

        self.assertRaises(
            xml.dom.NotFoundErr,
            self.node.insertBefore, refNode, refNode.cloneNode(0))

    def checkInsertBeforeExtraElementToDocument(self):
        if self.node.nodeType == Node.DOCUMENT_NODE:
            newNode = self.document.createElement('foo')
            self.assertRaises(
                xml.dom.HierarchyRequestErr,
                self.node.insertBefore, newNode, self.node.documentElement)

    def checkInsertBeforeForeignNode(self):
        allowedChildren = self.allowedChildrenMap[self.node.nodeType]

        # No use when no children are allowed or read-only
        if not allowedChildren or self.node.nodeType in self.readOnlyNodeList:
            return

        foreignDoc = self.implementation.createDocument(None, 'anotherDoc',
            None)
        if Node.TEXT_NODE in allowedChildren:
            refNode = self.document.createTextNode('a Text Node')
            foreignNode = foreignDoc.createTextNode('a Text Node')
        else:
            refNode = self.document.createComment('a Comment Node')
            foreignNode = foreignDoc.createComment('a Comment Node')

        self.node.appendChild(refNode)

        self.assertRaises(xml.dom.WrongDocumentErr,
                          self.node.insertBefore, foreignNode, refNode)

    def checkInsertBeforeAncestorNode(self):
        if self.node.nodeType in self.readOnlyNodeList:
            return

        if Node.ELEMENT_NODE not in self.allowedChildrenMap[self.node.nodeType]:
            return
        if self.node.nodeType not in self.allowedChildrenMap[Node.ELEMENT_NODE]:
            return

        ancestorNode = self.document.createElement('foo')
        ancestorNode.appendChild(self.node)

        if Node.TEXT_NODE in self.allowedChildrenMap[self.node.nodeType]:
            refNode = self.document.createTextNode('a Text Node')
        else:
            refNode = self.document.createComment('a Comment Node')

        self.node.appendChild(refNode)

        self.assertRaises(xml.dom.HierarchyRequestErr,
                          self.node.insertBefore, ancestorNode, refNode)

    def checkInsertBeforeSelf(self):
        # See DOM erratum core-7
        if self.node.nodeType in self.readOnlyNodeList:
            return

        if self.node.nodeType not in self.allowedChildrenMap[
                self.node.nodeType]:
            return

        if Node.TEXT_NODE in self.allowedChildrenMap[self.node.nodeType]:
            refNode = self.document.createTextNode('a Text Node')
        else:
            refNode = self.document.createComment('a Comment Node')

        self.node.appendChild(refNode)

        self.assertRaises(xml.dom.HierarchyRequestErr,
                          self.node.insertBefore, self.node, refNode)

    def checkInsertBeforeWithAttachedNode(self):
        # Test appending a Node that itself is part of a tree
        allowedChildren = self.allowedChildrenMap[self.node.nodeType]

        # No use when no children are allowed or read-only
        if not allowedChildren or self.node.nodeType in self.readOnlyNodeList:
            return

        if Node.TEXT_NODE in allowedChildren:
            refNode = self.document.createTextNode('a Text Node')
            newNode = self.document.createTextNode('a Text Node')
        else:
            refNode = self.document.createComment('a Comment Node')
            newNode = self.document.createComment('a Comment Node')

        oldParent = self.document.createElement('aParentElement')
        oldParent.appendChild(newNode)

        self.node.appendChild(refNode)
        self.node.insertBefore(newNode, refNode)

        self.failIf(oldParent.hasChildNodes(),
                    "Appended Node not removed from previous parent.")

    def checkInsertBeforeNodeParentReadOnly(self):
        # See DOM erratum core-2 http://www.w3.org/2000/11/DOM-Level-2-errata
        if self.node.nodeType in self.readOnlyNodeList:
            return
        if Node.TEXT_NODE not in self.allowedChildrenMap[self.node.nodeType]:
            return
        if self.node.nodeType in [Node.DOCUMENT_NODE, Node.DOCUMENT_TYPE_NODE]:
            return                      # can't import

        doc = self.parse("""
            <!DOCTYPE doc [
                <!ENTITY entity "Entity text">
            ]>
            <doc/>""")
        # This Text Node has a read-only parent.
        textNode = doc.doctype.entities.getNamedItem('entity').firstChild

        refNode = doc.createTextNode('a Text Node')
        # we need self.node to have the same doc as textNode
        self.node = doc.importNode(self.node, 1)
        self.node.appendChild(refNode)

        self.assertRaises(xml.dom.NoModificationAllowedErr,
                          self.node.insertBefore, textNode, refNode)

    def checkReplaceChild(self):
        if self.node.nodeType in self.readOnlyNodeList:
            if self.node.hasChildNodes():
                # Test for read-only
                newNode = self.document.createTextNode('a Text Node')
                self.assertRaises(
                    xml.dom.NoModificationAllowedErr,
                    self.node.replaceChild, newNode, self.node.firstChild)
            return

        allowedChildren = self.allowedChildrenMap[self.node.nodeType]

        if self.node.nodeType == Node.DOCUMENT_NODE:
            # To create a better test for Document Nodes, we remove the
            # documentElement Node.
            self.node.removeChild(self.node.documentElement)

            # Since replacing with a Document Type Node on a Document Node isn't
            # allowed, we remove it from the allowed children list for now.
            allowedChildren = allowedChildren[:-1]

        # No use when no children are allowed.
        if not allowedChildren:
            return
        else:
            # Append DOCUMENT_FRAGMENT to alowed, because we'll use an empty
            # fragment.
            allowedChildren = allowedChildren + (Node.DOCUMENT_FRAGMENT_NODE,)

        if Node.TEXT_NODE in allowedChildren:
            refNode = self.document.createTextNode('a Text Node')
        else:
            refNode = self.document.createComment('a Comment Node')

        for factoryMethod, factoryArgs in self.nodeCreateMap.items():
            if type(factoryMethod) is type(()): # DOMImplementation methods
                factory = self.implementation
                factoryMethod = factoryMethod[0]
            else:
                factory = self.document

            # Now create the reference to replace. We do this for every Node
            # type we try and replace with.
            self.node.appendChild(refNode)

            newNode = apply(getattr(factory, factoryMethod), factoryArgs)
            numberOfChildren = self.node.childNodes.length

            try:
                returnedNode = self.node.replaceChild(newNode, refNode)

            except xml.dom.HierarchyRequestErr:
                if self.node.nodeType == Node.DOCUMENT_NODE \
                   and newNode.nodeType == Node.ELEMENT_NODE:
                    self.assert_(
                        self.node.documentElement,
                        "Couldn't add an Element node to an empty Document.")

                self.assert_(
                    newNode.nodeType not in allowedChildren,
                    "Couldn't replace an old Node with a %s Node."
                    % TYPE_NAME[newNode.nodeType])

            except xml.dom.NoModificationAllowedErr:
                self.assert_(
                    self.node.nodeType in self.readOnlyNodeList,
                    "Claim of read-only-ness on a modifiable node. "
                    "Tried to replace an old Node with a %s Node"
                    % TYPE_NAME[self.node.nodeType])

            else:
                if newNode.nodeType != Node.DOCUMENT_FRAGMENT_NODE:
                    self.assert_(
                        isSameNode(refNode, returnedNode),
                        "Returned Node is not the same as has been replaced.")

                    checkAttributeSameNode(self.node, 'lastChild', newNode)
                    checkLength(self.node.childNodes, numberOfChildren)
                    self.assert_(
                        isSameNode(refNode, returnedNode),
                        "Returned Node is not the same as has been replaced.")
                else:
                    checkLength(self.node.childNodes, numberOfChildren - 1)

                self.assert_(newNode.nodeType in allowedChildren,
                             "Was allowed to replace an old Node with a "
                             "%s Node." % TYPE_NAME[newNode.nodeType])

    def checkReplaceChildNotFound(self):
        allowedChildren = self.allowedChildrenMap[self.node.nodeType]

        # No use when no children are allowed or read-only
        if not allowedChildren or self.node.nodeType in self.readOnlyNodeList:
            return

        if Node.TEXT_NODE in allowedChildren:
            refNode = self.document.createTextNode('a Text Node')
        else:
            refNode = self.document.createComment('a Comment Node')

        self.assertRaises(
            xml.dom.NotFoundErr,
            self.node.replaceChild, refNode, refNode.cloneNode(0))

    def checkReplaceChildExtraElementToDocument(self):
        if self.node.nodeType == Node.DOCUMENT_NODE:
            refNode = self.document.createComment('a Comment Node')
            self.node.appendChild(refNode)
            newNode = self.document.createElement('foo')

            self.assertRaises(xml.dom.HierarchyRequestErr,
                              self.node.replaceChild, newNode, refNode)

    def checkReplaceChildForeignNode(self):
        allowedChildren = self.allowedChildrenMap[self.node.nodeType]

        # No use when no children are allowed or read-only
        if not allowedChildren or self.node.nodeType in self.readOnlyNodeList:
            return

        foreignDoc = self.implementation.createDocument(None, 'anotherDoc',
            None)
        if Node.TEXT_NODE in allowedChildren:
            refNode = self.document.createTextNode('a Text Node')
            foreignNode = foreignDoc.createTextNode('a Text Node')
        else:
            refNode = self.document.createComment('a Comment Node')
            foreignNode = foreignDoc.createComment('a Comment Node')

        self.node.appendChild(refNode)

        self.assertRaises(xml.dom.WrongDocumentErr,
                          self.node.replaceChild, foreignNode, refNode)

    def checkReplaceChildAncestorNode(self):
        if self.node.nodeType in self.readOnlyNodeList:
            return

        if Node.ELEMENT_NODE not in self.allowedChildrenMap[self.node.nodeType]:
            return
        if self.node.nodeType not in self.allowedChildrenMap[Node.ELEMENT_NODE]:
            return

        ancestorNode = self.document.createElement('foo')
        ancestorNode.appendChild(self.node)

        if Node.TEXT_NODE in self.allowedChildrenMap[self.node.nodeType]:
            refNode = self.document.createTextNode('a Text Node')
        else:
            refNode = self.document.createComment('a Comment Node')

        self.node.appendChild(refNode)

        self.assertRaises(xml.dom.HierarchyRequestErr,
                          self.node.replaceChild, ancestorNode, refNode)

    def checkReplaceChildSelf(self):
        # See DOM erratum core-8
        if self.node.nodeType in self.readOnlyNodeList:
            return

        if self.node.nodeType not in self.allowedChildrenMap[
                self.node.nodeType]:
            return

        if Node.TEXT_NODE in self.allowedChildrenMap[self.node.nodeType]:
            refNode = self.document.createTextNode('a Text Node')
        else:
            refNode = self.document.createComment('a Comment Node')

        self.node.appendChild(refNode)

        self.assertRaises(xml.dom.HierarchyRequestErr,
                          self.node.replaceChild, self.node, refNode)

    def checkReplaceChildWithAttachedNode(self):
        # Test replacing with a Node that itself is part of a tree
        allowedChildren = self.allowedChildrenMap[self.node.nodeType]

        # No use when no children are allowed or read-only
        if not allowedChildren or self.node.nodeType in self.readOnlyNodeList:
            return

        if Node.TEXT_NODE in allowedChildren:
            refNode = self.document.createTextNode('a Text Node')
            newNode = self.document.createTextNode('a Text Node')
        else:
            refNode = self.document.createComment('a Comment Node')
            newNode = self.document.createComment('a Comment Node')

        oldParent = self.document.createElement('aParentElement')
        oldParent.appendChild(newNode)

        self.node.appendChild(refNode)
        self.node.replaceChild(newNode, refNode)

        self.failIf(oldParent.hasChildNodes(),
                    "Replacing Node not removed from previous parent.")

    def checkReplaceChildNodeParentReadOnly(self):
        # See DOM erratum core-2 http://www.w3.org/2000/11/DOM-Level-2-errata
        if self.node.nodeType in self.readOnlyNodeList:
            return
        if Node.TEXT_NODE not in self.allowedChildrenMap[self.node.nodeType]:
            return
        if self.node.nodeType in [Node.DOCUMENT_NODE, Node.DOCUMENT_TYPE_NODE]:
            return                      # can't import

        doc = self.parse("""
            <!DOCTYPE doc [
                <!ENTITY entity "Entity text">
            ]>
            <doc/>""")
        # This Text Node has a read-only parent.
        textNode = doc.doctype.entities.getNamedItem('entity').firstChild
        # we need self.node to have the same doc as textNode
        self.node = doc.importNode(self.node, 1)
        refNode = doc.createTextNode('a Text Node')
        self.node.appendChild(refNode)

        self.assertRaises(xml.dom.NoModificationAllowedErr,
                          self.node.replaceChild, textNode, refNode)



# --- Document

class DocumentReadTestCase(NodeReadTestCaseBase):

    def setUp(self):
        self.createDocument()
        self.node = self.document
        self.expectedType = Node.DOCUMENT_NODE

    def checkGetDoctype(self):
        checkAttribute(self.document, "doctype", None)
        checkReadOnly(self.document, "doctype")

    def checkGetImplementation(self):
        checkAttribute(self.document, "implementation", self.implementation)
        checkReadOnly(self.document, "implementation")

    def checkGetDocumentElement(self):
        checkAttributeNot(self.document, "documentElement", None)
        checkReadOnly(self.document, "documentElement")

    def checkCloneNode(self):
        # TODO: Implementation dependent, what should we test?
        pass


class DocumentWriteTestCase(NodeWriteTestCaseBase):

    def setUp(self):
        self.node = self.createDocument()

    def checkGetElementsByTagName(self):
        doc = self.document

        elements = {}
        names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        for c in names:
            elements[c] = doc.createElement(c)
        # set up simple tree
        elements['a'].appendChild(elements['b'])
        elements['a'].appendChild(elements['d'])
        elements['b'].appendChild(elements['c'])
        elements['d'].appendChild(elements['e'])
        elements['d'].appendChild(elements['h'])
        elements['e'].appendChild(elements['f'])
        elements['e'].appendChild(elements['g'])
        elements['h'].appendChild(elements['i'])

        doc.documentElement.appendChild(elements['a'])

        # now test

        # find all elements in the right order
        result = doc.getElementsByTagName('*')
        self.assertEqual(len(result), len(names) + 1)
        for name, element in map(None, names, result[1:]):
            self.assertEqual(name, element.tagName)

        # find single element, top
        result = doc.getElementsByTagName('a')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].tagName, 'a')

        # find single element somewhere in tree
        result = doc.getElementsByTagName('h')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].tagName, 'h')

    def checkCreateAttribute(self):
        attr = self.document.createAttribute(self.TEST_NAME)

        checkAttribute(attr, 'nodeType', Node.ATTRIBUTE_NODE)
        checkAttribute(attr, 'name', self.TEST_NAME)
        checkAttribute(attr, 'localName', None)
        checkAttribute(attr, 'prefix', None)
        checkAttribute(attr, 'namespaceURI', None)
        checkAttribute(attr, 'value', '')
        checkAttributeSameNode(attr, 'ownerDocument', self.document)

        # Note the ':' in the name, createAttribute does not know about
        # namespaces, so the colon has no special meaning.
        attr = self.document.createAttribute('not_a_prefix:not_a_localname')
        checkAttribute(attr, 'name', 'not_a_prefix:not_a_localname')
        checkAttribute(attr, 'localName', None)
        checkAttribute(attr, 'prefix', None)

        self.assertRaises(xml.dom.InvalidCharacterErr,
                          self.document.createAttribute, '5_illegal')

    def checkCreateCDATASection(self):
        cdata = self.document.createCDATASection('A CDATA Section')

        checkAttribute(cdata, 'nodeType', Node.CDATA_SECTION_NODE)
        checkAttribute(cdata, 'data', 'A CDATA Section')
        checkAttributeSameNode(cdata, 'ownerDocument', self.document)

    def checkCreateComment(self):
        comment = self.document.createComment('A Comment')

        checkAttribute(comment, 'nodeType', Node.COMMENT_NODE)
        checkAttribute(comment, 'data', 'A Comment')
        checkAttributeSameNode(comment, 'ownerDocument', self.document)

    def checkCreateDocumentFragment(self):
        fragment = self.document.createDocumentFragment()

        checkAttribute(fragment, 'nodeType', Node.DOCUMENT_FRAGMENT_NODE)
        checkLength(fragment.childNodes, 0)
        checkAttributeSameNode(fragment, 'ownerDocument', self.document)

    def checkCreateElement(self):
        el = self.document.createElement(self.TEST_NAME)

        checkAttribute(el, 'nodeType', Node.ELEMENT_NODE)
        checkAttribute(el, 'tagName', self.TEST_NAME)
        checkAttribute(el, 'localName', None)
        checkAttribute(el, 'prefix', None)
        checkAttribute(el, 'namespaceURI', None)
        checkAttributeSameNode(el, 'ownerDocument', self.document)

        # Note the ':' in the name, createElement does not know about
        # namespaces, so the colon has no special meaning.
        el = self.document.createElement('not_a_prefix:not_a_localname')
        checkAttribute(el, 'tagName', 'not_a_prefix:not_a_localname')
        checkAttribute(el, 'localName', None)
        checkAttribute(el, 'prefix', None)

    def checkCreateElementInvalidCharacter(self):
        self.assertRaises(xml.dom.InvalidCharacterErr,
                          self.document.createElement, '5_illegal')

    def checkCreateEntityReference(self):
        entRef = self.document.createEntityReference('entityReference')

        checkAttribute(entRef, 'nodeType', Node.ENTITY_REFERENCE_NODE)
        checkAttribute(entRef, 'nodeName', 'entityReference')
        checkAttributeSameNode(entRef, 'ownerDocument', self.document)

    def checkCreateEntityReferenceInvalidCharacter(self):
        self.assertRaises(xml.dom.InvalidCharacterErr,
                          self.document.createEntityReference, '5_illegal')

    def checkCreateProcessingInstruction(self):
        pi = self.document.createProcessingInstruction('PITarget', 'PI Data')

        checkAttribute(pi, 'nodeType', Node.PROCESSING_INSTRUCTION_NODE)
        checkAttribute(pi, 'target', 'PITarget')
        checkAttribute(pi, 'data', 'PI Data')
        checkAttributeSameNode(pi, 'ownerDocument', self.document)

    def checkCreateProcessingInstructionInvalidCharacter(self):
        self.assertRaises(
            xml.dom.InvalidCharacterErr,
            self.document.createProcessingInstruction, '5_illegal', 'data')

    def checkCreateTextNode(self):
        text = self.document.createTextNode('A Text Node')

        checkAttribute(text, 'nodeType', Node.TEXT_NODE)
        checkAttribute(text, 'data', 'A Text Node')
        checkAttributeSameNode(text, 'ownerDocument', self.document)


# --- Element

class ElementReadTestCase(NodeReadTestCaseBase):

    def setUp(self):
        doc = self.createDocument()
        self.element = self.node = doc.createElement("per")
        self.expectedType = Node.ELEMENT_NODE
        self.floating_element = self.element
        self.attached_element = doc.createElement("attached")
        doc.documentElement.appendChild(self.attached_element)

    def checkDocumentElementChildNodes(self):
        checkLength(self.document.documentElement.childNodes, 1)

    def checkAttachedElementParentNode(self):
        checkAttributeSameNode(self.attached_element, "parentNode",
                               self.document.documentElement)

    def checkDocumentElementFirstChild(self):
        checkAttributeSameNode(self.document.documentElement, "firstChild",
                               self.attached_element)
        checkAttributeSameNode(
            self.document.documentElement.firstChild, "parentNode",
                               self.document.documentElement)

    def checkTagName(self):
        checkAttribute(self.floating_element, "tagName", "per")
        checkAttribute(self.attached_element, "tagName", "attached")
        checkReadOnly(self.floating_element, "tagName")

    def checkGetAttribute(self):
        self.assertEqual(self.element.getAttribute("ugga"), "",
                         "non-existant attribute should return ''")

    def checkGetAttributeNode(self):
        self.assert_(self.element.getAttributeNode("ugga") is None,
                     "non-existant attribute node should return None")

    def checkCloneNode(self):
        el = self.element
        doc = self.document
        el.appendChild(doc.createTextNode('A Text Node'))
        el.appendChild(doc.createComment('A Comment'))
        el.setAttribute('attr1', 'An attribute')
        el.setAttribute('attr2', 'Another attribute')

        el.appendChild(el.cloneNode(0))
        clone = el.cloneNode(1)

        self.failIf(isSameNode(el, clone),
                    "Clone is same Node as original.")
        self.failIf(isSameNode(el, clone.lastChild),
                    "Clone is same Node as original.")

        checkAttribute(clone, 'parentNode', None)
        checkLength(clone.childNodes, el.childNodes.length)
        checkLength(clone.attributes, el.attributes.length)
        checkLength(clone.lastChild.childNodes, 0)
        checkLength(clone.lastChild.attributes, el.attributes.length)

        checkAttribute(clone, 'nodeName', el.nodeName)
        checkAttribute(clone.lastChild, 'nodeName', el.nodeName)
        checkAttribute(clone, 'nodeType', el.nodeType)
        checkAttribute(clone.lastChild, 'nodeType', el.nodeType)
        checkAttribute(clone, 'nodeValue', el.nodeValue)
        checkAttribute(clone.lastChild, 'nodeValue', el.nodeValue)

        for i in range(clone.childNodes.length):
            checkAttribute(clone.childNodes.item(i), 'nodeType',
                el.childNodes.item(i).nodeType)
            if clone.childNodes.item(i).nodeType != Node.ELEMENT_NODE:
                checkAttribute(clone.childNodes.item(i), 'data',
                    el.childNodes.item(i).data)

        for i in range(clone.attributes.length):
            checkAttribute(clone.attributes.item(i), 'name',
                el.attributes.item(i).name)
            checkAttribute(clone.lastChild.attributes.item(i), 'name',
                el.attributes.item(i).name)

            checkAttribute(clone.attributes.item(i), 'value',
                el.attributes.item(i).value)
            checkAttribute(clone.lastChild.attributes.item(i), 'value',
                el.attributes.item(i).value)

            # deep and shallow clones should clone attributes
            value = clone.attributes.item(i).value
            el.attributes.item(i).value = 'spam'
            checkAttribute(clone.attributes.item(i), 'value', value)
            checkAttribute(clone.lastChild.attributes.item(i), 'value', value)

            checkAttributeSameNode(clone.attributes.item(i), 'ownerElement',
                clone)
            checkAttributeSameNode(clone.lastChild.attributes.item(i),
                'ownerElement', clone.lastChild)

            self.failIf(isSameNode(el.attributes.item(i),
                                   clone.attributes.item(i)))


class ElementWriteTestCase(NodeWriteTestCaseBase):

    def setUp(self):
        doc = self.createDocument()
        self.element = self.node = doc.createElement("per")
        self.floating_element = self.element
        self.attached_element = doc.createElement("attached")
        self.attached_element2 = doc.createElement("attached2")
        doc.documentElement.appendChild(self.attached_element)
        doc.documentElement.appendChild(self.attached_element2)

    def checkAttachedElementsNextSibling(self):
        checkAttributeSameNode(self.attached_element, "nextSibling",
                               self.attached_element2)
        checkAttributeSameNode(self.attached_element2, "nextSibling",
                               None)

    def checkAttachedElementsPreviousSibling(self):
        checkAttributeSameNode(self.attached_element, "previousSibling",
                               None)
        checkAttributeSameNode(self.attached_element2, "previousSibling",
                               self.attached_element)

    def checkGetElementsByTagName(self):
        doc = self.document
        el = self.element

        elements = {}
        names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        for c in names:
            elements[c] = doc.createElement(c)
        # set up simple tree
        elements['a'].appendChild(elements['b'])
        elements['a'].appendChild(elements['d'])
        elements['b'].appendChild(elements['c'])
        elements['d'].appendChild(elements['e'])
        elements['d'].appendChild(elements['h'])
        elements['e'].appendChild(elements['f'])
        elements['e'].appendChild(elements['g'])
        elements['h'].appendChild(elements['i'])

        el.appendChild(elements['a'])

        # now test

        # find all elements in the right order
        result = el.getElementsByTagName('*')
        self.assertEqual(len(result), len(names))
        for name, element in map(None, names, result):
            self.assertEqual(name, element.tagName)

        # find single element, top
        result = el.getElementsByTagName('a')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].tagName, 'a')

        # find single element somewhere in tree
        result = el.getElementsByTagName('h')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].tagName, 'h')

    def checkSetAttribute(self):
        self.element.setAttribute("ugga", "foo")

        self.assert_(self.element.hasAttribute("ugga"),
                     "Test for presence of created attribute returned false.")

        value = self.element.getAttribute("ugga")
        self.assertEqual(value, 'foo',
                         "Incorrect attr value returned. Expected 'foo', got "
                          + repr(value))

    def checkSetAttributeIllegalCharacter(self):
        self.assertRaises(
            xml.dom.InvalidCharacterErr,
            self.element.setAttribute, '5_illegal', "Don't eat this")

    def checkSetAttributeNode(self):
        node = self.document.createAttribute("ugga")
        node.value = 'foo'
        returnValue = self.element.setAttributeNode(node)

        self.assert_(
            self.element.hasAttribute("ugga"),
            "Test for presence of created attribute returned false.")
        self.assert_(returnValue is None,
                     "Returned value is %s" % repr(returnValue))

        value = self.element.getAttribute("ugga")
        self.assertEqual(value, 'foo',
                         "Incorrect attr value returned. Expected 'foo', got "
                         + repr(value))

        returnedNode = self.element.getAttributeNode("ugga")
        self.assert_(isSameNode(node, returnedNode),
                     "Incorrect node returned from getAttributeNode.")

    def checkSetAttributeNodeReplaceExisting(self):
        node = self.document.createAttribute("ugga")
        self.element.setAttributeNode(node)
        newNode = self.document.createAttribute("ugga")

        returnValue = self.element.setAttributeNode(newNode)
        if returnValue is None:
            self.fail("setAttributeNode did not replace original attribute")
        self.assert_(isSameNode(node, returnValue),
                     "setAttributeNode returned %s" % repr(returnValue))

    def checkSetAttributeNodeWrongDocument(self):
        foreignDoc = self.implementation.createDocument(None, 'foo', None)
        foreignAttr = foreignDoc.createAttribute('spam')
        self.assertRaises(xml.dom.WrongDocumentErr,
                          self.element.setAttributeNodeNS, foreignAttr)

    def checkSetAttributeNodeAlreadyInUse(self):
        otherElement = self.document.createElement('foo')
        otherAttr = self.document.createAttribute('spam')
        otherElement.setAttributeNodeNS(otherAttr)
        self.assertRaises(xml.dom.InuseAttributeErr,
                          self.element.setAttributeNodeNS, otherAttr)

    def checkRemoveAttribute(self):
        node1 = self.document.createAttribute("foo")
        node2 = self.document.createAttribute("bar")
        self.element.setAttributeNode(node1)
        self.element.setAttributeNode(node2)

        self.element.removeAttribute("foo")

        self.failIf(
            self.element.hasAttribute("foo"),
            "Test for presence of created attribute still returns true.")

        self.assert_(self.element.hasAttribute("bar"),
                     "Test for presence of created attribute returned false.")

        checkAttribute(node1, 'ownerElement', None)

    def checkRemoveAttributeNode(self):
        node1 = self.document.createAttribute("foo")
        node2 = self.document.createAttribute("bar")
        self.element.setAttributeNode(node1)
        self.element.setAttributeNode(node2)

        returnedNode = self.element.removeAttributeNode(node1)

        self.assert_(
            isSameNode(node1, returnedNode),
            "Returned node not the same as the one removed.")

        checkAttribute(node1, 'ownerElement', None)

        self.failIf(
            self.element.hasAttribute("foo"),
            "Test for presence of created attribute still returns true.")

        self.assert_(
            self.element.hasAttribute("bar"),
            "Test for presence of created attribute returned false.")

    def checkRemoveAttributeNodeNotFound(self):
        node = self.document.createAttribute("foo")
        self.assertRaises(xml.dom.NotFoundErr,
                          self.element.removeAttributeNode, node)


# --- CharacterData

class CharacterDataReadTestCaseBase(NodeReadTestCaseBase):

    def checkGetData(self):
        checkAttribute(self.chardata, "data", "com")

    def checkGetLength(self):
        checkLength(self.chardata, 3)
        self.assertEqual(len(self.chardata.data), 3)
        self.assertEqual(len(self.chardata._get_data()), 3)

    def checkSubstringData(self):
        self.assertEqual(self.chardata.substringData(0, 2), "co")

    def checkSubstringDataNegativeOffset(self):
        self.assertRaises(xml.dom.IndexSizeErr,
                          self.chardata.substringData, -2, 0)

    def checkSubstringDataOffsetGreaterThanLength(self):
        self.assertRaises(xml.dom.IndexSizeErr,
                          self.chardata.substringData, 10, 0)

    def checkSubstringDataNegativeCount(self):
        self.assertRaises(xml.dom.IndexSizeErr,
                          self.chardata.substringData, 0, -2)

    def checkSubstringDataOffsetAndCountGreaterThanLength(self):
        self.assertEqual(self.chardata.substringData(1, 10), "om")

    def checkCloneNode(self):
        clone = self.chardata.cloneNode(0)
        deepClone = self.chardata.cloneNode(1)

        self.failIf(isSameNode(self.chardata, clone),
                    "Clone is same as original.")
        self.failIf(isSameNode(self.chardata, deepClone),
                    "Clone is same as original.")

        checkAttribute(clone, 'parentNode', None)
        checkAttribute(deepClone, 'parentNode', None)
        checkAttribute(clone, 'nodeType', self.chardata.nodeType)
        checkAttribute(deepClone, 'nodeType', self.chardata.nodeType)
        checkAttribute(clone, 'data', self.chardata.data)
        checkAttribute(deepClone, 'data', self.chardata.data)
        checkLength(clone.childNodes, 0)
        checkLength(deepClone.childNodes, 0)


class CharacterDataWriteTestCaseBase(NodeWriteTestCaseBase):

    def checkSetData(self):
        self.chardata._set_data("data")
        checkAttribute(self.chardata, "data", "data")

    def checkAppendData(self):
        self.chardata.appendData("com")
        checkAttribute(self.chardata, "data", "comcom")

    def checkInsertData(self):
        self.chardata.insertData(2, "com")
        checkAttribute(self.chardata, "data", "cocomm")

    def checkInsertDataNegativeOffset(self):
        self.assertRaises(xml.dom.IndexSizeErr,
                          self.chardata.insertData, -2, 'foo')

    def checkInsertDataOffsetGreaterThanLength(self):
        self.assertRaises(xml.dom.IndexSizeErr,
                          self.chardata.insertData, 10, 'foo')

    def checkDeleteData(self):
        self.chardata.deleteData(1, 1)
        checkAttribute(self.chardata, "data", "cm")

    def checkDeleteDataNegativeOffset(self):
        self.assertRaises(xml.dom.IndexSizeErr,
                          self.chardata.deleteData, -2, 0)

    def checkDeleteDataOffsetGreaterThanLength(self):
        self.assertRaises(xml.dom.IndexSizeErr,
                          self.chardata.deleteData, 10, 0)

    def checkDeleteDataNegativeCount(self):
        self.assertRaises(xml.dom.IndexSizeErr,
                          self.chardata.deleteData, 0, -2)

    def checkDeleteDataOffsetAndCountGreaterThanLength(self):
        self.chardata.deleteData(0, 10)
        checkAttribute(self.chardata, "data", "")

    def checkReplaceData(self):
        self.chardata.replaceData(1, 3, "uuuu")
        checkAttribute(self.chardata, "data", "cuuuu")

    def checkReplaceDataNegativeOffset(self):
        self.assertRaises(xml.dom.IndexSizeErr,
                          self.chardata.replaceData, -2, 0, 'foo')

    def checkReplaceDataOffsetGreaterThanLength(self):
        self.assertRaises(xml.dom.IndexSizeErr,
                          self.chardata.replaceData, 10, 0, 'foo')

    def checkReplaceDataNegativeCount(self):
        self.assertRaises(xml.dom.IndexSizeErr,
                          self.chardata.replaceData, 0, -2, 'foo')

    def checkReplaceDataOffsetAndCountGreaterThanLength(self):
        self.chardata.replaceData(0, 10, "foo")
        checkAttribute(self.chardata, "data", "foo")


# --- Comment

class CommentReadTestCase(CharacterDataReadTestCaseBase):

    def setUp(self):
        self.chardata = self.node = self.createDocument().createComment("com")
        self.expectedType = Node.COMMENT_NODE


class CommentWriteTestCase(CharacterDataWriteTestCaseBase):

    def setUp(self):
        self.chardata = self.node = self.createDocument().createComment("com")


# --- Text

class TextReadTestCase(CharacterDataReadTestCaseBase):

    def setUp(self):
        self.chardata = self.node = self.createDocument().createTextNode("com")
        self.expectedType = Node.TEXT_NODE


class TextWriteTestCase(CharacterDataWriteTestCaseBase):

    def setUp(self):
        self.chardata = self.node = self.createDocument().createTextNode("com")

    def checkAcquisition(self):
        if 1:
            # This test is disabled.  Simple implicit acquisition
            # causes removeAttribute() to be acquired when it
            # probably should not, but this issue is not of
            # sufficient importance for now.
            return
        cdata = self.document.createTextNode("com")
        self.document.documentElement.appendChild(cdata)
        cdata2 = self.document.createTextNode("com2")
        self.document.documentElement.appendChild(cdata2)
        attr = self.document.createAttribute("attrName")
        self.document.documentElement.setAttributeNode(attr)
        # Technically these should raise.  Because of acquisition they
        # might not.  We want to make sure that they don't affect
        # the tree.
        try:
            self.document.documentElement.firstChild.normalize()
        except:
            pass
        try:
            self.document.documentElement.firstChild.removeAttribute(
                "attrName")
        except:
            pass
        else:
            self.fail('removeAttribute() was acquired from documentElement.')
        checkAttribute(self.document.documentElement.childNodes, "length", 2)
        checkAttribute(self.document.documentElement.attributes, "length", 1)

    def checkSplitText(self):
        newNode = self.chardata.splitText(2)

        checkAttribute(self.chardata, 'data', 'co')
        checkAttribute(newNode, 'data', 'm')

    def checkSplitTextOffsetEqualToLength(self):
        try:
            newNode = self.chardata.splitText(self.chardata.length)
        except xml.dom.IndexSizeErr:
            self.fail(
                "INDEX_SIZE_ERR raised on splitText with offset == length.")
        checkAttribute(self.chardata, 'data', 'com')
        checkAttribute(newNode, 'data', '')

    def checkSplitTextNegativeOffset(self):
        self.assertRaises(xml.dom.IndexSizeErr,
                          self.chardata.splitText, -2)

    def checkSplitTextOffsetGreateThanLength(self):
        self.assertRaises(xml.dom.IndexSizeErr,
                          self.chardata.splitText, 10)

    def checkSplitTextWithParent(self):
        el = self.document.createElement('foo')
        el.appendChild(self.chardata)

        newNode = self.chardata.splitText(2)
        checkAttributeSameNode(self.chardata, 'nextSibling', newNode)


# --- Attr

class AttrReadTestCase(NodeReadTestCaseBase):

    def setUp(self):
        self.attr = self.node = self.createDocument().createAttribute("name")
        self.expectedType = Node.ATTRIBUTE_NODE

    def checkGetName(self):
        checkAttribute(self.attr, "name", "name")

    def checkGetSpecified(self):
        self.assert_(self.attr._get_specified())
        self.assert_(self.attr.specified)

    def checkGetValue(self):
        checkAttribute(self.attr, "value", "")

        checkLength(self.attr.childNodes, 1)
        checkAttribute(self.attr.firstChild, 'nodeType', Node.TEXT_NODE)
        checkAttribute(self.attr.firstChild, 'data', '')

    def checkCloneNode(self):
        clone = self.attr.cloneNode(0)
        deepClone = self.attr.cloneNode(1)

        self.failIf(isSameNode(self.attr, clone),
                    "Clone is same as original.")
        self.failIf(isSameNode(self.attr, deepClone),
                    "Clone is same as original.")

        checkAttribute(clone, 'parentNode', None)
        checkAttribute(deepClone, 'parentNode', None)
        checkAttribute(clone, 'nodeType', self.attr.nodeType)
        checkAttribute(deepClone, 'nodeType', self.attr.nodeType)
        checkAttribute(clone, 'name', self.attr.name)
        checkAttribute(deepClone, 'name', self.attr.name)
        checkAttribute(clone, 'value', self.attr.value)
        checkAttribute(deepClone, 'value', self.attr.value)
        checkAttribute(clone, 'specified', 1)
        checkAttribute(deepClone, 'specified', 1)
        checkAttribute(clone, 'nodeName', self.attr.nodeName)
        checkAttribute(deepClone, 'nodeName', self.attr.nodeName)
        checkAttribute(clone, 'nodeValue', self.attr.nodeValue)
        checkAttribute(deepClone, 'nodeValue', self.attr.nodeValue)

        checkLength(clone.childNodes, 1) # Subtree models value
        checkAttribute(clone.firstChild, 'nodeType', Node.TEXT_NODE)
        checkAttribute(clone.firstChild, 'data', self.attr.value)
        checkLength(deepClone.childNodes, 1)
        checkAttribute(deepClone.firstChild, 'nodeType', Node.TEXT_NODE)
        checkAttribute(deepClone.firstChild, 'data', self.attr.value)

class AttrWriteTestCase(NodeWriteTestCaseBase):

    def setUp(self):
        self.attr = self.node = self.createDocument().createAttribute(
            "attrName")
        self.element = self.document.createElement("eltName")

    def checkSetValue(self):
        self.attr._set_value("14")
        checkAttribute(self.attr, "value", "14")

        checkLength(self.attr.childNodes, 1)
        checkAttribute(self.attr.firstChild, 'nodeType', Node.TEXT_NODE)
        checkAttribute(self.attr.firstChild, 'data', '14')

    def checkManipulateSubTree(self):
        attr = self.attr

        self.assert_(attr.hasChildNodes(),
                     "Attr doesn't have subtree to manipulate!")

        newNode = self.document.createTextNode('New Value')
        attr.replaceChild(newNode, attr.firstChild)
        checkAttribute(attr.firstChild, 'data', 'New Value')
        checkAttribute(attr, 'value', 'New Value')

        attr.appendChild(self.document.createTextNode(' (appended)'))
        checkAttribute(attr, 'value', 'New Value (appended)')

        attr.firstChild.appendData(' ')
        attr.replaceChild(self.document.createEntityReference('foo'),
            attr.lastChild)
        checkAttribute(attr, 'value', 'New Value ')

        # Setting the value with a string containing an XML reference does *not*
        # cause it to create an EntiyReference. Everything is a string literal.
        attr.value = 'Some Value &test;'
        checkLength(attr.childNodes, 1)
        checkAttribute(attr.firstChild, 'data', 'Some Value &test;')

    def checkOwnerElement(self):
        checkAttribute(self.attr, "ownerElement", None)
        checkReadOnly(self.attr, "ownerElement")
        self.element.setAttributeNode(self.attr)
        checkAttributeSameNode(self.attr, "ownerElement", self.element)
        checkReadOnly(self.attr, "ownerElement")

    def checkAttrTwoReferencesIntegrity(self):
        #XXX this test should be generalized to any reference
        attr = self.document.createAttribute('spam')
        self.document.documentElement.setAttributeNode(attr)
        a1 = self.document.documentElement.attributes.item(0)
        a2 = self.document.documentElement.attributes.item(0)
        a1.appendChild(self.document.createTextNode('eggs'))
        self.assertEqual(
            a1.childNodes.length, a2.childNodes.length,
            "Write to one attr reference isn't reflected in another ref.")

    def checkAttrReferenceElementAttributeIntegrity(self):
        "changing an attribute node should be reflected by getAttribute"
        attr = self.document.createAttribute('spam')
        self.document.documentElement.setAttributeNode(attr)
        a1 = self.document.documentElement.attributes.item(0)
        a1.value = 'eggs'
        self.assertEqual(
            self.document.documentElement.getAttribute('spam'), 'eggs',
            "setting value of attr reference isn't reflected by getAttribute")
        a1.appendChild(self.document.createTextNode('ham'))
        self.assertEqual(
            self.document.documentElement.getAttribute('spam'), 'eggsham',
            "appendChild on attr reference isn't reflected by getAttribute.")

    def checkSetAttrWithSubtree(self):
        "setAttributeNode shouldn't lose attr subtree information"
        eggs = self.document.createTextNode('eggs')
        ham = self.document.createTextNode('ham')
        self.attr.appendChild(eggs)
        self.attr.appendChild(ham)
        self.element.setAttributeNode(self.attr)
        # check that getting the attr from the element preserves subtree
        checkAttribute(self.element.attributes.item(0).childNodes, "length", 3)
        self.assert_(
            self.attr.firstChild.nextSibling.isSameNode(eggs),
            "setting an attribute node destroys children")
        self.assert_(
            self.attr.firstChild.nextSibling.nextSibling.isSameNode(ham),
            "setting an attribute node destroys children")
        # check that another ref preserves subtree, too
        attr2 = self.element.getAttributeNode('attrName')
        checkAttribute(attr2.childNodes, "length", 3)
        self.assert_(
            attr2.firstChild.nextSibling.isSameNode(eggs),
            "setting an attribute node destroys children")
        self.assert_(
            attr2.firstChild.nextSibling.nextSibling.isSameNode(ham),
            "setting an attribute node destroys children")

    def checkCloneNode(self):
        attr = self.attr
        clone = attr.cloneNode(0)

        self.failIf(isSameNode(attr, clone),
                    "Clone is same Node as original.")
        checkAttribute(clone, 'value', attr.value)

        # make sure the cloned attr isn't sharing data with the original
        oldValue = self.attr.value
        self.attr.value = 'spam'
        checkAttribute(clone, 'value', oldValue)

# --- Default attributes

class DefaultAttrTestCase(TestCaseBase):

    def setUp(self):
        self.document = self.parse("""
            <!DOCTYPE doc [
                <!ELEMENT doc EMPTY>
                <!ATTLIST doc foo CDATA "bar">
            ]>
            <doc/>
        """)

    def checkHasAttribute(self):
        el = self.document.documentElement

        self.assert_(el.hasAttribute('foo'), 'Default attribute not found.')

    def checkGetAttribute(self):
        el = self.document.documentElement

        self.assertEqual(
            el.getAttribute('foo'), 'bar',
            "Wrong value of default attribute found, expected 'bar', found %s"
            % repr(el.getAttribute('foo')))

    def checkCreateElement(self):
        el = self.document.createElement('doc')

        self.assert_(
            el.hasAttribute('foo'),
            'Newly created Element Node should have default attribute.')
        self.assertEqual(
            el.getAttribute('foo'), 'bar',
            "Wrong value of default attribute found, expected 'bar', found %s"
            % el.getAttribute('foo'))
        checkAttribute(el.getAttributeNode('foo'), 'specified', 0)

    def checkCloneNode(self):
        attr = self.document.documentElement.getAttributeNode('foo')
        clone = attr.cloneNode(0)
        checkAttribute(clone, 'specified', 1)

    def checkCloneNodeElement(self):
        clone = self.document.documentElement.cloneNode(0)
        checkAttribute(clone.getAttributeNode('foo'), 'specified', 0)

        # XXX also check that cloned attrs aren't the same nodes, changes
        # aren't reflected across refs


    def checkRemoveAttribute(self):
        el = self.document.documentElement
        # Replace default with specified attr
        el.setAttribute('foo', 'baz')

        el.removeAttribute('foo')
        self.assert_(
            el.hasAttribute('foo'),
            'Removing specified attribute should restore default attribute.')
        self.assertEqual(
            el.getAttribute('foo'), 'bar',
            "Wrong value of default attribute found, expected 'bar', found %s"
            % el.getAttribute('foo'))
        checkAttribute(el.getAttributeNode('foo'), 'specified', 0)

    def checkRemoveAttributeNode(self):
        el = self.document.documentElement
        newAttr = self.document.createAttribute('foo')
        newAttr.value = 'baz'
        # Replace default with specified attr
        el.setAttributeNode(newAttr)

        el.removeAttributeNode(newAttr)
        self.assert_(
            el.hasAttribute('foo'), 
            'Removing specified attribute should restore default attribute.')
        self.assertEqual(
            el.getAttribute('foo'), 'bar',
            "Wrong value of default attribute found, expected 'bar', found %s"
            % el.getAttribute('foo'))
        checkAttribute(el.getAttributeNode('foo'), 'specified', 0)

    def checkRemoveNamedItem(self):
        el = self.document.documentElement
        # Replace default with specified attr
        el.setAttribute('foo', 'baz')

        el.attributes.removeNamedItem('foo')
        self.assert_(
            el.hasAttribute('foo'),
            'Removing specified attribute should restore default attribute.')
        self.assertEqual(
            el.getAttribute('foo'), 'bar',
            "Wrong value of default attribute found, expected 'bar', found %s"
            % el.getAttribute('foo'))
        checkAttribute(el.getAttributeNode('foo'), 'specified', 0)

    def checkSpecified(self):
        checkAttribute(self.document.documentElement.getAttributeNode('foo'),
            'specified', 0)

    def checkSetAttribute(self):
        el = self.document.documentElement
        el.setAttribute('foo', 'baz')
        checkAttribute(el.getAttributeNode('foo'), 'specified', 1)

    def checkSetAttributeNode(self):
        el = self.document.documentElement
        newAttr = self.document.createAttribute('foo')
        newAttr.value = 'baz'
        el.setAttributeNode(newAttr)
        checkAttribute(el.getAttributeNode('foo'), 'specified', 1)


# --- DocumentFragment

class DocumentFragmentReadTestCase(NodeReadTestCaseBase):

    def setUp(self):
        self.docfrag = self.createDocument().createDocumentFragment()
        self.node = self.docfrag
        self.expectedType = Node.DOCUMENT_FRAGMENT_NODE

    def checkCloneNode(self):
        frag = self.docfrag

        frag.appendChild(self.document.createComment('foo'))
        frag.appendChild(self.document.createTextNode('bar'))

        clone = frag.cloneNode(0)
        deepClone = frag.cloneNode(1)

        self.failIf(isSameNode(frag, clone),
                    "Clone is same Node as original.")
        self.failIf(isSameNode(frag, deepClone),
                    "Clone is same Node as original.")

        checkAttribute(clone, 'parentNode', None)
        checkAttribute(deepClone, 'parentNode', None)
        checkLength(clone.childNodes, 0)
        checkLength(deepClone.childNodes, frag.childNodes.length)

        for i in range(deepClone.childNodes.length):
            checkAttribute(deepClone.childNodes.item(i), 'nodeType',
                frag.childNodes.item(i).nodeType)
            checkAttribute(deepClone.childNodes.item(i), 'data',
                frag.childNodes.item(i).data)


class DocumentFragmentWriteTestCase(NodeWriteTestCaseBase):

    def setUp(self):
        self.createDocument()
        self.docfrag = self.node = self.document.createDocumentFragment()

    def checkInsertBeforeEnd(self):
        doc = self.document
        fragment = self.docfrag
        fragment.appendChild(doc.createElement('foo'))
        fragment.appendChild(doc.createTextNode('textual magic'))
        docelem = doc.documentElement

        docelem.insertBefore(fragment, None)
        checkAttribute(docelem.childNodes[0], "nodeName", "foo")
        checkAttribute(docelem.childNodes[1], "nodeValue", "textual magic")
        checkLength(docelem.childNodes, 2)
        checkAttribute(docelem.firstChild, "nodeName", "foo")


# --- NodeList

class NodeListReadTestCase(TestCaseBase):

    def setUp(self):
        self.createDocument()
        self.list = self.document.createElement("foo")._get_childNodes()

    def checkGetLength(self):
        checkLength(self.list, 0)
        checkLength(self.document.childNodes, 1)

    def checkItem(self):
        self.assert_(self.list.item(0) is None)

    def checkGetItem(self):
        self.assertRaises(xml.dom.IndexSizeErr, self.list[0])

    # there's no cmp for NodeList right now
    #def checkCmp(self):
    #    list1 = self.document.documentElement._get_childNodes()
    #    list2 = self.document.firstChild._get_childNodes()
    #    self.assertEqual(list1, list2,
    #                     "two NodeLists of the same thing don't compare"

##     def checkGetSlice(self):
##         self.assertEqual(self.list[2:5], [])


class NodeListWriteTestCase(TestCaseBase):

    def setUp(self):
        self.createDocument()
        self.list = self.document.childNodes

    def checkGetLength(self):
        checkLength(self.list, 1)
        self.document.appendChild(self.document.createComment('foo'))
        # A NodeList is 'live', changes to source Node should be reflected
        checkLength(self.list, 2)

    def checkItem(self):
        newNode = self.document.createComment('foo')
        self.document.appendChild(newNode)
        # A NodeList is 'live', changes to source Node should be reflected
        isSameNode(newNode, self.list.item(1))

        # This extends to the Nodes contained in the NodeList
        newNode.data = 'bar'
        checkAttribute(self.list.item(1), 'data', 'bar')


# --- NamedNodeMap

class NamedNodeMapReadTestCase(TestCaseBase):

    def setUp(self):
        self.map = self.createDocument().createElement("foo")._get_attributes()

    def checkGetLength(self):
        checkLength(self.map, 0)

    def checkGetNamedItem(self):
        self.assert_(self.map.getNamedItem("uuu") is None)

    def checkRemoveNamedItem(self):
        self.assertRaises(xml.dom.NotFoundErr,
                          self.map.removeNamedItem, "uuu")

    def checkItem(self):
        self.assert_(self.map.item(0) is None)

    def checkGetItem(self):
        try:
            self.map["uuu"]
            self.fail("expected KeyError to be raised")
        except KeyError:
            pass

    def checkGet(self):
        self.assertEqual(self.map.get("uuu", 5), 5)

    def checkHasKey(self):
        self.failIf(self.map.has_key("uuu"))

    def checkItems(self):
        self.assertEqual(self.map.items(), [])

    def checkKeys(self):
        self.assertEqual(self.map.keys(), [])

    def checkValues(self):
        self.assertEqual(self.map.values(), [])


class NonemptyNamedNodeMapWriteTestCase(TestCaseBase):

    def setUp(self):
        self.map = self.createDocument().createElement("foo")._get_attributes()
        self.attribute = self.document.createAttribute("attrName")
        self.attribute.value = "attrValue"
        self.map.setNamedItem(self.attribute)

    def checkRemoveNonexistentNamedItem(self):
        self.assertRaises(xml.dom.DOMException,
                          self.map.removeNamedItem, "uuu")

    def checkRemoveNamedItem(self):
        attribute2 = self.document.createAttribute("attrName2")
        self.map.setNamedItem(attribute2)
        attrOut = self.map.removeNamedItem("attrName2")
        self.assert_(isSameNode(attrOut, attribute2))

    def checkRemoveNamedItemNotFound(self):
        self.assertRaises(xml.dom.NotFoundErr,
                          self.map.removeNamedItem, "bogus")

    def checkGetLength(self):
        checkLength(self.map, 1)

    def checkGetNamedItem(self):
        self.assert_(isSameNode(self.attribute,
                                self.map.getNamedItem("attrName")))

    def checkGetNonexistentNamedItem(self):
        self.assert_(self.map.getNamedItem("uuu") is None)

    def checkItem(self):
        self.assert_(isSameNode(self.map.item(0), self.attribute))
        self.assert_(isSameNode(self.attribute, self.map.item(0)))

    def checkGetNonexistentItem(self):
        try:
            self.map["uuu"]
            self.fail("expected KeyError to be raised")
        except KeyError:
            pass

    def checkGetItem(self):
        self.assert_(isSameNode(self.attribute, self.map["attrName"]))

    def checkGet(self):
        self.assert_(isSameNode(self.attribute, self.map.get("attrName")))

    def checkHasKey(self):
        self.assert_(self.map.has_key("attrName"))
        self.assert_(not self.map.has_key("uuu"))

    def checkItems(self):
        key, node = self.map.items()[0]
        self.assertEqual(key, "attrName")
        self.assert_(isSameNode(self.attribute, node))

    def checkKeys(self):
        self.assertEqual(self.map.keys(), ["attrName"])

    def checkValues(self):
        L = []
        for attr in self.map.values():
            L.append(attr.value)
        self.assertEqual(L, ["attrValue"], "bad values list: %s" % `L`)

    def checkSetNamedItem(self):
        newAttr = self.document.createAttribute('someAttr')
        newAttr.value = 'spam'

        retVal = self.map.setNamedItem(newAttr)
        self.assert_(
            retVal is None,
            "setNamedItem returned %s" % repr(retVal))
        checkLength(self.map, 2)
        self.assert_(
            isSameNode(self.map.getNamedItem('someAttr'), newAttr),
            "setNamedItem store seems to have failed, can't retrieve.")

    def checkSetNamedItemReplacingExistingNode(self):
        newAttr = self.document.createAttribute('someAttr')
        self.map.setNamedItem(newAttr)
        anotherAttr = self.document.createAttribute('someAttr')
        anotherAttr.value = 'eggs'

        retVal = self.map.setNamedItem(newAttr)
        self.assert_(retVal is not None,
                     "setNamedItem returned None")
        self.assert_(isSameNode(retVal, newAttr),
                     "setNamedItem didn't return replaced Node.")
        checkLength(self.map, 2)

    def checkSetNamedItemWrongDocument(self):
        newDoc = self.implementation.createDocument(None, 'foo', None)
        foreignAttr = newDoc.createAttribute('someAttr')
        self.assertRaises(xml.dom.WrongDocumentErr,
                          self.map.setNamedItem, foreignAttr)

    def checkSetNamedItemAlreadyInUse(self):
        el = self.document.createElement('someElement')
        attr = self.document.createAttribute('someAttribute')
        el.setAttributeNode(attr)
        self.assertRaises(xml.dom.InuseAttributeErr,
                          self.map.setNamedItem, attr)

    def checkSetNamedItemHierarchyRequestErr(self):
        # See DOM erratum core-4.
        textNode = self.document.createTextNode('text node')
        self.assertRaises(xml.dom.HierarchyRequestErr,
                          self.map.setNamedItem, textNode)


cases = buildCases(__name__, 'Core', None)
