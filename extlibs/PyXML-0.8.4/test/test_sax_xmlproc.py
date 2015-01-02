from test.test_support import verbose, TestFailed, findfile
from xml.sax.sax2exts import XMLValParserFactory
from xml.sax import InputSource, SAXException, ContentHandler
from StringIO import StringIO
import sys

#make_parser, ContentHandler, \
#                    SAXException, SAXReaderNotAvailable, SAXParseException
#  try:
#      make_parser()
#  except SAXReaderNotAvailable:
#      # don't try to test this module if we cannot create a parser
#      raise ImportError("no XML parsers available")
#  from xml.sax.saxutils import XMLGenerator, escape, XMLFilterBase
#  from xml.sax.expatreader import create_parser
#  from xml.sax.xmlreader import InputSource, AttributesImpl, AttributesNSImpl
#  from cStringIO import StringIO

# ===== Utilities

tests = 0
fails = 0

def confirm(outcome, name):
    global tests, fails

    tests = tests + 1
    if outcome:
        print "Passed", name
    else:
        print "Failed", name
        fails = fails + 1

def gen_inputs():
    f = open("xmlval_illformed.dtd","w")
    f.write("""<!ELEMENT configuration EMPTY>\n""")

if __name__=='__main__' and len(sys.argv)>1 and sys.argv[1] == 'generate':
    gen_inputs()
    raise SystemExit

doc1 = """<?xml version="1.0"?>
<!DOCTYPE configuration SYSTEM "NONEXISTENT.dtd">
<configuration/>"""

def test_nonexistent():
    p = XMLValParserFactory.make_parser()
    i = InputSource("doc1.xml")
    i.setByteStream(StringIO(doc1))
    try:
        p.parse(i)
    except SAXException,e:
        print "PASS:",e
        return 1
    else:
        return 0

doc2 = """<?xml version="1.0"?>
<!DOCTYPE configuration SYSTEM "xmlval_illformed.dtd">
<"""

def test_illformed():
    p = XMLValParserFactory.make_parser()
    i = InputSource("doc2.xml")
    i.setByteStream(StringIO(doc2))
    try:
        p.parse(i)
    except SAXException,e:
        print "PASS:",e
        return 1
    else:
        return 0

doc3 = """<?xml version="1.0"?>
<!DOCTYPE configuration [
  <!ELEMENT configuration EMPTY>
]>
<configuration>
</configuration>
"""

class H(ContentHandler):
    def __init__(self):
        self.passed = 0

    def ignorableWhitespace(self, data):
        self.passed = 1

def test_ignorable():
    p = XMLValParserFactory.make_parser()
    i = InputSource("doc3.xml")
    i.setByteStream(StringIO(doc3))
    h = H()
    p.setContentHandler(h)
    p.parse(i)
    return h.passed

items = locals().items()
items.sort()
for (name, value) in items:
    if name[ : 5] == "test_":
        confirm(value(), name)

print "%d tests, %d failures" % (tests, fails)
if fails != 0:
    raise TestFailed, "%d of %d tests failed" % (fails, tests)
