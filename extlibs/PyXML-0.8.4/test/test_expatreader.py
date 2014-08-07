# Test specific to the Expat SAX handler

# Check presence of underlying parser
try:
    import xml.parsers.expat
except ImportError:
    import pyexpat

from xml.sax.expatreader import create_parser
from xml.sax import handler
from xml.sax import SAXNotSupportedException
import test_support
import unittest

testcases = []

class feature_namespace_prefixes(unittest.TestCase):
    def setUp(self):
        self.parser = create_parser()
        self.parser.setFeature(handler.feature_namespaces, 1)
        self.parser.setFeature(handler.feature_namespace_prefixes, 1)

    def test_prefix_given(self):
        class Handler(handler.ContentHandler):
            def startElementNS(self, name, qname, attrs):
                self.qname = qname

        h = Handler()

        self.parser.setContentHandler(h)
        self.parser.feed("<Q:E xmlns:Q='http://pyxml.sf.net/testuri'/>")
        self.parser.close()
        self.failIf(h.qname is None)

testcases.append(feature_namespace_prefixes)

def test_main():
    import test_support
    test_support.run_unittest(*testcases)

if __name__ == "__main__":
    import test_support
    test_support.verbose = 1
    test_main()
