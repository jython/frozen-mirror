"""Test DOM registration framework."""

import unittest

import test_support

from xml.dom import domreg


def parse_feature_string(s):
    # helper to make sure the results are always plain lists
    return list(domreg._parse_feature_string(s))


class DomregTestCase(unittest.TestCase):

    def setUp(self):
        domreg.registerDOMImplementation("its-a-fake",
                                         self.getDOMImplementation)

    def getDOMImplementation(self):
        self.fake = FakeDOM(self.my_features)
        return self.fake

    def test_simple(self):
        self.assertEqual(parse_feature_string("simple"),
                         [("simple", None)])
        self.assertEqual(parse_feature_string("simple 1.0"),
                         [("simple", "1.0")])
        self.assertEqual(parse_feature_string("simple complex"),
                         [("simple", None), ("complex", None)])
        self.assertEqual(parse_feature_string("simple 2 complex 3.1.4.2"),
                         [("simple", "2"), ("complex", "3.1.4.2")])

    def test_extra_version(self):
        self.assertRaises(ValueError,
                          domreg._parse_feature_string, "1.0")
        self.assertRaises(ValueError,
                          domreg._parse_feature_string, "1 simple")
        self.assertRaises(ValueError,
                          domreg._parse_feature_string, "simple 1 2")

    def test_find_myself(self):
        self.my_features = [("splat", "1"), ("splat", "2"), ("splat", None)]
        self.failUnless(domreg.getDOMImplementation(features="splat")
                        is self.fake)
        self.failUnless(domreg.getDOMImplementation(features="splat 1")
                        is self.fake)
        self.failUnless(domreg.getDOMImplementation(features="splat 2")
                        is self.fake)
        self.failUnless(domreg.getDOMImplementation(features="splat 1 splat 2")
                        is self.fake)
        self.failUnless(domreg.getDOMImplementation(features="splat 2 splat 1")
                        is self.fake)

    def _test_cant_find(self):
        # This test is disabled since we need to determine what the
        # right thing to do is.  ;-(  The DOM Level 3 draft says
        # getDOMImplementation() should return null when there isn't a
        # match, but the existing Python API raises ImportError.
        self.my_features = []
        self.failUnless(domreg.getDOMImplementation(features="splat")
                        is None)
        self.failUnless(domreg.getDOMImplementation(features="splat 1")
                        is None)


class FakeDOM:
    def __init__(self, features):
        self.__features = features

    def hasFeature(self, feature, version):
        return (feature, version) in self.__features


def test_suite():
    return unittest.makeSuite(DomregTestCase)

def test_main():
    test_support.run_suite(test_suite())

if __name__ == "__main__":
    test_support.verbose = 1
    test_main()
