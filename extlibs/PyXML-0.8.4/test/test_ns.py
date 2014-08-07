"""Tests for the xml.ns module."""

import unittest

import xml.ns


URI = "http://xml.python.org/test/namespace"


class SimpleTests(unittest.TestCase):
    def setUp(self):
        self.ns = self.createNamespace(URI, ["abc", "defg"])

    def test_predefined_names(self):
        self.assertEqual(self.ns.abc, (URI, "abc"))
        self.assertEqual(self.ns.defg, (URI, "defg"))


class OpenNamespaceTests(SimpleTests):
    createNamespace = xml.ns.OpenNamespace

    def test_undefined_names(self):
        x = self.ns.splat
        self.assertEqual(x, (URI, "splat"))
        self.assertEqual(x, self.ns.splat)


class ClosedNamespaceTests(SimpleTests):
    createNamespace = xml.ns.ClosedNamespace

    def test_undefined_names(self):
        self.assertRaises(AttributeError, lambda ns=self.ns: ns.notthere)


def test_suite():
    suite = unittest.makeSuite(OpenNamespaceTests)
    suite.addTest(unittest.makeSuite(ClosedNamespaceTests))
    return suite

def test_main():
    import test_support
    test_support.run_suite(test_suite())

if __name__ == "__main__":
    import test_support
    test_support.verbose = 1
    test_main()

