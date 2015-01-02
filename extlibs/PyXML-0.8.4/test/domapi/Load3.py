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

"""Tests for the 'Load' part of the Load/Save component from DOM Level 3.

Note that the Load/Save component is a working draft and not a final
recommendation.
"""

import xml.dom

import Base

# select the right StringIO
try:
    unicode
except NameError:
    try:
        from cStringIO import StringIO
    except:
        from StringIO import StringIO
else:
    # cStringIO has no support for Unicode strings
    from StringIO import StringIO


class BuilderTestCaseBase(Base.TestCaseBase):
    def createBuilder(self):
        return self.implementation.createDOMBuilder(
            self.implementation.MODE_SYNCHRONOUS, None)


class BuilderFeatureConformanceTestCase(BuilderTestCaseBase):
    """Test that the DOMBuilder has the defaults and allows setting
    all features required by the W3C specification.

    The features are not exercised, but every value that is required
    to be supported is tested and set.
    """

    FEATURES = {
        # feature-name: (default, must-support-true, must-support-false)
        "namespaces": (1, 1, 0),
        "namespace-declarations": (1, 1, 0),
        "validation": (0, 0, 1),
        "external-general-entities": (1, 1, 0),
        "external-parameter-entities": (1, 1, 0),
        "validate-if-schema": (0, 0, 1),
        "create-entity-ref-nodes": (1, 1, 0),
        "entities": (1, 1, 0),
        "whitespace-in-element-content": (1, 1, 0),
        "cdata-sections": (1, 1, 0),
        "comments": (1, 1, 1),
        "charset-overrides-xml-encoding": (1, 1, 1),
        }

    def checkFeatureDefaults(self):
        for item in self.FEATURES.items():
            feature, (default, xxx, xxx) = item
            b = self.createBuilder()
            value = b.getFeature(feature) and 1 or 0
            self.assert_(value == default,
                         "default feature value not right")

    def checkRequiredFeatureSettings(self):
        for item in self.FEATURES.items():
            feature, (xxx, require_true, require_false) = item
            b = self.createBuilder()
            if require_true:
                self.assert_(b.canSetFeature(feature, 1),
                             "builder indicates feature cannot be enabled")
                b.setFeature(feature, 1)
                self.assert_(b.getFeature(feature),
                             "enabling feature failed")
            if require_false:
                self.assert_(b.canSetFeature(feature, 0),
                             "builder indicates feature cannot be disabled")
                b.setFeature(feature, 0)
                self.assert_(not b.getFeature(feature),
                             "disabling feature failed")

    def checkSupportsFeatures(self):
        b = self.createBuilder()
        for feature in self.FEATURES.keys():
            self.assert_(b.supportsFeature(feature),
                         "builder reports non-support for required feature")

    def checkEntityNodesFeatureSideEffect(self):
        b = self.createBuilder()
        b.setFeature("entities", 0)
        self.assert_(not b.getFeature("create-entity-ref-nodes"),
                     "setting entities to false should turn off"
                     " create-entity-ref-nodes")

    def checkUnknownFeature(self):
        b = self.createBuilder()
        self.assertRaises(xml.dom.NotFoundErr,
                          b.setFeature, "non-existant-feature", 0)
        self.assertRaises(xml.dom.NotFoundErr,
                          b.getFeature, "non-existant-feature")
        self.assert_(not b.supportsFeature("non-existant-feature"),
                     "expected non-existant-feature to raise"
                     " xml.dom.NotFoundErr")
        self.assert_(not b.canSetFeature("non-existant-feature", 0),
                     "builder allows setting of non-existant feature"
                     " to false")
        self.assert_(not b.canSetFeature("non-existant-feature", 1),
                     "builder allows setting of non-existant feature"
                     " to true")

    def checkWhiteSpaceInElementContentDiscarded(self):
        TEXT = """<!DOCTYPE doc [
          <!ELEMENT doc (foo+)>
        ]>
        <doc>
          <foo/>
        </doc>"""
        doc = self._parse(TEXT, {"whitespace-in-element-content": 0})
        for node in doc.documentElement.childNodes:
            if node.nodeType == xml.dom.Node.TEXT_NODE:
                self.fail("found whitespace-in-element-content node which"
                          " should bave been excluded")

    def checkCommentsOmitted(self):
        doc = self._parse("<doc><!-- comment --></doc>",
                          {"comments": 0})
        self.assert_(doc.documentElement.childNodes.length == 0,
                     "comment node was returned as part of the document")

    def checkCDATAAsText(self):
        doc = self._parse("<doc><![CDATA[<<!--stuff-->>]]></doc>",
                          {"cdata-sections": 0})
        self.assert_(doc.documentElement.childNodes[0].data
                     == "<<!--stuff-->>")
        self.assert_(doc.documentElement.childNodes.length == 1)

    def checkWithoutNamespaces(self):
        doc = self._parse("<doc xmlns='foo' xmlns:tal='bar' tal:attr='value'>"
                          "  <tal:element tal:attr2='another'/>"
                          "</doc>",
                          {"namespaces": 0})
        docelem = doc.documentElement
        self.assert_(docelem.namespaceURI is None)
        self.assert_(docelem.prefix is None)
        self.assert_(docelem.getAttributeNode("xmlns").namespaceURI is None)
        self.assert_(docelem.getAttributeNode("xmlns").prefix is None)
        self.assert_(docelem.getAttributeNode("tal:attr").namespaceURI is None)
        self.assert_(docelem.getAttributeNode("tal:attr").prefix is None)
        elem = docelem.firstChild
        self.assert_(elem.namespaceURI is None)
        self.assert_(elem.prefix is None)

    def checkWithoutNamespaceDeclarations(self):
        doc = self._parse("<doc xmlns='foo' xmlns:tal='bar' tal:attr='value'>"
                          "<tal:element tal:attr2='another'/>"
                          "</doc>",
                          {"namespace-declarations": 0})
        docelem = doc.documentElement
        self.failIf(docelem.hasAttribute("xmlns"))
        self.failIf(docelem.hasAttribute("xmlns:tal"))
        self.assert_(docelem.attributes.length == 1)

    # We can't just name this parse(), since the framework overwrites
    # that name on the actual instances.
    #
    def _parse(self, source, flags={}):
        b = self.createBuilder()
        for feature, value in flags.items():
            b.setFeature(feature, value)
        fp = StringIO(source)
        inpsrc = self.implementation.createDOMInputSource()
        inpsrc.byteStream = fp
        return b.parse(inpsrc)


cases = Base.buildCases(__name__, "LS-Load", "3.0")
