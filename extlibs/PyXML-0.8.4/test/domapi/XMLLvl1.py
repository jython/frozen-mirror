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
from CoreLvl1 import NodeReadTestCaseBase, NodeWriteTestCaseBase
from CoreLvl1 import TextReadTestCase, TextWriteTestCase
TextReadTestCaseBase = TextReadTestCase
TextWriteTestCaseBase = TextWriteTestCase
del TextReadTestCase
del TextWriteTestCase

import xml.dom
from xml.dom import Node

# --- DocumentType

class DocumentTypeReadTestCase(NodeReadTestCaseBase):

    def setUp(self):
        self.doctype = self.node = self.implementation.createDocumentType(
            'foo', None, None)
        self.expectedType = Node.DOCUMENT_TYPE_NODE

        doc = self.parse("""
            <!DOCTYPE doc [
                <!ENTITY internalParsedE "Entity text">

                <!NOTATION aNotation PUBLIC "uri:public">
                <!ENTITY publicUnparsedE PUBLIC "uri:public" "uri:system"
                    NDATA aNotation>
                <!ENTITY systemUnparsedE SYSTEM "uri:system" NDATA aNotation>
            ]>
            <doc/>""")

        self.doctypeInternalSubset = doc.doctype

    def checkName(self):
        checkAttribute(self.doctype, 'name', 'foo')
        checkReadOnly(self.doctype, 'name')

    def checkEmptyEntities(self):
        self.assertEqual(self.doctype.entities.length, 0)
        self.assertEqual(len(self.doctype.entities), 0)

    def checkEntitiesInternalSubset(self):
        checkLength(self.doctypeInternalSubset.entities, 3)

        entity = self.doctypeInternalSubset.entities.getNamedItem(
            'internalParsedE')

    def checkEntitiesRemoveReadOnly(self):
        self.assertRaises(
            xml.dom.NoModificationAllowedErr,
            self.doctypeInternalSubset.entities.removeNamedItem,
            'internalParsedE')

    def checkEntitiesSetReadOnly(self):
        entity = self.doctypeInternalSubset.entities.item(0)
        self.assertRaises(
            xml.dom.NoModificationAllowedErr,
            self.doctypeInternalSubset.entities.setNamedItem, entity)

    def checkEmptyNotations(self):
        self.assertEqual(self.doctype.notations.length, 0)
        self.assertEqual(len(self.doctype.notations), 0)

    def checkNotationsInternalSubset(self):
        checkLength(self.doctypeInternalSubset.notations, 1)

        notation = self.doctypeInternalSubset.notations.getNamedItem(
            'aNotation')

    def checkNotationsRemoveReadOnly(self):
        self.assertRaises(
            xml.dom.NoModificationAllowedErr,
            self.doctypeInternalSubset.notations.removeNamedItem, 'aNotation')

    def checkNotationsSetReadOnly(self):
        notation = self.doctypeInternalSubset.notations.item(0)
        self.assertRaises(
            xml.dom.NoModificationAllowedErr,
            self.doctypeInternalSubset.notations.setNamedItem, notation)

    def checkCloneNode(self):
        # TODO: Implementation dependent, what should we test?
        pass


class DocumentTypeWriteTestCase(NodeWriteTestCaseBase):

    def setUp(self):
        self.createDocument() # Needed for Node tests
        self.doctype = self.node = self.implementation.createDocumentType(
            'foo', None, None)


# --- ProcessingInstruction

class ProcessingInstructionReadTestCase(NodeReadTestCaseBase):

    def setUp(self):
        self.pi = self.createDocument().createProcessingInstruction("pit",
                                                                    "pid")
        self.node = self.pi
        self.expectedType = Node.PROCESSING_INSTRUCTION_NODE

    def checkGetTarget(self):
        checkAttribute(self.pi, "target", "pit")

    def checkGetData(self):
        checkAttribute(self.pi, "data", "pid")

    def checkCloneNode(self):
        clone = self.pi.cloneNode(0)
        deepClone = self.pi.cloneNode(1)

        self.failIf(isSameNode(self.pi, clone),
                    "Clone is same as original.")
        self.failIf(isSameNode(self.pi, deepClone),
                    "Clone is same as original.")

        checkAttribute(clone, 'parentNode', None)
        checkAttribute(deepClone, 'parentNode', None)
        checkAttribute(clone, 'nodeType', self.pi.nodeType)
        checkAttribute(deepClone, 'nodeType', self.pi.nodeType)
        checkAttribute(clone, 'data', self.pi.data)
        checkAttribute(deepClone, 'data', self.pi.data)
        checkAttribute(clone, 'target', self.pi.target)
        checkAttribute(deepClone, 'target', self.pi.target)
        checkLength(clone.childNodes, 0)
        checkLength(deepClone.childNodes, 0)


class ProcessingInstructionWriteTestCase(NodeWriteTestCaseBase):

    def setUp(self):
        self.pi = self.createDocument().createProcessingInstruction("pit",
                                                                    "pid")
        self.node = self.pi

    def checkSetData(self):
        self.pi._set_data("uggg")
        checkAttribute(self.pi, "data", "uggg")


# --- CDATASection

class CDATASectionReadTestCase(TextReadTestCaseBase):

    def setUp(self):
        self.chardata = self.node = self.createDocument().createCDATASection(
            "com")
        self.expectedType = Node.CDATA_SECTION_NODE


class CDATASectionWriteTestCase(TextWriteTestCaseBase):

    def setUp(self):
        self.chardata = self.node = self.createDocument().createCDATASection(
            "com")


# --- EntityReference

class EntityReferenceReadTestCase(NodeReadTestCaseBase):

    def setUp(self):
        self.entref = self.node = self.createDocument().createEntityReference(
            "eref")
        self.expectedType = Node.ENTITY_REFERENCE_NODE
        self.expectedNodeName = 'eref'

    def checkCloneNode(self):
        pass # TODO: Fill in meaningful test here.


class EntityReferenceWriteTestCase(NodeWriteTestCaseBase):

    def setUp(self):
        self.entref = self.node = self.createDocument().createEntityReference(
            "eref")

    # TODO: An ENTITY_REFERENCE_NODE Node will have childNodes when the
    # entity it refers to has childNodes. We need entities first before we write
    # tests for that.


# --- Entity

class EntityReadTestCase(NodeReadTestCaseBase):

    def setUp(self):
        doc = self.document = self.parse("""
            <!DOCTYPE doc [
                <!ENTITY internalParsedE "Entity text">

                <!NOTATION aNotation PUBLIC "uri:public">
                <!ENTITY publicUnparsedE PUBLIC "uri:public" "uri:system"
                    NDATA aNotation>
                <!ENTITY systemUnparsedE SYSTEM "uri:system" NDATA aNotation>
            ]>
            <doc/>
        """)

        self.node = self.internalParsed = doc.doctype.entities.getNamedItem(
            'internalParsedE')
        self.publicUnparsed = doc.doctype.entities.getNamedItem(
            'publicUnparsedE')
        self.systemUnparsed = doc.doctype.entities.getNamedItem(
            'systemUnparsedE')

        self.expectedNodeName = 'internalParsedE'
        self.expectedType = Node.ENTITY_NODE

    def checkPublicIdReadOnly(self):
        checkReadOnly(self.node, 'publicId')

    def checkPublicIdInternalParsed(self):
        checkAttribute(self.internalParsed, 'publicId', None)

    def checkPublicIdPublicUnparsed(self):
        checkAttribute(self.publicUnparsed, 'publicId', 'uri:public')

    def checkPublicIdSystemUnparsed(self):
        checkAttribute(self.systemUnparsed, 'publicId', None)

    def checkSystemIdReadOnly(self):
        checkReadOnly(self.node, 'systemId')

    def checkSystemIdInternalParsed(self):
        checkAttribute(self.internalParsed, 'systemId', None)

    def checkSystemIdPublicUnparsed(self):
        checkAttribute(self.publicUnparsed, 'systemId', 'uri:system')

    def checkSystemIdSystemUnparsed(self):
        checkAttribute(self.systemUnparsed, 'systemId', 'uri:system')

    def checkNotationNameReadOnly(self):
        checkReadOnly(self.node, 'notationName')

    def checkNotationNameInternalParsed(self):
        checkAttribute(self.internalParsed, 'notationName', None)

    def checkNotationNamePublicUnparsed(self):
        checkAttribute(self.publicUnparsed, 'notationName', 'aNotation')

    def checkNotationNameSystemUnparsed(self):
        checkAttribute(self.systemUnparsed, 'notationName', 'aNotation')

    def checkSubTreeInternalParsed(self):
        entity = self.internalParsed

        self.assert_(
            entity.hasChildNodes(),
            'Internal Parsed Entity has no subtree representing the value.')
        checkAttribute(entity.firstChild, 'nodeType', Node.TEXT_NODE)
        checkAttribute(entity.firstChild, 'data', 'Entity text')
        checkReadOnly(entity.firstChild, 'data')

    def checkSubTreePublicUnparsed(self):
        self.failIf(self.publicUnparsed.hasChildNodes(),
                    'An unparsed entity should not have a sub-tree.')

    def checkSubTreeSystemUnparsed(self):
        self.failIf(self.systemUnparsed.hasChildNodes(),
                    'An unparsed entity should not have a sub-tree.')

class EntityWriteTestCase(NodeWriteTestCaseBase):

    def setUp(self):
        doc = self.document = self.parse("""
            <!DOCTYPE doc [
                <!ENTITY internalParsedE "Entity text">
            ]>
            <doc/>
        """)

        self.node = doc.doctype.entities.getNamedItem('internalParsedE')


# --- Notation

class NotationReadTestCase(NodeReadTestCaseBase):

    def setUp(self):
        doc = self.document = self.parse("""
            <!DOCTYPE doc [
                <!NOTATION publicExternalN PUBLIC "uri:public" "uri:system">
                <!NOTATION systemExternalN SYSTEM "uri:system">
                <!NOTATION publicN PUBLIC "uri:public">
            ]>
            <doc/>
        """)

        self.node = self.publicExternal = doc.doctype.notations.getNamedItem(
            'publicExternalN')
        self.systemExternal = doc.doctype.notations.getNamedItem(
            'systemExternalN')
        self.public = doc.doctype.notations.getNamedItem('publicN')

        self.expectedNodeName = 'publicExternalN'
        self.expectedType = Node.NOTATION_NODE

    def checkPublicIdReadOnly(self):
        checkReadOnly(self.node, 'publicId')

    def checkPublicIdPublicExternal(self):
        checkAttribute(self.publicExternal, 'publicId', 'uri:public')

    def checkPublicIdSystemExternal(self):
        checkAttribute(self.systemExternal, 'publicId', None)

    def checkPublicIdPublic(self):
        checkAttribute(self.public, 'publicId', 'uri:public')

    def checkSystemIdReadOnly(self):
        checkReadOnly(self.node, 'systemId')

    def checkSystemIdPublicExternal(self):
        checkAttribute(self.publicExternal, 'systemId', 'uri:system')

    def checkSystemIdSystemExternal(self):
        checkAttribute(self.systemExternal, 'systemId', 'uri:system')

    def checkSystemIdPublic(self):
        checkAttribute(self.public, 'systemId', None)


class NotationWriteTestCase(NodeWriteTestCaseBase):

    def setUp(self):
        doc = self.document = self.parse("""
            <!DOCTYPE doc [
                <!NOTATION aNotation PUBLIC "uri:public">
            ]>
            <doc/>
        """)

        self.node = doc.doctype.notations.getNamedItem('aNotation')


cases = buildCases(__name__, 'XML', '1.0')
