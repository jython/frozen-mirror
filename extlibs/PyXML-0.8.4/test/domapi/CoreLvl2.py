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
import CoreLvl1
_DOMImplCase = CoreLvl1.DOMImplementationReadTestCase
_NodeTestCaseBase = CoreLvl1.NodeWriteTestCaseBase
del CoreLvl1

import sys
import string
import xml.dom
from xml.dom import Node

# --- DOMIMplementation

class DOMImplementationReadTestCase(TestCaseBase):

    TEST_NAMESPACE = TEST_NAMESPACE
    TEST_PREFIX = 'aprefix'
    TEST_LOCAL_NAME = 'somelocalname'
    TEST_QUALIFIED_NAME = '%s:%s' % (TEST_PREFIX, TEST_LOCAL_NAME)

    def setUp(self):
        # self.implementation is already set.
        pass

    def checkCreateDocument(self):
        # Non namespace Document
        newDoc = self.implementation.createDocument(None, self.TEST_LOCAL_NAME,
            None)

        checkAttribute(newDoc, 'nodeType', Node.DOCUMENT_NODE)
        checkAttribute(newDoc, 'doctype', None)
        checkAttributeNot(newDoc, 'documentElement', None)
        self.assert_(newDoc.implementation is self.implementation,
                     'Created Document has different implementation.')
        checkAttribute(newDoc.documentElement, 'namespaceURI', None)
        checkAttribute(newDoc.documentElement, 'tagName', self.TEST_LOCAL_NAME)

    def checkCreateDocumentWithNamespace(self):
        newDoc = self.implementation.createDocument(self.TEST_NAMESPACE,
            self.TEST_QUALIFIED_NAME, None)

        checkAttribute(newDoc.documentElement, 'namespaceURI',
            self.TEST_NAMESPACE)
        checkAttribute(newDoc.documentElement, 'tagName',
            self.TEST_QUALIFIED_NAME)

    def checkCreateDocumentWithDocumentType(self):
        docType = self.implementation.createDocumentType(
            self.TEST_QUALIFIED_NAME, 'uri:public', 'uri:system')
        newDoc = self.implementation.createDocument(None, self.TEST_LOCAL_NAME,
            docType)

        checkAttributeSameNode(newDoc, 'doctype', docType)

    def checkCreateDocumentIllegalCharacterErr(self):
        self.assertRaises(xml.dom.InvalidCharacterErr,
                          self.implementation.createDocument,
                          self.TEST_NAMESPACE, '4_prefix:5_illegal', None)

    def checkCreateDocumentMalformedQA(self):
        self.assertRaises(xml.dom.NamespaceErr,
                          self.implementation.createDocument,
                          self.TEST_NAMESPACE, 'malformed:qualfied:name', None)
        self.assertRaises(xml.dom.NamespaceErr,
                          self.implementation.createDocument,
                          self.TEST_NAMESPACE, ':malformed_qn', None)

    def checkCreateDocumentWithPrefixNoNamespace(self):
        self.assertRaises(xml.dom.NamespaceErr,
                          self.implementation.createDocument,
                          None, self.TEST_QUALIFIED_NAME, None)

    def checkCreateDocumentWithXMLPrefixWrongNamespace(self):
        self.assertRaises(xml.dom.NamespaceErr,
                          self.implementation.createDocument,
                          self.TEST_NAMESPACE, 'xml:nope', None)

    def checkCreateDocumentWithUsedDocType(self):
        docType = self.implementation.createDocumentType(
            self.TEST_QUALIFIED_NAME, 'uri:public', 'uri:system')
        self.implementation.createDocument(None, self.TEST_LOCAL_NAME,
            docType)

        self.assertRaises(xml.dom.WrongDocumentErr,
                          self.implementation.createDocument,
                          None, self.TEST_LOCAL_NAME, docType)

    def checkCreateDocumentType(self):
        docType = self.implementation.createDocumentType(
            self.TEST_QUALIFIED_NAME, 'uri:public', 'uri:system')

        checkAttribute(docType, 'ownerDocument', None)
        checkAttribute(docType, 'name', self.TEST_QUALIFIED_NAME)
        checkAttribute(docType, 'publicId', 'uri:public')
        checkAttribute(docType, 'systemId', 'uri:system')

        checkLength(docType.entities, 0)
        checkLength(docType.notations, 0)

    def checkCreateDocumentTypeIllegalCharacterErr(self):
        self.assertRaises(xml.dom.InvalidCharacterErr,
                          self.implementation.createDocumentType,
                          '4_prefix:5_illegal', 'uri:public', 'uri:system')

    def checkCreateDocumentTypeMalformedQA(self):
        self.assertRaises(xml.dom.NamespaceErr,
                          self.implementation.createDocumentType,
                          'malformed:qualfied:name', 'uri:public',
                          'uri:system')
        self.assertRaises(xml.dom.NamespaceErr,
                          self.implementation.createDocumentType,
                          ':malformed_qn', 'uri:public', 'uri:system')


# --- Node

class NodeReadTestCaseBase(TestCaseBase):

    TEST_NAMESPACE = TEST_NAMESPACE
    TEST_PREFIX = 'aprefix'
    TEST_LOCAL_NAME = 'somelocalname'
    TEST_QUALIFIED_NAME = '%s:%s' % (TEST_PREFIX, TEST_LOCAL_NAME)

    def checkLocalName(self):
        if self.node.nodeType in (Node.ATTRIBUTE_NODE,
                Node.ELEMENT_NODE):
            expect = self.TEST_LOCAL_NAME
            noNS = self.nodeNoNS
        else:
            expect = None
            noNS = None

        checkAttribute(self.node, 'localName', expect)
        checkReadOnly(self.node, 'localName')

        if noNS:
            checkAttribute(noNS, 'localName', None)

    def checkNameSpaceURI(self):
        if self.node.nodeType in (Node.ATTRIBUTE_NODE,
                Node.ELEMENT_NODE):
            expect = self.TEST_NAMESPACE
            noNS = self.nodeNoNS
        else:
            expect = None
            noNS = None

        checkAttribute(self.node, 'namespaceURI', expect)
        checkReadOnly(self.node, 'namespaceURI')

        if noNS:
            checkAttribute(noNS, 'namespaceURI', None)

    def checkOwnerDocument(self):
        if self.node.nodeType in (Node.DOCUMENT_NODE,
                Node.DOCUMENT_TYPE_NODE):
            expect = None

        else:
            expect = self.document

        checkAttributeSameNode(self.node, 'ownerDocument', expect)
        checkReadOnly(self.node, 'ownerDocument')

    def checkPrefix(self):
        if self.node.nodeType in (Node.ATTRIBUTE_NODE,
                Node.ELEMENT_NODE):
            expect = self.TEST_PREFIX
            noNS = self.nodeNoNS
        else:
            expect = None
            noNS = None

        checkAttribute(self.node, 'prefix', expect)

        if noNS:
            checkAttribute(noNS, 'prefix', None)

    def hasAttributes(self):
        self.failIf(self.node.hasAttributes(),
                    "hasAttributes returned 'true' when 'false' was expected.")

    featureMatrix = _DOMImplCase.featureMatrix

    def checkIsSupported(self):
        for feature, level in self.featureMatrix:
            result1 = self.node.isSupported(feature, level)
            result2 = self.node.isSupported(string.upper(feature), level)
            result3 = self.node.isSupported(string.lower(feature), level)

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


class NodeWriteTestCaseBase(TestCaseBase):

    TEST_NAMESPACE = NodeReadTestCaseBase.TEST_NAMESPACE
    TEST_PREFIX = NodeReadTestCaseBase.TEST_PREFIX
    TEST_LOCAL_NAME = NodeReadTestCaseBase.TEST_LOCAL_NAME
    TEST_QUALIFIED_NAME = NodeReadTestCaseBase.TEST_QUALIFIED_NAME

    readOnlyNodeList = _NodeTestCaseBase.readOnlyNodeList

    def checkPrefix(self):
        # Nodetypes that are read-only.
        if self.node.nodeType in self.readOnlyNodeList:
            checkReadOnly(self.node, 'nodeValue')
            return

        # Nodetypes that should ignore changes.
        if self.node.nodeType not in (Node.ATTRIBUTE_NODE,
                Node.ELEMENT_NODE):
            self.node.prefix = "Ignore_this"
            checkAttribute(self.node, "prefix", None)
            return

        # All other node types
        self.node.prefix = 'foo'
        checkAttribute(self.node, 'prefix', 'foo')
        checkAttribute(self.node, 'nodeName', 'foo:%s' % self.TEST_LOCAL_NAME)

        # Changing the prefix also changes other attributes
        newQualifiedName = '%s:%s' % ('foo', self.TEST_LOCAL_NAME)
        checkAttribute(self.node, 'nodeName', newQualifiedName)
        if self.node.nodeType == Node.ATTRIBUTE_NODE:
            checkAttribute(self.node, 'name', newQualifiedName)
        else:
            checkAttribute(self.node, 'tagName', newQualifiedName)

    def checkPrefixInvalidCharacter(self):
        if self.node.nodeType in self.readOnlyNodeList:
            return

        if self.node.nodeType not in (Node.ATTRIBUTE_NODE,
                Node.ELEMENT_NODE):
            return

        try:
            self.node.prefix = '5_illegal_prefix'
        except xml.dom.InvalidCharacterErr:
            pass
        else:
            self.fail("Setting of illegal prefix succeeded.")

    def checkPrefixMalformedPrefix(self):
        if self.node.nodeType in self.readOnlyNodeList:
            return

        if self.node.nodeType not in (Node.ATTRIBUTE_NODE,
                Node.ELEMENT_NODE):
            return

        try:
            self.node.prefix = ':prefix_with_colon'
        except xml.dom.NamespaceErr:
            pass
        else:
            self.fail("Setting of malformed prefix with ':' succeeded.")

    def checkPrefixNamespaceErr(self):
        if self.node.nodeType in self.readOnlyNodeList:
            return

        if self.node.nodeType not in (Node.ATTRIBUTE_NODE,
                Node.ELEMENT_NODE):
            return

        try:
            self.nodeNoNS.prefix = 'foo'
        except xml.dom.NamespaceErr:
            pass
        else:
            self.fail('Changing prefix on Node without namespace succeeded.')

    def checkPrefixXMLNamespace(self):
        if self.node.nodeType in self.readOnlyNodeList:
            return

        if self.node.nodeType not in (Node.ATTRIBUTE_NODE,
                Node.ELEMENT_NODE):
            return

        try:
            self.node.prefix = 'xml'
        except xml.dom.NamespaceErr:
            pass
        else:
            self.fail("Changing prefix to 'xml' on Node without"
                      " W3C XML namespace succeeded.")

    def checkPrefixXMLNSNamespace(self):
        if self.node.nodeType in self.readOnlyNodeList:
            return

        if self.node.nodeType not in (Node.ATTRIBUTE_NODE, Node.ELEMENT_NODE):
            return

        if self.node.nodeType == Node.ATTRIBUTE_NODE:
            try:
                self.node.prefix = 'xmlns'
            except xml.dom.NamespaceErr:
                pass
            else:
                self.fail("Changing prefix to 'xmlns' on Attribute without"
                          " W3C XML Namespaces namespace succeeded.")


# --- Document

class DocumentReadTestCase(NodeReadTestCaseBase):

    def setUp(self):
        self.node = self.createDocumentNS()

    def checkImportNode(self):
        foreignDoc = self.implementation.createDocument(None, 'foo', None)
        self.assertRaises(xml.dom.NotSupportedErr,
                          foreignDoc.importNode, self.document, 0)


class DocumentWriteTestCase(NodeWriteTestCaseBase):

    def setUp(self):
        self.node = self.createDocumentNS()

    def checkGetElementsByTagNameNS(self):
        doc = self.document

        elements = {}
        names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        for c in names:
            elements[c + '1'] = doc.createElementNS('uri:1', 'one:' + c)
            elements[c + '2'] = doc.createElementNS('uri:2', 'two:' + c)
        # set up simple tree
        elements['a1'].appendChild(elements['a2'])
        elements['a1'].appendChild(elements['b1'])
        elements['a1'].appendChild(elements['d1'])
        elements['b1'].appendChild(elements['b2'])
        elements['b1'].appendChild(elements['c1'])
        elements['c1'].appendChild(elements['c2'])
        elements['d1'].appendChild(elements['d2'])
        elements['d1'].appendChild(elements['e1'])
        elements['d1'].appendChild(elements['h1'])
        elements['e1'].appendChild(elements['e2'])
        elements['e1'].appendChild(elements['f1'])
        elements['e1'].appendChild(elements['g1'])
        elements['f1'].appendChild(elements['f2'])
        elements['g1'].appendChild(elements['g2'])
        elements['h1'].appendChild(elements['h2'])
        elements['h1'].appendChild(elements['i1'])
        elements['i1'].appendChild(elements['i2'])

        doc.documentElement.appendChild(elements['a1'])

        # now test

        # find all elements in the right order
        result = doc.getElementsByTagNameNS('*', '*')
        allnames = []
        add = allnames.append
        for name in names:
            add(name)
            add(name)
        self.assertEqual(len(result), len(allnames) + 1)
        for name, element in map(None, allnames, result[1:]):
            self.assertEqual(name, element.localName)

        # find all elements in one namespace in the right order
        result = doc.getElementsByTagNameNS('uri:1', '*')
        self.assertEqual(len(result), len(names))
        for name, element in map(None, names, result):
            self.assertEqual(name, element.localName)

        # find single element, top
        result = doc.getElementsByTagNameNS('uri:1', 'a')
        checkLength(result, 1)
        self.assertEqual(result[0].tagName, 'one:a')

        # find single element somewhere in tree
        result = doc.getElementsByTagNameNS('uri:2', 'h')
        checkLength(result, 1)
        self.assertEqual(result[0].tagName, 'two:h')

        # find elements in the tree from all namespaces
        result = doc.getElementsByTagNameNS('*', 'f')
        checkLength(result, 2)
        self.assertEqual(result[0].tagName, 'one:f')
        self.assertEqual(result[1].tagName, 'two:f')

    def checkNormalize(self):
        doc = self.document
        docEl = doc.documentElement

        # First build a tree with adjacent and empty Text nodes, intermingled
        # with other Nodes.
        docEl.appendChild(doc.createTextNode('This'))
        docEl.appendChild(doc.createTextNode(''))
        docEl.appendChild(doc.createTextNode(' is'))
        docEl.appendChild(doc.createTextNode(' '))
        docEl.appendChild(doc.createTextNode('a test.'))

        docEl.appendChild(doc.createCDATASection("Don't merge"))
        docEl.appendChild(doc.createTextNode('1'))

        docEl.appendChild(doc.createComment('foo'))
        docEl.appendChild(doc.createTextNode('2'))

        subEl = doc.createElement('baz')
        attr = doc.createAttribute('eggs')
        subEl.setAttributeNode(attr)
        docEl.appendChild(subEl)

        subEl.appendChild(doc.createTextNode('To '))
        subEl.appendChild(doc.createTextNode(''))
        subEl.appendChild(doc.createTextNode('be or'))

        subEl.appendChild(doc.createEntityReference('amp'))

        subEl.appendChild(doc.createTextNode('not '))
        subEl.appendChild(doc.createTextNode('to'))
        subEl.appendChild(doc.createTextNode(' be'))

        attr.appendChild(doc.createTextNode('Spanish '))
        attr.appendChild(doc.createTextNode('Inquisition'))

        docEl.appendChild(doc.createTextNode('3'))

        docEl.appendChild(doc.createProcessingInstruction('bar', 'spam'))
        docEl.appendChild(doc.createTextNode('4'))

        # Now test
        doc.normalize()

        checkLength(docEl.childNodes, 9)
        checkLength(subEl.childNodes, 3)
        checkLength(attr.childNodes, 1)

        checkAttribute(docEl.childNodes[0], 'nodeType', Node.TEXT_NODE)
        checkAttribute(docEl.childNodes[0], 'data', 'This is a test.')

        checkAttribute(docEl.childNodes[1], 'nodeType',
                       Node.CDATA_SECTION_NODE)
        checkAttribute(docEl.childNodes[2], 'nodeType', Node.TEXT_NODE)
        checkAttribute(docEl.childNodes[3], 'nodeType',
                       Node.COMMENT_NODE)
        checkAttribute(docEl.childNodes[4], 'nodeType', Node.TEXT_NODE)
        checkAttribute(docEl.childNodes[5], 'nodeType',
                       Node.ELEMENT_NODE)
        checkAttribute(docEl.childNodes[6], 'nodeType', Node.TEXT_NODE)
        checkAttribute(docEl.childNodes[7], 'nodeType',
                       Node.PROCESSING_INSTRUCTION_NODE)
        checkAttribute(docEl.childNodes[8], 'nodeType', Node.TEXT_NODE)

        checkAttribute(subEl.childNodes[0], 'nodeType', Node.TEXT_NODE)
        checkAttribute(subEl.childNodes[1], 'nodeType',
                       Node.ENTITY_REFERENCE_NODE)
        checkAttribute(subEl.childNodes[2], 'nodeType', Node.TEXT_NODE)

        checkAttribute(subEl.childNodes[0], 'data', 'To be or')
        checkAttribute(subEl.childNodes[2], 'data', 'not to be')

        checkAttribute(attr.childNodes[0], 'data', 'Spanish Inquisition')

    def checkCreateAttributeNS(self):
        attr = self.document.createAttributeNS(self.TEST_NAMESPACE,
                                               self.TEST_QUALIFIED_NAME)

        checkAttribute(attr, 'nodeType', Node.ATTRIBUTE_NODE)
        checkAttribute(attr, 'name', self.TEST_QUALIFIED_NAME)
        checkAttribute(attr, 'localName', self.TEST_LOCAL_NAME)
        checkAttribute(attr, 'prefix', self.TEST_PREFIX)
        checkAttribute(attr, 'namespaceURI', self.TEST_NAMESPACE)
        checkAttribute(attr, 'value', '')
        checkAttributeSameNode(attr, 'ownerDocument', self.document)

    def checkCreateAttributeNSNoPrefix(self):
        attr = self.document.createAttributeNS(self.TEST_NAMESPACE,
                                               self.TEST_LOCAL_NAME)

        checkAttribute(attr, 'name', self.TEST_LOCAL_NAME)
        checkAttribute(attr, 'localName', self.TEST_LOCAL_NAME)
        checkAttribute(attr, 'prefix', None)
        checkAttribute(attr, 'namespaceURI', self.TEST_NAMESPACE)

    def checkCreateAttributeNSIllegalCharacter(self):
        self.assertRaises(xml.dom.InvalidCharacterErr,
                          self.document.createAttributeNS,
                          self.TEST_NAMESPACE, '4_prefix:5_illegal')

    def checkCreateAttributeNSMalformedQA(self):
        self.assertRaises(xml.dom.NamespaceErr,
                          self.document.createAttributeNS,
                          self.TEST_NAMESPACE, 'malformed:qualfied:name')

        self.assertRaises(xml.dom.NamespaceErr,
                          self.document.createAttributeNS,
                          self.TEST_NAMESPACE, ':malformed_qn')

    def checkCreateAttributeNSPrefixNoNamespace(self):
        self.assertRaises(xml.dom.NamespaceErr,
                          self.document.createAttributeNS,
                          None, self.TEST_QUALIFIED_NAME)

    def checkCreateAttributeNSXMLNamespace(self):
        self.assertRaises(xml.dom.NamespaceErr,
                          self.document.createAttributeNS,
                          self.TEST_NAMESPACE, 'xml:nope')

    def checkCreateAttributeNSXMLNamespace(self):
        self.assertRaises(xml.dom.NamespaceErr,
                          self.document.createAttributeNS,
                          self.TEST_NAMESPACE, 'xmlns:nope')

    def checkCreateElementNS(self):
        el = self.document.createElementNS(self.TEST_NAMESPACE,
                                           self.TEST_QUALIFIED_NAME)

        checkAttribute(el, 'nodeType', Node.ELEMENT_NODE)
        checkAttribute(el, 'tagName', self.TEST_QUALIFIED_NAME)
        checkAttribute(el, 'localName', self.TEST_LOCAL_NAME)
        checkAttribute(el, 'prefix', self.TEST_PREFIX)
        checkAttribute(el, 'namespaceURI', self.TEST_NAMESPACE)
        checkAttributeSameNode(el, 'ownerDocument', self.document)

    def checkCreateElementNSNoPrefix(self):
        el = self.document.createElementNS(self.TEST_NAMESPACE,
                                           self.TEST_LOCAL_NAME)

        checkAttribute(el, 'tagName', self.TEST_LOCAL_NAME)
        checkAttribute(el, 'localName', self.TEST_LOCAL_NAME)
        checkAttribute(el, 'prefix', None)
        checkAttribute(el, 'namespaceURI', self.TEST_NAMESPACE)

    def checkCreateElementNSIllegalCharacter(self):
        self.assertRaises(xml.dom.InvalidCharacterErr,
                          self.document.createElementNS,
                          self.TEST_NAMESPACE, '4_prefix:5_illegal')

    def checkCreateElementNSMalformedQA(self):
        self.assertRaises(xml.dom.NamespaceErr,
                          self.document.createElementNS,
                          self.TEST_NAMESPACE, 'malformed:qualfied:name')
        self.assertRaises(xml.dom.NamespaceErr,
                          self.document.createElementNS,
                          self.TEST_NAMESPACE, ':malformed_qn')

    def checkCreateElementNSPrefixNoNamespace(self):
        self.assertRaises(xml.dom.NamespaceErr,
                          self.document.createElementNS,
                          None, self.TEST_QUALIFIED_NAME)

    def checkCreateElementNSXMLNamespace(self):
        self.assertRaises(xml.dom.NamespaceErr,
                          self.document.createElementNS,
                          self.TEST_NAMESPACE, 'xml:nope')


class GetElementByIdTestCase(TestCaseBase):

    PROLOGUE = """\
<!DOCTYPE idtest [
  <!ELEMENT idtest EMPTY>
  <!ATTLIST idtest
            id   ID   #IMPLIED
    >
]>
"""

    def setup(self):
        pass

    def checkWithoutId(self):
        doc = self.parse(self.PROLOGUE + "<idtest/>")
        self.assert_(doc.getElementById("foo") is None)

    def checkWithDifferentId(self):
        doc = self.parse(self.PROLOGUE + "<idtest id='bar'/>")
        self.assert_(doc.getElementById("foo") is None)

    def checkWithIdOnRootElement(self):
        doc = self.parse(self.PROLOGUE + "<idtest id='foo'/>")
        self.assert_(isSameNode(doc.getElementById("foo"),
                                doc.documentElement))

    def checkWithIdOnChildElement(self):
        doc = self.parse(self.PROLOGUE
                         + "<idtest><idtest id='foo'/></idtest>")
        self.assert_(isSameNode(doc.getElementById("foo"),
                                doc.documentElement.firstChild))


# --- Element

class ElementReadTestCase(NodeReadTestCaseBase):

    def setUp(self):
        doc = self.createDocument()
        self.element = self.nodeNoNS = self.elementNoNS = doc.createElement(
            self.TEST_LOCAL_NAME)
        self.elementNS = self.node = doc.createElementNS(
            self.TEST_NAMESPACE, self.TEST_QUALIFIED_NAME)

    def checkGetAttributeNS(self):
        self.assertEqual(self.element.getAttributeNS("uri:bugga", "ugga"), "",
                         "non-existant attribute should return ''")

    def checkGetAttributeNodeNS(self):
        self.assert_(
            self.element.getAttributeNodeNS("uri:bugga", "ugga") is None,
            "non-existant attribute should return None")

    def checkCloneNode(self):
        el = self.element
        clone = el.cloneNode(0)

        self.failIf(isSameNode(el, clone), "Clone is same Node as original.")
        checkAttribute(clone, 'localName', el.localName)
        checkAttribute(clone, 'namespaceURI', el.namespaceURI)
        checkAttribute(clone, 'prefix', el.prefix)

    def checkImportNode(self):
        el = self.element
        doc = self.document

        el.appendChild(doc.createTextNode('A Text Node'))
        el.appendChild(doc.createComment('A Comment'))
        el.setAttribute('attr1', 'An attribute')
        el.setAttribute('attr2', 'Another attribute')

        foreignDoc = self.implementation.createDocument(None, 'foo', None)

        clone = foreignDoc.importNode(self.element, 0)
        deepClone = foreignDoc.importNode(self.element, 1)

        self.failIf(isSameNode(el, clone),
                    "Clone is same Node as original.")
        self.failIf(isSameNode(el, deepClone),
                    "Clone is same Node as original.")

        checkAttributeSameNode(clone, 'ownerDocument', foreignDoc)
        checkAttributeSameNode(deepClone, 'ownerDocument', foreignDoc)
        checkAttribute(clone, 'parentNode', None)
        checkAttribute(deepClone, 'parentNode', None)
        checkLength(clone.childNodes, 0)
        checkLength(deepClone.childNodes, el.childNodes.length)
        checkLength(clone.attributes, el.attributes.length)
        checkLength(deepClone.attributes, el.attributes.length)

        checkAttribute(clone, 'nodeName', el.nodeName)
        checkAttribute(deepClone, 'nodeName', el.nodeName)
        checkAttribute(clone, 'nodeType', el.nodeType)
        checkAttribute(deepClone, 'nodeType', el.nodeType)
        checkAttribute(clone, 'nodeValue', el.nodeValue)
        checkAttribute(deepClone, 'nodeValue', el.nodeValue)

        for i in range(deepClone.childNodes.length):
            checkAttribute(deepClone.childNodes.item(i), 'nodeType',
                el.childNodes.item(i).nodeType)
            checkAttributeSameNode(deepClone.childNodes.item(i),
                'ownerDocument', foreignDoc)
            if deepClone.childNodes.item(i).nodeType != Node.ELEMENT_NODE:
                checkAttribute(deepClone.childNodes.item(i), 'data',
                    el.childNodes.item(i).data)

        for i in range(deepClone.attributes.length):
            checkAttribute(clone.attributes.item(i), 'name',
                el.attributes.item(i).name)
            checkAttribute(deepClone.attributes.item(i), 'name',
                el.attributes.item(i).name)

            checkAttribute(clone.attributes.item(i), 'value',
                el.attributes.item(i).value)
            checkAttribute(deepClone.attributes.item(i), 'value',
                el.attributes.item(i).value)

            checkAttributeSameNode(clone.attributes.item(i), 'ownerElement',
                clone)
            checkAttributeSameNode(deepClone.attributes.item(i),
                'ownerElement', deepClone)


class ElementWriteTestCase(NodeWriteTestCaseBase):

    def setUp(self):
        doc = self.createDocument()
        self.element = self.nodeNoNS = self.elementNoNS = doc.createElement(
            self.TEST_LOCAL_NAME)
        self.elementNS = self.node = doc.createElementNS(self.TEST_NAMESPACE,
            self.TEST_QUALIFIED_NAME)

    def checkHasAttribute(self):
        self.failIf(self.element.hasAttribute('ugga'),
                    "Test for non-exisiting attribute returned true.")

        self.element.setAttribute("ugga", "foo")

        self.assert_(self.element.hasAttribute('ugga'),
                     "Test for exisiting attribute returned false.")

    def checkSetAttributeNS(self):
        self.element.setAttributeNS("uri:bugga", "b:ugga", "foo")
        self.element.setAttributeNS("uri:bar", "bar:ugga", "baz")

        self.assert_(self.element.hasAttributeNS("uri:bar", "ugga"),
                     "Test for presence of created attribute returned false.")
        value = self.element.getAttributeNS("uri:bugga", "ugga")
        self.assertEqual(value, 'foo',
                         "Incorrect attr value returned. Expected 'foo', got "
                         + repr(value))
        node = self.element.getAttributeNodeNS("uri:bugga", "ugga")
        self.assertEqual(node.prefix, 'b',
                         "New Attr has incorrect prefix, expected 'b', got "
                         + repr(node.prefix))

    #"Note that because the DOM does no lexical checking, the empty string
    #will be treated as a real namespace URI in DOM Level 2 methods.
    #Applications must use the value null as the namespaceURI parameter for
    #methods if they wish to have no namespace." - the rec
    # The NamespaceURI must be a namespace name, which Namespaces in XML
    # states is a URI reference.  I'm assuming that "" is not a valid URI
    # reference, so we're not testing using that.
    def checkSetAttributeEmptyNS(self):
        self.element.setAttributeNS(None, "ugga", "foo")

        self.assert_(self.element.hasAttributeNS(None, "ugga"),
                     "Test for presence of created attribute returned false.")
        value = self.element.getAttributeNS(None, "ugga")
        self.assertEqual(value, 'foo',
                         "Incorrect attr value returned. Expected 'foo', got "
                         + repr(value))
        node = self.element.getAttributeNodeNS(None, "ugga")
        self.assert_(node.prefix is None,
                     "New Attr node has incorrect prefix, expected None, got "
                     + repr(node.prefix))

    def checkSetAttributeNSDifferentPrefix(self):
        self.element.setAttributeNS("uri:bugga", "b:ugga", "foo")
        self.element.setAttributeNS("uri:bar", "bar:ugga", "baz")

        self.element.setAttributeNS("uri:bugga", "c:ugga", "new value")

        self.assert_(self.element.hasAttributeNS("uri:bar", "ugga"),
                     "Test for presence of created attribute returned false.")
        value = self.element.getAttributeNS("uri:bugga", "ugga")
        self.assertEqual(
            value, 'new value',
            "Wrong attr value returned. Expected 'new value', got "
            + repr(value))
        node = self.element.getAttributeNodeNS("uri:bugga", "ugga")
        self.assertEqual(node.prefix, 'c',
                         "New Attr has incorrect prefix, expected 'c', got "
                         + repr(node.prefix))

    def checkSetAttributeNSNoPrefix(self):
        self.element.setAttributeNS(TEST_NAMESPACE, 'foo', 'bar')

        self.assert_(self.element.hasAttributeNS(TEST_NAMESPACE, "foo"),
                     "Test for presence of created attribute returned false.")
        value = self.element.getAttributeNS(TEST_NAMESPACE, "foo")
        self.assertEqual(value, 'bar',
                         "Incorrect attr value returned. Expected 'bar', got "
                         + repr(value))
        node = self.element.getAttributeNodeNS(TEST_NAMESPACE, "foo")
        checkAttribute(node, 'prefix', None)

    def checkSetAttributeNSXMLNSDeclaration(self):
        XMLNSNamespace = 'http://www.w3.org/2000/xmlns/'
        self.element.setAttributeNS(XMLNSNamespace, 'xmlns', TEST_NAMESPACE)

        self.assert_(
            self.element.hasAttributeNS(XMLNSNamespace, "xmlns"),
            "Test for presence of created xmlns attribute returned false.")
        value = self.element.getAttributeNS(XMLNSNamespace, "xmlns")
        self.assertEqual(value, TEST_NAMESPACE,
                         "Incorrect attr value returned. Expected %s, got "
                         + repr((`TEST_NAMESPACE`, `value`)))
        node = self.element.getAttributeNodeNS(XMLNSNamespace, "xmlns")
        checkAttribute(node, 'prefix', None)

    def checkSetAttributeNSIllegalCharacter(self):
        self.assertRaises(xml.dom.InvalidCharacterErr,
                          self.element.setAttributeNS,
                          "uri:bugga", "5_b:ugga", "illegal")

    def checkSetAttributeNSMalformedQA(self):
        self.assertRaises(xml.dom.NamespaceErr,
                          self.element.setAttributeNS,
                          "uri:bugga", 'malformed:qualfied:name', "malformed")
        self.assertRaises(xml.dom.NamespaceErr,
                          self.element.setAttributeNS,
                          "uri:bugga", ':malformed_qn', "malformed")

    def checkSetAttributeNSPrefixNoNamespace(self):
        self.assertRaises(xml.dom.NamespaceErr,
                          self.element.setAttributeNS,
                          None, 'prefix:localName', 'Nono')

    def checkSetAttributeNSXMLNamespace(self):
        self.assertRaises(xml.dom.NamespaceErr,
                          self.element.setAttributeNS,
                          'uri:unknown', 'xml:localName', 'Nono')

    def checkSetAttributeNSXMLNSNamespace(self):
        self.assertRaises(xml.dom.NamespaceErr,
                          self.element.setAttributeNS,
                          'uri:unknown', 'xmlns:localName', 'No')

    def checkSetAttributeNodeNS(self):
        node1 = self.document.createAttributeNS("uri:bugga", "b:ugga")
        node1.value = 'foo'
        node2 = self.document.createAttributeNS("uri:bar", "bar:ugga")
        returnValue = self.element.setAttributeNode(node1)
        self.element.setAttributeNode(node2)

        self.assert_(returnValue is None,
                     "setAttributeNodeNS returned " + repr(returnValue))

        self.assert_(self.element.hasAttributeNS("uri:bar", "ugga"),
                     "Test for presence of created attribute returned false.")

        value = self.element.getAttributeNS("uri:bugga", "ugga")
        self.assertEqual(value, 'foo',
                         "Incorrect attr value returned. Expected 'foo', got "
                         + repr(value))

        node = self.element.getAttributeNodeNS("uri:bugga", "ugga")
        self.assert_(isSameNode(node1, node),
                     "Incorrect node returned from getAttributeNodeNS.")

    def checkSetAttributeNodeNSReplaceExisting(self):
        # Try a new node with same namespaceURI and localname, but differing
        # prefix. This should replace the existing node, returning it.
        node1 = self.document.createAttributeNS("uri:bugga", "b:ugga")
        self.element.setAttributeNode(node1)
        node2 = self.document.createAttributeNS("uri:bugga", "c:ugga")

        returnValue = self.element.setAttributeNodeNS(node2)
        self.failIf(returnValue is None,
                    "setAttributeNodeNS did not replace original attribute")
        self.assert_(isSameNode(node1, returnValue),
                     "setAttributeNodeNS returned " + repr(returnValue))

    def checkSetAttributeNodeNSWrongDocument(self):
        foreignDoc = self.implementation.createDocument(None, 'foo', None)
        foreignAttr = foreignDoc.createAttributeNS('uri:spam', 'spam:eggs')
        self.assertRaises(xml.dom.WrongDocumentErr,
                          self.element.setAttributeNodeNS, foreignAttr)

    def checkSetAttributeNodeNSAlreadyInUse(self):
        otherElement = self.document.createElement('foo')
        otherAttr = self.document.createAttributeNS('uri:spam', 'spam:eggs')
        otherElement.setAttributeNodeNS(otherAttr)
        self.assertRaises(xml.dom.InuseAttributeErr,
                          self.element.setAttributeNodeNS, otherAttr)

    def checkRemoveAttributeNS(self):
        node1 = self.document.createAttributeNS("uri:bugga", "b:ugga")
        node2 = self.document.createAttributeNS("uri:bar", "bar:ugga")
        self.element.setAttributeNode(node1)
        self.element.setAttributeNode(node2)

        self.element.removeAttributeNS("uri:bugga", "ugga")

        self.failIf(
            self.element.hasAttributeNS("uri:bugga", "ugga"),
            "Test for presence of created attribute still returns true.")

        self.assert_(
            self.element.hasAttributeNS("uri:bar", "ugga"),
            "Test for presence of created attribute returned false.")

    def checkGetElementsByTagNameNS(self):
        doc = self.document
        el = self.element

        elements = {}
        names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        for c in names:
            elements[c + '1'] = doc.createElementNS('uri:1', 'one:' + c)
            elements[c + '2'] = doc.createElementNS('uri:2', 'two:' + c)
        # set up simple tree
        elements['a1'].appendChild(elements['a2'])
        elements['a1'].appendChild(elements['b1'])
        elements['a1'].appendChild(elements['d1'])
        elements['b1'].appendChild(elements['b2'])
        elements['b1'].appendChild(elements['c1'])
        elements['c1'].appendChild(elements['c2'])
        elements['d1'].appendChild(elements['d2'])
        elements['d1'].appendChild(elements['e1'])
        elements['d1'].appendChild(elements['h1'])
        elements['e1'].appendChild(elements['e2'])
        elements['e1'].appendChild(elements['f1'])
        elements['e1'].appendChild(elements['g1'])
        elements['f1'].appendChild(elements['f2'])
        elements['g1'].appendChild(elements['g2'])
        elements['h1'].appendChild(elements['h2'])
        elements['h1'].appendChild(elements['i1'])
        elements['i1'].appendChild(elements['i2'])

        el.appendChild(elements['a1'])

        # now test

        # find all elements in the right order
        result = el.getElementsByTagNameNS('*', '*')
        allnames = []
        add = allnames.append
        for name in names:
            add(name)
            add(name)
        self.assertEqual(len(result), len(allnames))
        for name, element in map(None, allnames, result):
            self.assertEqual(name, element.localName)

        # find all elements in one namespace in the right order
        result = el.getElementsByTagNameNS('uri:1', '*')
        self.assertEqual(len(result), len(names))
        for name, element in map(None, names, result):
            self.assertEqual(name, element.localName)

        # find single element, top
        result = el.getElementsByTagNameNS('uri:1', 'a')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].tagName, 'one:a')

        # find single element somewhere in tree
        result = el.getElementsByTagNameNS('uri:2', 'h')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].tagName, 'two:h')

        # find elements in the tree from all namespaces
        result = el.getElementsByTagNameNS('*', 'f')
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].tagName, 'one:f')
        self.assertEqual(result[1].tagName, 'two:f')

    def checkNormalize(self):
        doc = self.document
        el = self.element

        # Build test nodes
        el1 = el.appendChild(doc.createElement('e1'))
        el2 = el.appendChild(doc.createElement('e2'))

        el1.appendChild(doc.createTextNode('foo'))
        el1.appendChild(doc.createTextNode('bar'))

        el2.appendChild(doc.createTextNode('spam'))
        el2.appendChild(doc.createTextNode('eggs'))

        # Now test
        # Only normalize on element, sibling should be unaffected
        el1.normalize()

        checkAttribute(el1.childNodes, 'length', 1)
        checkAttribute(el2.childNodes, 'length', 2)

        checkAttribute(el1.childNodes[0], 'data', 'foobar')

        # Now normalize the whole test tree
        el.normalize()

        checkAttribute(el1.childNodes, 'length', 1)
        checkAttribute(el2.childNodes, 'length', 1)

        checkAttribute(el1.childNodes[0], 'data', 'foobar')
        checkAttribute(el2.childNodes[0], 'data', 'spameggs')


# --- CharacterData

class CharacterDataReadTestCaseBase(NodeReadTestCaseBase):

    def checkImportNode(self):
        foreignDoc = self.implementation.createDocument(None, 'foo', None)

        clone = foreignDoc.importNode(self.chardata, 0)
        deepClone = foreignDoc.importNode(self.chardata, 1)

        self.failIf(isSameNode(self.chardata, clone),
                    "Clone is same as original.")
        self.failIf(isSameNode(self.chardata, deepClone),
                    "Clone is same as original.")

        checkAttributeSameNode(clone, 'ownerDocument', foreignDoc)
        checkAttributeSameNode(deepClone, 'ownerDocument', foreignDoc)
        checkAttribute(clone, 'parentNode', None)
        checkAttribute(deepClone, 'parentNode', None)
        checkAttribute(clone, 'nodeType', self.chardata.nodeType)
        checkAttribute(deepClone, 'nodeType', self.chardata.nodeType)
        checkAttribute(clone, 'data', self.chardata.data)
        checkAttribute(deepClone, 'data', self.chardata.data)
        checkLength(clone.childNodes, 0)
        checkLength(deepClone.childNodes, 0)


class CharacterDataWriteTestCaseBase(NodeWriteTestCaseBase):

    pass


# --- Comment

class CommentReadTestCase(CharacterDataReadTestCaseBase):

    def setUp(self):
        self.chardata = self.node = self.createDocument().createComment("com")


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
        self.expectedType = Node.TEXT_NODE


# --- Attr

class AttrReadTestCase(NodeReadTestCaseBase):

    def setUp(self):
        self.attr = self.node = self.createDocument().createAttributeNS(
            self.TEST_NAMESPACE, self.TEST_QUALIFIED_NAME)
        self.attrNoNS = self.nodeNoNS = self.document.createAttribute(
            self.TEST_LOCAL_NAME)

    def checkCloneNode(self):
        attr = self.attr
        clone = attr.cloneNode(0)

        self.failIf(isSameNode(attr, clone), "Clone is same Node as original.")
        checkAttribute(clone, 'localName', attr.localName)
        checkAttribute(clone, 'namespaceURI', attr.namespaceURI)
        checkAttribute(clone, 'prefix', attr.prefix)

        # make sure the cloned attr isn't sharing data with the original
        newPrefix = 'foo'
        newQname = '%s:%s' % (newPrefix, self.TEST_LOCAL_NAME)
        oldPrefix = self.attr.prefix
        oldQname = self.attr.name
        self.attr.prefix = newPrefix
        checkAttribute(clone, 'prefix', oldPrefix)
        checkAttribute(clone, 'name', oldQname)

    def checkImportNode(self):
        foreignDoc = self.implementation.createDocument(None, 'foo', None)

        clone = foreignDoc.importNode(self.attr, 0)
        deepClone = foreignDoc.importNode(self.attr, 1)

        self.failIf(isSameNode(self.attr, clone),
                    "Clone is same as original.")
        self.failIf(isSameNode(self.attr, deepClone),
                    "Clone is same as original.")

        checkAttributeSameNode(clone, 'ownerDocument', foreignDoc)
        checkAttributeSameNode(deepClone, 'ownerDocument', foreignDoc)
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
        self.attr = self.node = self.createDocument().createAttributeNS(
            self.TEST_NAMESPACE, self.TEST_QUALIFIED_NAME)
        self.attrNoNS = self.nodeNoNS = self.document.createAttribute(
            self.TEST_LOCAL_NAME)

    def checkAttrNodePrefixMultipleRefs(self):
        "changing the attribute prefix should change the name of other refs"
        # qualified name with different prefix
        newPrefix = 'foo'
        newQname = '%s:%s' % (newPrefix, self.TEST_LOCAL_NAME)

        self.attr.value = 'spam'
        self.document.documentElement.setAttributeNode(self.attr)
        attr2 = self.document.documentElement.getAttributeNodeNS(
            self.TEST_NAMESPACE, self.TEST_LOCAL_NAME)

        self.attr.prefix = newPrefix

        attr3 = self.document.documentElement.getAttributeNodeNS(
            self.TEST_NAMESPACE, self.TEST_LOCAL_NAME)
        # orig attr
        checkAttribute(self.attr, 'nodeName', newQname)
        # attr gotten before set
        checkAttribute(attr2, 'nodeName', newQname)
        # attr gotten after set
        checkAttribute(attr3, 'nodeName', newQname)

    def checkElementAttrPrefixMultipleRefs(self):
        "changing the attribute prefix should change the name of other refs"
        # qualified name with different prefix
        newPrefix = 'foo'
        newQname = '%s:%s' % (newPrefix, self.TEST_LOCAL_NAME)

        self.attr.value = 'spam'
        self.document.documentElement.setAttributeNode(self.attr)
        attr2 = self.document.documentElement.getAttributeNodeNS(
            self.TEST_NAMESPACE, self.TEST_LOCAL_NAME)

        # change the prefix and value of the attr.  Since we're giving the same
        # localname and namespaceURI, the existing attr should be changed.
        self.document.documentElement.setAttributeNS(self.TEST_NAMESPACE,
                                                     newQname, 'eggs')

        attr3 = self.document.documentElement.getAttributeNodeNS(
            self.TEST_NAMESPACE, self.TEST_LOCAL_NAME)

        # element attr
        value = self.document.documentElement.getAttributeNS(
            self.TEST_NAMESPACE, self.TEST_LOCAL_NAME)
        self.assertEqual(
            value, 'eggs',
            "changing prefix and value on attr didn't change original attr")
        # orig attr
        checkAttribute(self.attr, 'nodeName', newQname)
        # attr gotten before set
        checkAttribute(attr2, 'nodeName', newQname)
        # attr gotten after set
        checkAttribute(attr3, 'nodeName', newQname)


# --- Default attributes

class DefaultAttrTestCase(TestCaseBase):

    def setUp(self):
        self.document = self.parse("""
            <!DOCTYPE doc [
                <!ELEMENT doc EMPTY>
                <!ATTLIST doc foo CDATA "bar">
            ]>
            <doc xmlns="%s"/>
        """ % TEST_NAMESPACE)

    def checkCreateElementNS(self):
        el = self.document.createElementNS(TEST_NAMESPACE, 'doc')

        self.assert_(el.hasAttribute('foo'),
                     'Newly created Element should have default attribute.')
        self.assertEqual(
            el.getAttribute('foo'), 'bar',
            "Wrong value of default attribute found, expected 'bar', "
            "found " + repr(el.getAttribute('foo')))
        checkAttribute(el.getAttributeNode('foo'), 'specified', 0)

    def checkImportNode(self):
        attr = self.document.documentElement.getAttributeNode('foo')
        newDoc = self.implementation.createDocument(None, 'baz', None)

        importedAttr = newDoc.importNode(attr, 0)
        checkAttribute(importedAttr, 'specified', 1)

    def checkImportNodeFromDefault(self):
        newDoc = self.implementation.createDocument(None, 'baz', None)

        el = newDoc.importNode(self.document.documentElement, 0)

        self.failIf(el.hasAttribute('foo'),
                    "Default attribute retained when importing into document"
                    " that doesn't specify the default attribute.")

    def checkImportNodeToDefault(self):
        newDoc = self.implementation.createDocument(None, 'baz', None)
        newEl = newDoc.createElementNS(TEST_NAMESPACE, 'doc')

        el = self.document.importNode(newEl, 0)

        self.assert_(
            el.hasAttribute('foo'),
            'Imported Element Node should have default attribute.')
        self.assertEqual(
            el.getAttribute('foo'), 'bar',
            "Wrong value of default attribute found, expected 'bar', found "
            + repr(el.getAttribute('foo')))
        checkAttribute(el.getAttributeNode('foo'), 'specified', 0)


class DefaultAttrWithPrefixTestCase(TestCaseBase):

    def setUp(self):
        self.document = self.parse("""
            <!DOCTYPE prefix:doc [
                <!ELEMENT prefix:doc EMPTY>
                <!ATTLIST prefix:doc prefix:foo CDATA "bar">
            ]>
            <prefix:doc xmlns:prefix="%s"/>
        """ % TEST_NAMESPACE)

    def checkHasAttributeNS(self):
        el = self.document.documentElement

        self.assert_(el.hasAttributeNS(TEST_NAMESPACE, 'foo'),
                     'Default attribute not found.')

    def checkGetAttributeNS(self):
        el = self.document.documentElement

        self.assertEqual(
            el.getAttributeNS(TEST_NAMESPACE, 'foo'), 'bar',
            "Wrong value of default attribute found, expected 'bar', found "
            + repr(el.getAttributeNS(TEST_NAMESPACE, 'foo')))

    def checkCreateElementNS(self):
        el = self.document.createElementNS(TEST_NAMESPACE, 'doc')

        self.assert_(
            el.hasAttributeNS(TEST_NAMESPACE, 'foo'),
            'Newly created Element Node should have default attribute.')
        self.assertEqual(
            el.getAttributeNS(TEST_NAMESPACE, 'foo'), 'bar',
            "Wrong value of default attribute found, expected 'bar', found "
            + repr(el.getAttributeNS(TEST_NAMESPACE, 'foo')))
        checkAttribute(el.getAttributeNodeNS(TEST_NAMESPACE, 'foo'),
                       'specified', 0)

    def checkImportNodeToDefault(self):
        newDoc = self.implementation.createDocument(None, 'baz', None)
        newEl = newDoc.createElementNS(TEST_NAMESPACE, 'prefix:doc')

        el = self.document.importNode(newEl, 0)

        self.assert_(
            el.hasAttributeNS(TEST_NAMESPACE, 'foo'),
            'Imported Element Node should have default attribute.')
        self.assertEqual(
            el.getAttributeNS(TEST_NAMESPACE, 'foo'), 'bar',
            "Wrong value of default attribute found, expected 'bar', found "
            + repr(el.getAttributeNS(TEST_NAMESPACE, 'foo')))
        checkAttribute(el.getAttributeNodeNS(TEST_NAMESPACE, 'foo'),
                       'specified', 0)

    def checkChangePrefixUnspecified(self):
        attr = self.document.documentElement.getAttributeNodeNS(
            TEST_NAMESPACE, 'foo')
        attr.prefix = 'test'

        # Changing the prefix of a default attribute shouldn't make a new
        # unspecified (default) attribute node appear.
        # TODO: It turns out this may be a hole in the spec. See PXML(60)[]:
        # http://www.zope.org/Members/karl/ParsedXML/ParsedXMLTracker/60
        # Waiting for consensus from DOM WG. Changing the prefix *should* make
        # a new Attr node appear it seems. I am not convinced yet.
        self.assertEqual(
            attr.ownerElement.attributes.length, 1,
            "Changing the prefix of a default attribute caused a new default "
            "attribute node to be created.")

        # The specified flag shouldn't change; we didn't change the value
        checkAttribute(attr, 'specified', 0)

    def checkChangePrefixSpecified(self):
        self.document.documentElement.setAttributeNS(
            TEST_NAMESPACE, 'foo', 'newValue')
        attr = self.document.documentElement.getAttributeNodeNS(
            TEST_NAMESPACE, 'foo')
        attr.prefix = 'test'

        # Changing the prefix of a specified attribute shouldn't make a new
        # unspecified (default) attribute node appear.
        self.assertEqual(
            attr.ownerElement.attributes.length, 2,
            "Changing the prefix of a specified attribute caused a new "
            "default attribute node to be created.")

    def checkRemoveAttributeNS(self):
        el = self.document.documentElement
        # Replace default with specified attr
        el.setAttributeNS(TEST_NAMESPACE, 'foo', 'baz')

        el.removeAttributeNS(TEST_NAMESPACE, 'foo')
        self.assert_(
            el.hasAttributeNS(TEST_NAMESPACE, 'foo'),
            'Removing specified attribute should restore default attribute.')
        self.assertEqual(
            el.getAttributeNS(TEST_NAMESPACE, 'foo'), 'bar',
            "Wrong value of default attribute foud, expected 'bar', found "
            + repr(el.getAttributeNS(TEST_NAMESPACE, 'foo')))
        checkAttribute(el.getAttributeNodeNS(TEST_NAMESPACE, 'foo'),
                       'specified', 0)

    def checkRemoveAttributeNode(self):
        el = self.document.documentElement
        newAttr = self.document.createAttributeNS(TEST_NAMESPACE, 'foo')
        newAttr.value = 'baz'
        # Replace default with specified attr
        el.setAttributeNodeNS(newAttr)

        el.removeAttributeNode(newAttr)
        self.assert_(
            el.hasAttributeNS(TEST_NAMESPACE, 'foo'),
            'Removing specified attribute should restore default attribute.')
        self.assert_(
            el.getAttributeNS(TEST_NAMESPACE, 'foo'), 'bar',
            "Wrong value of default attribute found, expected 'bar', found "
            + repr(el.getAttributeNS(TEST_NAMESPACE, 'foo')))
        checkAttribute(el.getAttributeNodeNS(TEST_NAMESPACE, 'foo'),
                       'specified', 0)

    def checkRemoveNamedItemNS(self):
        el = self.document.documentElement
        # Replace default with specified attr
        el.setAttributeNS(TEST_NAMESPACE, 'foo', 'baz')

        el.attributes.removeNamedItemNS(TEST_NAMESPACE, 'foo')
        self.assert_(
            el.hasAttributeNS(TEST_NAMESPACE, 'foo'),
            'Removing specified attribute should restore default attribute.')
        self.assertEqual(
            el.getAttributeNS(TEST_NAMESPACE, 'foo'), 'bar',
            "Wrong value of default attribute found, expected 'bar', found "
            + repr(el.getAttributeNS(TEST_NAMESPACE, 'foo')))
        checkAttribute(el.getAttributeNodeNS(TEST_NAMESPACE, 'foo'),
                       'specified', 0)

    def checkSetAttributeNS(self):
        el = self.document.documentElement
        el.setAttributeNS(TEST_NAMESPACE, 'foo', 'baz')
        checkAttribute(el.getAttributeNodeNS(TEST_NAMESPACE, 'foo'),
            'specified', 1)

    def checkSetAttributeNodeNS(self):
        el = self.document.documentElement
        newAttr = self.document.createAttributeNS(TEST_NAMESPACE, 'foo')
        newAttr.value = 'baz'
        el.setAttributeNode(newAttr)
        checkAttribute(el.getAttributeNodeNS(TEST_NAMESPACE, 'foo'),
            'specified', 1)


# --- DocumentFragment

class DocumentFragmentReadTestCase(NodeReadTestCaseBase):

    def setUp(self):
        self.docfrag = self.createDocument().createDocumentFragment()
        self.node = self.docfrag

    def checkImportNode(self):
        foreignDoc = self.implementation.createDocument(None, 'foo', None)
        frag = self.docfrag

        frag.appendChild(self.document.createComment('foo'))
        frag.appendChild(self.document.createTextNode('bar'))

        clone = foreignDoc.importNode(frag, 0)
        deepClone = foreignDoc.importNode(frag, 1)

        self.failIf(isSameNode(frag, clone),
                    "Clone is same Node as original.")
        self.failIf(isSameNode(frag, deepClone),
                    "Clone is same Node as original.")

        checkAttributeSameNode(clone, 'ownerDocument', foreignDoc)
        checkAttributeSameNode(deepClone, 'ownerDocument', foreignDoc)
        checkAttribute(clone, 'parentNode', None)
        checkAttribute(deepClone, 'parentNode', None)
        checkLength(clone.childNodes, 0)
        checkLength(deepClone.childNodes, frag.childNodes.length)

        for i in range(deepClone.childNodes.length):
            checkAttribute(deepClone.childNodes.item(i), 'nodeType',
                frag.childNodes.item(i).nodeType)
            checkAttribute(deepClone.childNodes.item(i), 'data',
                frag.childNodes.item(i).data)
            checkAttributeSameNode(deepClone.childNodes.item(i),
                'ownerDocument', foreignDoc)


class DocumentFragmentWriteTestCase(NodeWriteTestCaseBase):

    def setUp(self):
        self.docfrag = self.createDocument().createDocumentFragment()
        self.node = self.docfrag


# --- NamedNodeMap

class NamedNodeMapWriteTestCase(TestCaseBase):

    TEST_NAMESPACE = NodeReadTestCaseBase.TEST_NAMESPACE
    TEST_PREFIX = NodeReadTestCaseBase.TEST_PREFIX
    TEST_LOCAL_NAME = NodeReadTestCaseBase.TEST_LOCAL_NAME
    TEST_QUALIFIED_NAME = NodeReadTestCaseBase.TEST_QUALIFIED_NAME

    def setUp(self):
        self.map = self.createDocument().createElement("foo")._get_attributes()
        self.attribute = self.document.createAttributeNS(self.TEST_NAMESPACE,
            self.TEST_QUALIFIED_NAME)
        self.attribute.value = "attrValue"
        self.map.setNamedItemNS(self.attribute)

    def checkGetNamedItemNS(self):
        node = self.map.getNamedItemNS(self.TEST_NAMESPACE,
            self.TEST_LOCAL_NAME)

        self.assert_(node is not None,
                     "getNamedItemNS didn't retrieve attribute.")
        self.assert_(isSameNode(node, self.attribute),
                     "getNamedItemNS retrieved incorrect attribute.")

    def checkGetNamedItemNSWrongNamespace(self):
        node = self.map.getNamedItemNS('uri:foo', self.TEST_LOCAL_NAME)
        self.assert_(node is None, "getNamedItemNS returned an attribute.")

    def checkGetNamedItemNSWrongLocalname(self):
        node = self.map.getNamedItemNS(self.TEST_NAMESPACE, 'bar')
        self.assert_(node is None, "getNamedItemNS returned an attribute.")

    def checkRemoveNamedItemNS(self):
        node = self.map.removeNamedItemNS(self.TEST_NAMESPACE,
            self.TEST_LOCAL_NAME)

        self.assert_(node is not None,
                     "removeNamedItemNS didn't return an attribute.")
        self.assert_(isSameNode(node, self.attribute),
                     "removeNamedItemNS returned incorrect attribute.")
        n = self.map.getNamedItemNS(self.TEST_NAMESPACE, self.TEST_LOCAL_NAME)
        self.assert_(n is None, "Attribute was not removed.")
        checkLength(self.map, 0)

    def checkRemoveNamedItemNSNotFound(self):
        # Exceptions
        self.assertRaises(xml.dom.NotFoundErr,
                          self.map.removeNamedItemNS, 'uri:foo', 'bar:baz')

    def checkSetNamedItemNS(self):
        newAttr = self.document.createAttributeNS(self.TEST_NAMESPACE,
            'qname:someAttr')
        newAttr.value = 'spam'

        retVal = self.map.setNamedItemNS(newAttr)
        self.assert_(retVal is None,
                     "setNamedItemNS returned " + repr(retVal))
        checkLength(self.map, 2)
        n = self.map.getNamedItemNS(self.TEST_NAMESPACE, 'someAttr')
        self.assert_(
            isSameNode(n, newAttr),
            "setNamedItemNS store seems to have failed, can't retrieve.")

    def checkSetNamedItemNSReplaceExisting(self):
        newAttr = self.document.createAttributeNS(self.TEST_NAMESPACE,
            'qname:someAttr')
        self.map.setNamedItemNS(newAttr)
        anotherAttr = self.document.createAttributeNS(self.TEST_NAMESPACE,
            'anotherQN:someAttr')
        anotherAttr.value = 'eggs'

        retVal = self.map.setNamedItemNS(newAttr)
        self.failIf(retVal is None, "setNamedItemNS returned None")
        self.assert_(isSameNode(retVal, newAttr),
                     "setNamedItemNS didn't return replaced Node.")
        checkLength(self.map, 2)

    def checkSetNamedItemNSWrongDocument(self):
        newDoc = self.implementation.createDocument(None, 'foo', None)
        foreignAttr = newDoc.createAttributeNS(
            self.TEST_NAMESPACE, self.TEST_QUALIFIED_NAME)
        self.assertRaises(xml.dom.WrongDocumentErr,
                          self.map.setNamedItem, foreignAttr)

    def checkSetNamedItemNSAlreadyInUse(self):
        el = self.document.createElement('someElement')
        attr = self.document.createAttributeNS(
            self.TEST_NAMESPACE, self.TEST_QUALIFIED_NAME)
        el.setAttributeNode(attr)
        self.assertRaises(xml.dom.InuseAttributeErr,
                          self.map.setNamedItem, attr)

    def checkSetNamedItemNSHierarchyRequestErr(self):
        # See DOM erratum core-4.
        element = self.document.createElementNS(TEST_NAMESPACE, 'foo:bar')
        self.assertRaises(xml.dom.HierarchyRequestErr,
                          self.map.setNamedItemNS, element)


cases = buildCases(__name__, 'Core', '2.0')
