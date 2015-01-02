# regression test for SAX drivers
# $Id: test_saxdrivers.py,v 1.6 2002/07/01 18:42:04 fdrake Exp $

from xml.sax.saxutils import XMLGenerator, ContentGenerator
from xml.sax import handler, SAXReaderNotAvailable
import xml.sax.saxexts
import xml.sax.sax2exts
from cStringIO import StringIO
from test.test_support import verbose, TestFailed, findfile

try:
    import warnings
except ImportError:
    pass
else:
    warnings.filterwarnings("ignore", ".* xmllib .* obsolete.*",
                            DeprecationWarning, 'xmllib$')

tests=0
fails=0

xml_test = open(findfile("test.xml.out")).read()
xml_test_out = open(findfile("test.xml.out")).read()

expected_failures=[
    "xml.sax.drivers.drv_sgmlop", # does not handle &quot; entity reference
    "xml.sax.drivers.drv_xmllib", # reports S before first tag,
                                  # does not report xmlns: attribute
    ]

def summarize(p,result):
    global tests,fails
    tests=tests+1
    if result == xml_test_out:
        if p in expected_failures:
            print p,"XPASS"
        else:
            print p,"PASS"
    elif p in expected_failures:
        print p,"XFAIL"
    else:
        print p,"FAIL"
        fails=fails+1
        if verbose:
            print result
            #open("test.xml."+p,"w").write(result.getvalue())

def test_sax1():
    factory=xml.sax.saxexts.XMLParserFactory
    for p in factory.get_parser_list():
        try:
            parser = factory._create_parser(p)
        except ImportError:
            print p,"NOT SUPPORTED"
            continue
        except SAXReaderNotAvailable:
            print p,"NOT SUPPORTED"
            continue
        result = StringIO()
        xmlgen = ContentGenerator(result)
        parser.setDocumentHandler(xmlgen)
        # We should not pass file names to parse; we don't have
        # any URLs, either
        parser.parseFile(open(findfile("test.xml")))
        summarize(p,result.getvalue())

def test_sax2():
    factory = xml.sax.sax2exts.XMLParserFactory
    for p in factory.get_parser_list():
        try:
            parser = factory._create_parser(p)
        except ImportError:
            print p,"NOT SUPPORTED"
            continue
        except SAXReaderNotAvailable:
            print p,"NOT SUPPORTED"
            continue
        # Don't try to test namespace support, yet
        parser.setFeature(handler.feature_namespaces,0)
        result = StringIO()
        xmlgen = XMLGenerator(result)
        parser.setContentHandler(xmlgen)
        # In SAX2, we can pass an open file object to parse()
        parser.parse(open(findfile("test.xml")))
        summarize(p,result.getvalue())

def test_incremental():
    global tests, fails
    factory = xml.sax.sax2exts.XMLParserFactory
    for p in factory.get_parser_list():
        try:
            parser = factory._create_parser(p)
        except ImportError:
            print p,"NOT SUPPORTED"
            continue
        except SAXReaderNotAvailable:
            print p,"NOT SUPPORTED"
            continue
        if not hasattr(parser, "feed"):
            continue

        # Don't try to test namespace support, yet
        result = StringIO()
        xmlgen = XMLGenerator(result)
        parser.setContentHandler(xmlgen)

        parser.feed("<doc>")
        parser.feed("</doc>")
        parser.close()

        tests = tests + 1
        if result.getvalue() == '<?xml version="1.0" encoding="iso-8859-1"?>\n<doc></doc>':
            print p, "PASS"
        else:
            print p, "FAIL"
            fails = fails + 1


items = locals().items()
items.sort()
for (name, value) in items:
    if name[ : 5] == "test_":
        value()

print "%d tests, %d failures" % (tests, fails)
if fails != 0:
    raise TestFailed, "%d of %d tests failed" % (fails, tests)
