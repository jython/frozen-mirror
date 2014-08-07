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

"""A suite of unit tests for the Python DOM API.

This suite will test a DOM API for compliance with the DOM API, level
2.  It assumes that the DOM tested supports at least both the Core and
XML features.  It requires PyUnit; see http://pyunit.sourceforge.net/.

Example for the python minidom (which is an incomplete implementation):

from xml.dom.minidom import DOMImplementation, parseString
from domapi import DOMImplementationTestSuite

def MiniDomParseString(self, xml):
    return parseString(xml)

def test_suite():
    '''Return a test suite for the Zope testing framework.'''
    return DOMImplementationTestSuite(DOMImplementation(), MiniDomParseString)

if __name__ == '__main__':
    import unittest
    unittest.TextTestRunner().run(test_suite())

"""

import unittest
import CoreLvl1, CoreLvl2, CoreLvl3, XMLLvl1, XMLLvl2, TraversalLvl2, Load3

cases = (
    CoreLvl1.cases +
    CoreLvl2.cases +
    CoreLvl3.cases +
    XMLLvl1.cases +
    XMLLvl2.cases +
 #   TraversalLvl2.cases +
    Load3.cases
)

def DOMImplementationTestSuite(implementation, parseMethod, verbose=0):
    """ Create a testsuite for DOM lvl 2 compliance, given a DOM
    Implementation.

    To test a DOM implementation, hand in a DOMImplementation object,
    and a method that will take a string holding an XML document and
    returns a Document Node created from the XML.

    Then run the returned unittest testsuite.

    Note that the signature of the parse method is (self, xmlString)
    and should parse the xml string with namespaces turned on. It will
    be used to create Nodes which normally cannot be created using the
    DOM API, like Notations and Entities.

    """

    # First test for minimal feature support
    # XXX Why???
    assert (implementation.hasFeature('Core', '2.0') and
            implementation.hasFeature('XML', '2.0')), (
        "This DOMImplementation doesn't feature the level 2 Core and XML API.")

    suite = unittest.TestSuite()
    # The minimal set of features that should return 1 on hasFeature.
    # ('Core', '1.0') was never defined for DOM level 1, it was implicit. Most
    # DOM level 2 implementations return true, but this is a courtesy.
    supportedFeatures = {
        ('Core', None): 1,
        ('Core', '2.0'): 1,
        ('XML', None): 1,
        ('XML', '1.0'): 1,
        ('XML', '2.0'): 1,
    }

    for case, feature, version in cases:
        if implementation.hasFeature(feature, version):
            case.implementation = implementation
            case.parse = parseMethod
            suite.addTest(unittest.makeSuite(case, 'check'))

            supportedFeatures[(feature, version)] = 1
            supportedFeatures[(feature, None)] = 1
        else:
            if verbose:
                print ("Test %s skipped: DOM feature not supported.\n" %
                   case.__name__)

    # Record supported features.
    CoreLvl1.DOMImplementationReadTestCase.supportedFeatures = (
        supportedFeatures.keys())
    CoreLvl2.NodeReadTestCaseBase.supportedFeatures = (
        supportedFeatures.keys())

    return suite
