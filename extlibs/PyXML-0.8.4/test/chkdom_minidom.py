import unittest

import xml.dom.expatbuilder
import xml.dom.minidom

from domapi import DOMImplementationTestSuite


def DOMParseString(self, text):
    return xml.dom.expatbuilder.parseString(text)

def test_suite():
    """Return a test suite for the Zope testing framework."""
    return DOMImplementationTestSuite(xml.dom.minidom.getDOMImplementation(),
                                      DOMParseString)

if __name__ == "__main__":
    unittest.main(defaultTest="test_suite")
