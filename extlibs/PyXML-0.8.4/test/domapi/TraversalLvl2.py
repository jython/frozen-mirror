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

import xml.dom
from xml.dom import Node

# --- NodeFilter interface. Should this be in xml.dom.__init__?

class NodeFilter:
    # Constants returned by acceptNode
    FILTER_ACCEPT                  = 1
    FILTER_REJECT                  = 2
    FILTER_SKIP                    = 3

    # Constants for whatToShow
    SHOW_ALL                       = 0xFFFFFFFF
    SHOW_ELEMENT                   = 0x00000001
    SHOW_ATTRIBUTE                 = 0x00000002
    SHOW_TEXT                      = 0x00000004
    SHOW_CDATA_SECTION             = 0x00000008
    SHOW_ENTITY_REFERENCE          = 0x00000010
    SHOW_ENTITY                    = 0x00000020
    SHOW_PROCESSING_INSTRUCTION    = 0x00000040
    SHOW_COMMENT                   = 0x00000080
    SHOW_DOCUMENT                  = 0x00000100
    SHOW_DOCUMENT_TYPE             = 0x00000200
    SHOW_DOCUMENT_FRAGMENT         = 0x00000400
    SHOW_NOTATION                  = 0x00000800

    def acceptNode(self, node):
        # By default, accept
        return self.FILTER_ACCEPT


# --- DocumentTraversal

class DocumentTraversalReadTestCase(TestCaseBase):

    def setUp(self):
        self.createDocumentNS()

    def checkCreateNodeIterator(self):
        root = self.document
        whatToShow = NodeFilter.SHOW_ALL
        filter = NodeFilter()

        iterator = self.document.createNodeIterator(
            root, whatToShow, filter, 1)

        checkAttributeSameNode(iterator, 'root', root)
        checkAttribute(iterator, 'whatToShow', whatToShow)
        self.assert_(
            iterator.filter is filter,
            "Created iterator has got a different filter object. Expected %s,"
            " found %s." % (repr(filter), repr(iterator.filter)))
        checkAttribute(iterator, 'expandEntityReferences', 1)

    def checkCreateNodeIteratorNoRoot(self):
        self.assertRaises(xml.dom.NotSupportedErr,
                          self.document.createNodeIterator,
                          None, NodeFilter.SHOW_ALL, None, 0)

    def checkCreateTreeWalker(self):
        root = self.document
        whatToShow = NodeFilter.SHOW_ALL
        filter = NodeFilter()

        walker = self.document.createTreeWalker(root, whatToShow, filter, 1)

        checkAttributeSameNode(walker, 'root', root)
        checkAttribute(walker, 'whatToShow', whatToShow)
        self.assert_(
            walker.filter is filter,
            "Created walker has got a different filter object. Expected %s,"
            " found %s." % (repr(filter), repr(walker.filter)))
        checkAttribute(walker, 'expandEntityReferences', 1)

    def checkCreateTreeWalkerNoRoot(self):
        self.assertRaises(xml.dom.NotSupportedErr,
                          self.document.createTreeWalker,
                          None, NodeFilter.SHOW_ALL, None, 0)

# --- NodeIterator

class NodeIteratorTestCase(TestCaseBase):

    def setUp(self):
        # Create a tree of elements. Alphabetic order denotes document order.
        docType = self.implementation.createDocumentType('A', None, None)
        self.document = doc = self.implementation.createDocument(
            None, 'A', docType)

        self.A = a = doc.documentElement
        self.B = a.appendChild(doc.createTextNode('B'))
        self.C = c = a.appendChild(doc.createElement('C'))
        self.D = c.appendChild(doc.createCDATASection('D'))
        self.E = c.appendChild(doc.createProcessingInstruction('E', 'A PI'))
        self.F = a.appendChild(doc.createComment('F'))
        self.G = a.appendChild(doc.createTextNode('G'))

        self.all = (doc, docType, a, self.B, c, self.D, self.E, self.F, self.G)

    def iterate(self, iterator, expectedNodes):
        all = expectedNodes[:]
        while 1:
            nextNode = iterator.nextNode()

            if nextNode is None:
                self.failIf(all,
                            "nextNode returned None before end, still expected"
                            " to see %s." % `all`)

            self.assert_(all,
                         "nextNode returned %s; expected None." % `nextNode`)

            expect = all.pop(0)
            self.assert_(
                isSameNode(expect, nextNode),
                "nextNode returned %s, expected %s." % (`nextNode`, `expect`))

        all = expectedNodes[:]
        while 1:
            previousNode = iterator.previousNode()

            if previousNode is None:
                self.failIf(all,
                            "previousNode returned None before end, still"
                            " expected to see %s." % `all`)

            self.assert_(all,
                         "previousNode returned %s; expected None." %
                         `previousNode`)

            expect = all.pop()
            self.assert_(isSameNode(expect, previousNode),
                         "previousNode returned %s, expected %s."
                         % (repr(previousNode), repr(expect)))

    def checkIteratorNoFilter(self):
        iterator = self.document.createNodeIterator(
            self.document, NodeFilter.SHOW_ALL, None, 0)

        self.iterate(iterator, list(self.all))

    def checkIteratorOnlyTextNodes(self):
        iterator = self.document.createNodeIterator(self.document,
            NodeFilter.SHOW_TEXT, None, 0)

        self.iterate(iterator, [self.B, self.G])

    def checkIteratorAllButTextNodes(self):
        iterator = self.document.createNodeIterator(self.document,
            NodeFilter.SHOW_ALL ^ NodeFilter.SHOW_TEXT, None, 0)

        self.iterate(iterator, list(self.all[:3] + self.all[4:8]))

    def checkIteratorFilterSkipC(self):
        class SkipCFilter(NodeFilter):
            def acceptNode(self, node):
                if node.nodeName == 'C':
                    return self.FILTER_SKIP
                else:
                    return self.FILTER_ACCEPT

        iterator = self.document.createNodeIterator(self.document,
            NodeFilter.SHOW_ALL, SkipCFilter(), 0)

        self.iterate(iterator, list(self.all[:4] + self.all[5:]))

    def checkIteratorFilterRejectC(self):
        class RejectCFilter(NodeFilter):
            def acceptNode(self, node):
                if node.nodeName == 'C':
                    return self.FILTER_REJECT
                else:
                    return self.FILTER_ACCEPT

        iterator = self.document.createNodeIterator(self.document,
            NodeFilter.SHOW_ALL, RejectCFilter(), 0)

        self.iterate(iterator, list(self.all[:4] + self.all[5:]))

    def checkIteratorOnlyTextNodesFilterSkipG(self):
        class SkipGFilter(NodeFilter):
            def acceptNode(self, node):
                if node.nodeValue == 'G':
                    return self.FILTER_SKIP
                else:
                    return self.FILTER_ACCEPT

        iterator = self.document.createNodeIterator(self.document,
            NodeFilter.SHOW_TEXT, SkipGFilter(), 0)

        self.iterate(iterator, [self.B])

    def checkIteratorPreviousNode(self):
        iterator = self.document.createNodeIterator(self.document,
            NodeFilter.SHOW_ALL, None, 0)

        self.assert_(iterator.previousNode() is None,
                     "previousNode on a fresh iterator did not return None.")

    def checkIteratorNextNodeInvalidState(self):
        iterator = self.document.createNodeIterator(self.document,
            NodeFilter.SHOW_ALL, None, 0)
        iterator.detach()

        self.assertRaises(xml.dom.InvalidStateErr, iterator.nextNode)

    def checkIteratorPreviousNodeInvalidState(self):
        iterator = self.document.createNodeIterator(self.document,
            NodeFilter.SHOW_ALL, None, 0)
        iterator.detach()

        self.assertRaises(xml.dom.InvalidStateErr, iterator.previousNode)

    def checkIteratorFilterException(self):
        class ExceptionFilter(NodeFilter):
            def acceptNode(self, node):
                raise KeyError, (
                    "Test exception to see if it will propagate.")

        iterator = self.document.createNodeIterator(self.document,
            NodeFilter.SHOW_ALL, ExceptionFilter(), 0)

        self.assertRaises(KeyError, iterator.nextNode)


# -- TreeWalker

class TreeWalkerTestCase(TestCaseBase):

    def setUp(self):
        # Create a tree of elements. Alphabetic order denotes document order.
        docType = self.implementation.createDocumentType('A', None, None)
        self.document = doc = self.implementation.createDocument(None, 'A',
            docType)

        self.A = a = doc.documentElement
        self.B = a.appendChild(doc.createTextNode('B'))
        self.C = c = a.appendChild(doc.createElement('C'))
        self.D = c.appendChild(doc.createCDATASection('D'))
        self.E = c.appendChild(doc.createProcessingInstruction('E', 'A PI'))
        self.F = a.appendChild(doc.createComment('F'))
        self.G = a.appendChild(doc.createTextNode('G'))

        self.all = (doc, docType, a, self.B, c, self.D, self.E, self.F, self.G)

    def iterate(self, walker, advanceMethod, retreatMethod,
                expectedNodesNext, expectedNodesPrevious = None):
        "Exercise methods given in advanceMethod, retreatMethod"
        if not expectedNodesPrevious:
            expectedNodesPrevious = expectedNodesNext
        all = expectedNodesNext[:]
        current = walker.currentNode
        while 1:
            if current is None:
                self.failIf(all,
                            "%s returned None before end, still expected to "
                            "see %s. TreeWalker.currentNode is %s." % (
                                advanceMethod, `all`, `walker.currentNode`))

            self.assert_(all,
                         "%s returned %s when we should've gotten None. "
                         "TreeWalker.currentNode is %s." % (
                             advanceMethod, `current`, `walker.currentNode`))

            expect = all.pop(0)
            self.assert_(
                isSameNode(expect, current),
                "%s returned %s, expected %s. TreeWalker.currentNode is %s."
                % (advanceMethod, `current`, `expect`, `walker.currentNode`))

            current = getattr(walker, advanceMethod)()

        all = expectedNodesPrevious[:]
        current = walker.currentNode
        while 1:
            if current is None:
                self.failIf(all,
                            "%s returned None before end, still expected to "
                            "see %s. TreeWalker.currentNode is %s." % (
                                retreatMethod, `all`, `walker.currentNode`))

            self.assert_(all,
                         "%s returned %s when we should've gotten None. "
                         "TreeWalker.currentNode is %s." % (
                             retreatMethod, `current`, `walker.currentNode`))

            expect = all.pop()
            self.assert_(
                isSameNode(expect, current),
                "%s returned %s, expected %s. TreeWalker.currentNode is %s."
                % (retreatMethod, `current`, `expect`, `walker.currentNode`))

            current = getattr(walker, retreatMethod)()

    def checkWalkerNoFilterIterate(self):
        walker = self.document.createTreeWalker(self.document,
            NodeFilter.SHOW_ALL, None, 0)

        self.iterate(walker, "nextNode", "previousNode", list(self.all))

    def checkWalkerOnlyTextNodesIterate(self):
        walker = self.document.createTreeWalker(self.document,
            NodeFilter.SHOW_TEXT, None, 0)

        self.iterate(walker, "nextNode", "previousNode",
                     [self.document, self.B, self.G], [self.B, self.G])

    def checkWalkerAllButTextNodesIterate(self):
        walker = self.document.createTreeWalker(self.document,
            NodeFilter.SHOW_ALL ^ NodeFilter.SHOW_TEXT, None, 0)

        self.iterate(walker, "nextNode", "previousNode",
                     list(self.all[:3] + self.all[4:8]))

    def checkWalkerFilterSkipCIterate(self):
        class SkipCFilter(NodeFilter):
            def acceptNode(self, node):
                if node.nodeName == 'C':
                    return self.FILTER_SKIP
                else:
                    return self.FILTER_ACCEPT

        walker = self.document.createTreeWalker(self.document,
            NodeFilter.SHOW_ALL, SkipCFilter(), 0)

        self.iterate(walker, "nextNode", "previousNode",
                     list(self.all[:4] + self.all[5:]))


    def checkWalkerFilterRejectCIterate(self):
        class RejectCFilter(NodeFilter):
            def acceptNode(self, node):
                if node.nodeName == 'C':
                    return self.FILTER_REJECT
                else:
                    return self.FILTER_ACCEPT

        walker = self.document.createTreeWalker(self.document,
            NodeFilter.SHOW_ALL, RejectCFilter(), 0)

        self.iterate(walker, "nextNode", "previousNode",
                     list(self.all[:4] + self.all[7:]))

    def checkWalkerOnlyTextNodesFilterSkipG(self):
        class SkipGFilter(NodeFilter):
            def acceptNode(self, node):
                if node.nodeValue == 'G':
                    return self.FILTER_SKIP
                else:
                    return self.FILTER_ACCEPT

        walker = self.document.createTreeWalker(self.document,
            NodeFilter.SHOW_TEXT, SkipGFilter(), 0)

        self.iterate(walker, "nextNode", "previousNode",
                     [self.document, self.B], [self.B,])

    def checkWalkerNoFilterParentNodeFirstChild(self):
        walker = self.document.createTreeWalker(self.document,
            NodeFilter.SHOW_ALL, None, 0)

        self.assert_(walker.parentNode() is None,
                     "parentNode on a fresh walker did not return None.")

        walker.firstChild() # doctype
        walker.nextSibling() # A
        walker.firstChild() # B
        walker.nextSibling() # C
        walker.firstChild() # D
        self.iterate(walker, "parentNode", "firstChild",
                     [self.D, self.C, self.A, self.document],
                     [self.document.doctype, self.document],)

    def checkWalkerOnlyTextNodesParentNodeFirstChild(self):
        walker = self.document.createTreeWalker(self.document,
            NodeFilter.SHOW_TEXT, None, 0)

        self.iterate(walker, "firstChild", "parentNode",
                     [self.document])

    def checkWalkerAllButTextNodesParentNodeFirstChild(self):
        walker = self.document.createTreeWalker(self.document,
            NodeFilter.SHOW_ALL ^ NodeFilter.SHOW_TEXT, None, 0)

        walker.firstChild() # doctype
        walker.nextSibling() # A
        self.iterate(walker, "firstChild", "parentNode",
                     [self.A, self.C, self.D],
                     [self.document, self.A, self.C, self.D],)

    # "first visible child" might be seen to imply "first child that
    # is visible", rather than "first visible descendent", but the
    # examples skip to descendents.
    def checkWalkerFilterSkipCFirstChild(self):
        class SkipCFilter(NodeFilter):
            def acceptNode(self, node):
                if node.nodeName == 'C':
                    return self.FILTER_SKIP
                else:
                    return self.FILTER_ACCEPT

        self.A.removeChild(self.B)

        walker = self.document.createTreeWalker(self.document,
            NodeFilter.SHOW_ALL, SkipCFilter(), 0)

        walker.firstChild() # doctype
        walker.nextSibling() # A
        self.iterate(walker, "firstChild", "parentNode",
                     [self.A, self.D],
                     [self.document, self.A, self.D])

    # also checks parentNode robustness under currentNode move
    def checkWalkerFilterSkipCParentNode(self):
        class SkipCFilter(NodeFilter):
            def acceptNode(self, node):
                if node.nodeName == 'C':
                    return self.FILTER_SKIP
                else:
                    return self.FILTER_ACCEPT

        walker = self.document.createTreeWalker(self.document,
            NodeFilter.SHOW_ALL, SkipCFilter(), 0)

        walker.firstChild() # doctype
        walker.nextSibling() # A
        walker.firstChild() # B
        self.C.appendChild(self.B)

        self.iterate(walker, "parentNode", "firstChild",
                     [self.B, self.A, self.document],
                     [self.document.doctype, self.document])

    def checkWalkerFilterRejectCFirstChild(self):
        class RejectCFilter(NodeFilter):
            def acceptNode(self, node):
                if node.nodeName == 'C':
                    return self.FILTER_REJECT
                else:
                    return self.FILTER_ACCEPT

        self.A.removeChild(self.B)

        walker = self.document.createTreeWalker(self.document,
            NodeFilter.SHOW_ALL, RejectCFilter(), 0)

        walker.firstChild() # doctype
        walker.nextSibling() # A
        self.iterate(walker, "firstChild", "parentNode",
                     [self.A, self.F],
                     [self.document, self.A, self.F])

    # also tests parentNode robustness under currentNode move
    def checkWalkerFilterRejectCParentNode(self):
        class RejectCFilter(NodeFilter):
            def acceptNode(self, node):
                if node.nodeName == 'C':
                    return self.FILTER_REJECT
                else:
                    return self.FILTER_ACCEPT

        walker = self.document.createTreeWalker(self.document,
            NodeFilter.SHOW_ALL, RejectCFilter(), 0)

        walker.firstChild() # doctype
        walker.nextSibling() # A
        walker.firstChild() # B
        self.C.appendChild(self.B)

        self.iterate(walker, "parentNode", "firstChild",
                     [self.B, self.A, self.document],
                     [self.document.doctype, self.document])

    def checkWalkerOnlyTextNodesParentNodeFirstChildFilterSkipB(self):
        class SkipBFilter(NodeFilter):
            def acceptNode(self, node):
                if node.nodeValue == 'B':
                    return self.FILTER_SKIP
                else:
                    return self.FILTER_ACCEPT

        walker = self.document.createTreeWalker(self.document,
            NodeFilter.SHOW_TEXT, SkipBFilter(), 0)

        self.iterate(walker, "firstChild", "parentNode",
                     [self.document, self.G])

    def checkWalkerNoFilterNextSiblingPreviousSibling(self):
        walker = self.document.createTreeWalker(self.document,
            NodeFilter.SHOW_ALL, None, 0)

        self.assert_(walker.previousSibling() is None,
                     "previousSibling on a fresh walker did not return None.")

        # move to B to make more interesting
        walker.firstChild() # doctype
        walker.nextSibling() # A
        walker.firstChild() # B
        self.iterate(walker, "nextSibling", "previousSibling",
                     [self.B, self.C, self.F, self.G])

    def checkWalkerNoFilterLastChild(self):
        walker = self.document.createTreeWalker(self.document,
            NodeFilter.SHOW_ALL, None, 0)

        # move to A to make more interesting
        walker.firstChild() # doctype
        walker.nextSibling() # A
        retNode = walker.lastChild()
        self.assert_(isSameNode(retNode, walker.currentNode))
        self.assert_(isSameNode(self.G, walker.currentNode))

    def checkWalkerPreviousNode(self):
        walker = self.document.createTreeWalker(self.document,
            NodeFilter.SHOW_ALL, None, 0)

        self.assert_(walker.previousNode() is None,
                     "previousNode on a fresh walker did not return None.")

    def checkCurrentNodeNoneNotSupported(self):
        walker = self.document.createTreeWalker(self.document,
            NodeFilter.SHOW_ALL, None, 0)

        try:
            walker.currentNode = None
        except xml.dom.NotSupportedErr:
            pass
        else:
            self.fail("Was allowed to set currentNode to None.")

cases = buildCases(__name__, 'Traversal', '2.0')
