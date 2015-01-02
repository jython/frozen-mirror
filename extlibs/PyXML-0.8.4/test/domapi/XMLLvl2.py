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
import CoreLvl2
TextReadTestCaseBase = CoreLvl2.TextReadTestCase
TextWriteTestCaseBase = CoreLvl2.TextWriteTestCase
NodeReadTestCaseBase = CoreLvl2.NodeReadTestCaseBase
NodeWriteTestCaseBase = CoreLvl2.NodeWriteTestCaseBase
del CoreLvl2

import xml.dom
from xml.dom import Node

# --- DocumentType

class DocumentTypeReadTestCase(NodeReadTestCaseBase):

    def setUp(self):
        self.doctype = self.node = self.implementation.createDocumentType(
            'foo:bar', 'uri:foo', 'uri:bar')

    def checkInternalSubset(self):
        # The DOM Level 2 recommendation is not clear on the value of the
        # internalSubset attribute when there isn't one; this test relies
        # on a clarification from Joe Kesselman:
        #
        # http://lists.w3.org/Archives/Public/www-dom/2001AprJun/0009.html
        #
        checkAttribute(self.doctype, 'internalSubset', None)
        checkReadOnly(self.doctype, 'internalSubset')

    def checkPublicId(self):
        checkAttribute(self.doctype, 'publicId', 'uri:foo')
        checkReadOnly(self.doctype, 'publicId')

    def checkSystemId(self):
        checkAttribute(self.doctype, 'systemId', 'uri:bar')
        checkReadOnly(self.doctype, 'systemId')

    def checkImportNode(self):
        foreignDoc = self.implementation.createDocument(None, 'foo', None)
        self.assertRaises(xml.dom.NotSupportedErr,
                          foreignDoc.importNode, self.doctype, 0)


class DocumentTypeWriteTestCase(NodeWriteTestCaseBase):

    def setUp(self):
        self.doctype = self.node = self.implementation.createDocumentType(
            'foo:bar', 'uri:foo', 'uri:bar')


# --- ProcessingInstruction

class ProcessingInstructionReadTestCase(NodeReadTestCaseBase):

    def setUp(self):
        self.pi = self.createDocument().createProcessingInstruction("pit",
                                                                    "pid")
        self.node = self.pi

    def checkImportNode(self):
        foreignDoc = self.implementation.createDocument(None, 'foo', None)

        clone = foreignDoc.importNode(self.pi, 0)
        deepClone = foreignDoc.importNode(self.pi, 1)

        self.failIf(isSameNode(self.pi, clone),
                    "Clone is same as original.")
        self.failIf(isSameNode(self.pi, deepClone),
                    "Clone is same as original.")

        checkAttributeSameNode(clone, 'ownerDocument', foreignDoc)
        checkAttributeSameNode(deepClone, 'ownerDocument', foreignDoc)
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


# --- CDATASection

class CDATASectionReadTestCase(TextReadTestCaseBase):

    def setUp(self):
        self.chardata = self.node = self.createDocument().createCDATASection(
            "com")


class CDATASectionWriteTestCase(TextWriteTestCaseBase):

    def setUp(self):
        self.chardata = self.node = self.createDocument().createCDATASection(
            "com")


# --- EntityReference

class EntityReferenceReadTestCase(NodeReadTestCaseBase):

    def setUp(self):
        self.entref = self.node = self.createDocument().createEntityReference(
            "eref")

    def checkImportNode(self):
        pass # TODO: Fill in meaningful test here.


class EntityReferenceWriteTestCase(NodeWriteTestCaseBase):

    def setUp(self):
        self.entref = self.node = self.createDocument().createEntityReference(
            "eref")


# --- Entity

class EntityReadTestCase(NodeReadTestCaseBase):

    def setUp(self):
        doc = self.document = self.parse("""
            <!DOCTYPE doc [
                <!ENTITY internalParsedE "Entity text">
            ]>
            <doc/>
        """)

        self.node = doc.doctype.entities.getNamedItem('internalParsedE')


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
                <!NOTATION aNotation PUBLIC "uri:public">
            ]>
            <doc/>
        """)

        self.node = doc.doctype.notations.getNamedItem('aNotation')


class NotationWriteTestCase(NodeWriteTestCaseBase):

    def setUp(self):
        doc = self.document = self.parse("""
            <!DOCTYPE doc [
                <!NOTATION aNotation PUBLIC "uri:public">
            ]>
            <doc/>
        """)

        self.node = doc.doctype.notations.getNamedItem('aNotation')


cases = buildCases(__name__, 'XML', '2.0')
