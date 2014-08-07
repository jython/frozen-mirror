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

import xml.dom
from xml.dom import Node

import sys
import unittest

# Namespace URI for namespace tests
TEST_NAMESPACE = 'uri:namespacetests'

# Convenience map for assert messages
TYPE_NAME = {
        Node.ATTRIBUTE_NODE:                'Attribute',
        Node.CDATA_SECTION_NODE:            'CDATA Section',
        Node.COMMENT_NODE:                  'Comment',
        Node.DOCUMENT_FRAGMENT_NODE:        'Document Fragment',
        Node.DOCUMENT_NODE:                 'Document',
        Node.DOCUMENT_TYPE_NODE:            'DocumentType',
        Node.ELEMENT_NODE:                  'Element',
        Node.ENTITY_NODE:                   'Entity',
        Node.ENTITY_REFERENCE_NODE:         'Entity Reference',
        Node.NOTATION_NODE:                 'Notation',
        Node.PROCESSING_INSTRUCTION_NODE:   'Processing Instruction',
        Node.TEXT_NODE:                     'Text',
   }

def checkAttribute(node, attribute, value):
    """Check that an attribute holds the expected value, and that the
    corresponding accessor method, if provided, returns an equivalent
    value."""
    #
    v1 = getattr(node, attribute)
    if v1 != value:
        raise AssertionError(
            "attribute value does not match\n  expected: %s\n  found: %s"
            % (`value`, `v1`))
    if hasattr(node, "_get_" + attribute):
        v2 = getattr(node, "_get_" + attribute)()
        if v2 != value:
            raise AssertionError(
                "accessor result does not match\n  expected: %s\n  found: %s"
                % (`value`, `v2`))
        if v1 != v2:
            raise AssertionError(
                "attribute & accessor result don't compare equal\n"
                "  attribute: %s\n  accessor: %s"
                % (`v1`, `v2`))


def checkAttributeNot(node, attribute, value):
    """Check that an attribute doesn't hold a specific failing value,
    and that the corresponding accessor method, if provided, returns
    an equivalent value."""
    #
    v1 = getattr(node, attribute)
    if v1 == value:
        raise AssertionError(
           "attribute value should not match\n  found: %s" % `v1`)
    if hasattr(node, "_get_" + attribute):
        v2 = getattr(node, "_get_" + attribute)()
        if v2 == value:
            raise AssertionError(
                "accessor result should not match\n  found: %s" % `v2`)
        if v1 != v2:
            raise AssertionError(
                "attribute & accessor result don't compare equal\n"
                "  attribute: %s\n  accessor: %s"
                % (`v1`, `v2`))

def checkAttributeSameNode(node, attribute, value):
    v1 = getattr(node, attribute)
    if value is None:
        if v1 is not None:
            raise AssertionError(
                "attribute value does not match\n  expected: %s\n  found: %s"
                % (`value`, `v1`))
    else:
        if not isSameNode(value, v1):
            raise AssertionError(
                "attribute value does not match\n  expected: %s\n  found: %s"
                % (`value`, `v1`))
    if hasattr(node, "_get_" + attribute):
        v2 = getattr(node, "_get_" + attribute)()
        if value is None:
            if v2 is not None:
                raise AssertionError(
                    "accessor result does not match\n"
                    "  expected: %s\n  found: %s" % (`value`, `v2`))
        elif not isSameNode(value, v2):
            raise AssertionError(
                "accessor result does not match\n"
                "  expected: %s\n  found: %s" % (`value`, `v2`))


def checkReadOnly(node, attribute):
    try:
        setattr(node, attribute, "don't set this!")
    except xml.dom.NoModificationAllowedErr:
        pass
    else:
        raise AssertionError("write-access to the '%s' attribute not blocked"
                             % attribute)

    if hasattr(node, "_set_" + attribute):
        # setter implemented; make sure it won't allow update
        try:
            getattr(node, "_set_" + attribute)("don't set this!")
        except xml.dom.NoModificationAllowedErr:
            pass
        else:
            raise AssertionError("_set_%s() allowed attribute update"
                                 % attribute)


def checkLength(node, value):
    checkAttribute(node, "length", value)
    if len(node) != value:
        raise AssertionError("broken support for __len__()")
    checkReadOnly(node, "length")


def isSameNode(node1, node2):
    """Compare two nodes, returning true if they are the same.

    Use the DOM lvl 3 Node.isSameNode method if available, otherwise use a
    simple 'is' test.

    """

    if hasattr(node1, 'isSameNode'):
        return node1.isSameNode(node2)
    else:
        return node1 is node2


class TestCaseBase(unittest.TestCase):

    def createDocumentNS(self):
        self.document = self.implementation.createDocument(
            TEST_NAMESPACE, 'foo:bar', None)
        return self.document

    def createDocument(self):
        self.document = self.implementation.createDocument(None, 'root', None)
        return self.document

def buildCases(modName, feature, level):
    cases = []
    add = cases.append
    objects = sys.modules[modName].__dict__
    for obj in objects.keys():
        if obj[-8:] != 'TestCase': continue
        add((objects[obj], feature, level))

    return list(cases)
