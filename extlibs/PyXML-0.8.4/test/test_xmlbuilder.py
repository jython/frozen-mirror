"""Tests of the extended features of xml.dom.expatbuilder."""

import os
import pprint
import unittest

from cStringIO import StringIO

from xml.dom import XMLNS_NAMESPACE
from xml.dom import xmlbuilder


INTERNAL_SUBSET = ("<!NOTATION x SYSTEM 'http://xml.python.org/notation/x'>\n"
                   "<!ENTITY e SYSTEM 'http://xml.python.org/entity/e'>")
DOCUMENT_SOURCE = (
    '<!DOCTYPE doc [' + INTERNAL_SUBSET.replace('\n', '\r\n') + ''']>
<doc xmlns:a="http://xml.python.org/a"
     xmlns:A="http://xml.python.org/a"
     xmlns:b="http://xml.python.org/b"
     a:a="a" b:b="b"/>
''')


class Tests(unittest.TestCase):

    def setUp(self):
        self.builder = xmlbuilder.DOMBuilder()

    def makeSource(self, text):
        source = xmlbuilder.DOMInputSource()
        source.byteStream = StringIO(text)
        return source

    def check_attrs(self, atts, expected):
        self.assertEqual(atts.length, len(expected))
        info = atts.itemsNS()
        info.sort()
        if info != expected:
            self.fail("bad attribute information:\n" + pprint.pformat(info))

    def run_checks(self, attributes):
        document = self.builder.parse(self.makeSource(DOCUMENT_SOURCE))

        self.assertEqual(document.doctype.internalSubset, INTERNAL_SUBSET)
        self.assertEqual(document.doctype.entities.length, 1,
                         "entity not stored in doctype")

        node = document.doctype.entities['e']
        self.assert_(node.notationName is None)
        self.assert_(node.publicId is None)
        self.assertEqual(node.systemId, 'http://xml.python.org/entity/e')
        self.assertEqual(document.doctype.notations.length, 1)

        node = document.doctype.notations['x']
        self.assert_(node.publicId is None)
        self.assertEqual(node.systemId, 'http://xml.python.org/notation/x')

        self.check_attrs(document.documentElement.attributes, attributes)

    def test_namespace_decls_on(self):
        self.builder.setFeature("namespace_declarations", 1)
        self.run_checks(#((nsuri, localName), value),
                        [((XMLNS_NAMESPACE, "A"), "http://xml.python.org/a"),
                         ((XMLNS_NAMESPACE, "a"), "http://xml.python.org/a"),
                         ((XMLNS_NAMESPACE, "b"), "http://xml.python.org/b"),
                         (("http://xml.python.org/a", "a"), "a"),
                         (("http://xml.python.org/b", "b"), "b"),
                         ])

    def test_namespace_decls_off(self):
        self.builder.setFeature("namespace_declarations", 0)
        self.run_checks(#((nsuri, localName), value),
                        [(("http://xml.python.org/a", "a"), "a"),
                         (("http://xml.python.org/b", "b"), "b"),
                         ])

    def test_get_element_by_id(self):
        ID_PREFIX = "<!DOCTYPE doc [ <!ATTLIST e id ID #IMPLIED> ]>"
        doc = self.builder.parse(self.makeSource(
            ID_PREFIX + "<doc id='foo'><e id='foo'/></doc>"))
        self.assert_(doc.getElementById("bar") is None,
                     "received unexpected node")
        self.assertEqual(doc.getElementById("foo").nodeName, "e",
                         "did not get expected node")
        # Check an implementation detail; this is testing the
        # ID-caching behavior.
        self.assert_(doc._id_cache.has_key("foo"))

        # make sure adding an element with an ID works
        e = doc.createElement("e")
        e.setAttribute("id", "new")
        doc.documentElement.appendChild(e)
        self.assert_(e.isSameNode(doc.getElementById("new")))

        # make sure the cache doesn't cause false hits when we remove nodes
        doc.documentElement.removeChild(e)
        self.assert_(e.parentNode is None)
        self.assert_(doc.getElementById("new") is None)

        # now add the node back, make sure we can still get it by id,
        # the change the value of the id attribute and check that it's
        # returned only for the new ID
        doc.documentElement.appendChild(e)
        self.assert_(e.isSameNode(doc.getElementById("new")))
        a = e.getAttributeNode("id")
        a.value = "no-longer-new"
        self.assert_(doc.getElementById("new") is None)
        self.assert_(e.isSameNode(doc.getElementById("no-longer-new")))

        # make sure removing the attribute makes the ID lookup return None:
        e.removeAttributeNode(a)
        self.assertEqual(e.getAttribute("id"), "")
        self.assert_(doc.getElementById("no-longer-new") is None)

        # check that modifying e.attributes works as well
        attrs = e.attributes
        e.setAttributeNode(a)
        self.assert_(e.isSameNode(doc.getElementById("no-longer-new")))
        attrs.removeNamedItem("id")
        self.assert_(doc.getElementById("no-longer-new") is None)

        a2 = doc.createAttribute("id")
        a2.value = "alternate-id"
        attrs.setNamedItem(a)
        self.assert_(e.isSameNode(doc.getElementById("no-longer-new")))
        attrs.setNamedItem(a2)
        self.assert_(doc.getElementById("no-longer-new") is None)
        self.assert_(e.isSameNode(doc.getElementById("alternate-id")))

        # make sure nodes with an ID in a fragment are not located.
        f = doc.createDocumentFragment()
        e = doc.createElement("e")
        e.setAttribute("id", "in-fragment")
        f.appendChild(e)
        self.assert_(doc.getElementById("in-fragment") is None)

        doc = self.builder.parse(self.makeSource(
            ID_PREFIX + "<doc id='foo'><d id='foo'/><e id='foo'/></doc>"))
        self.assertEqual(doc.getElementById("foo").nodeName, "e",
                         "did not get expected node")

        doc = self.builder.parse(self.makeSource(
            ID_PREFIX + ("<doc id='foo'><e id='foo' name='a'/>"
                         "<e id='bar' name='b'/></doc>")))
        self.assertEqual(doc.getElementById("foo").getAttribute("name"), "a",
                         "did not get expected node")

    def test_whitespace_in_element_content(self):
        DTD_PREFIX = "<!DOCTYPE doc [ <!ELEMENT doc (e*)> ]>"
        doc = self.builder.parse(self.makeSource(
            DTD_PREFIX + ("<doc id='foo'> <e/><e>  </e></doc>")))
        docelem = doc.documentElement
        e1, e2 = docelem.getElementsByTagName("e")
        ws1 = docelem.firstChild
        ws2 = e2.firstChild

        # test WS in element content
        self.assert_(ws1.isWhitespaceInElementContent)
        ws1.appendData("not-white")
        self.assert_(not ws1.isWhitespaceInElementContent)
        ws1.replaceData(0, len(ws1.data), "    ")
        self.assert_(ws1.isWhitespaceInElementContent)
        ws1.replaceData(0, len(ws1.data), "not-white")
        self.assert_(not ws1.isWhitespaceInElementContent)
        ws1.data = "  "
        self.assert_(ws1.isWhitespaceInElementContent)

        # test WS not in element content
        self.assert_(not ws2.isWhitespaceInElementContent)
        ws2.appendData("not-white")
        self.assert_(not ws2.isWhitespaceInElementContent)
        ws2.replaceData(0, len(ws2.data), "    ")
        self.assert_(not ws2.isWhitespaceInElementContent)
        ws2.replaceData(0, len(ws2.data), "not-white")
        self.assert_(not ws2.isWhitespaceInElementContent)
        ws2.data = "  "
        self.assert_(not ws2.isWhitespaceInElementContent)

    def check_resolver(self, content_type, encoding):
        resolver = TestingResolver(content_type)
        source = resolver.resolveEntity(None, DUMMY_URL)
        self.assertEqual(source.encoding, encoding,
                         "wrong encoding; expected %s, got %s"
                         % (repr(encoding), repr(source.encoding)))

    def test_entity_resolver_encodings(self):
        self.check_resolver((None, None, []), None)
        self.check_resolver(("text", "plain", []), None)
        self.check_resolver(("text", "plain", ["charset=iso-8859-1"]),
                            "iso-8859-1")
        self.check_resolver(("text", "plain", ["charset=UTF-8"]), "utf-8")

    def test_internal_subset_isolation(self):
        document = self.builder.parse(self.makeSource(
            "<!DOCTYPE doc ["
            "<!-- comment --> <?pi foo?>"
            "]><doc/>"
            ))
        s = document.toxml()
        self.assertEqual(s,
                         '<?xml version="1.0" ?>\n'
                         '<!DOCTYPE doc ['
                         '<!-- comment --> <?pi foo?>'
                         ']>\n'
                         '<doc/>')

    def test_document_prolog_in_order(self):
        source = self.makeSource(
            "<!-- comment -->\n"
            "<!DOCTYPE doc []>\n"
            "<?pi foo?>\n"
            "<doc/>")
        document = self.builder.parse(source)
        s = document.toxml()
        self.assertEqual(s,
                         '<?xml version="1.0" ?>\n'
                         '<!-- comment -->'
                         '<!DOCTYPE doc []>\n'
                         '<?pi foo?>'
                         '<doc/>')

    def test_docelem_has_namespace(self):
        source = self.makeSource(
            "<doc xmlns='http://xml.python.org/namespace/x'>abc<e/>def</doc>")
        document = self.builder.parse(source)
        self.assertEqual(document.documentElement.namespaceURI,
                         'http://xml.python.org/namespace/x')

    def test_isId(self):
        source = self.makeSource(
            "<!DOCTYPE doc [\n"
            "  <!ATTLIST doc id ID #IMPLIED>\n"
            "]><doc id='name' notid='name'/>")
        document = self.builder.parse(source)
        elem = document.documentElement
        a1 = elem.getAttributeNode("id")
        a2 = elem.getAttributeNode("notid")
        self.failUnless(a1.isId)
        self.failIf(a2.isId)

    def test_schemaType(self):
        source = self.makeSource(
            "<!DOCTYPE doc [\n"
            "  <!ENTITY e1 SYSTEM 'http://xml.python.org/e1'>\n"
            "  <!ENTITY e2 SYSTEM 'http://xml.python.org/e2'>\n"
            "  <!ATTLIST doc id   ID       #IMPLIED \n"
            "                ref  IDREF    #IMPLIED \n"
            "                refs IDREFS   #IMPLIED \n"
            "                enum (a|b)    #IMPLIED \n"
            "                ent  ENTITY   #IMPLIED \n"
            "                ents ENTITIES #IMPLIED \n"
            "                nm   NMTOKEN  #IMPLIED \n"
            "                nms  NMTOKENS #IMPLIED \n"
            "                text CDATA    #IMPLIED \n"
            "    >\n"
            "]><doc id='name' notid='name' text='splat!' enum='b'"
            "       ref='name' refs='name name' ent='e1' ents='e1 e2'"
            "       nm='123' nms='123 abc' />")
        document = self.builder.parse(source)
        elem = document.documentElement
        t = elem.schemaType
        self.assert_(t.name is None)
        self.assert_(t.namespace is None)

        check_attr = self.check_attr_schemaType
        check_attr(elem, "id",    "id")
        check_attr(elem, "notid", None)
        check_attr(elem, "enum",  "enumeration")
        check_attr(elem, "ent",   "entity")
        check_attr(elem, "ents",  "entities")
        check_attr(elem, "ref",   "idref")
        check_attr(elem, "refs",  "idrefs")
        check_attr(elem, "text",  "cdata")

    def check_attr_schemaType(self, elem, attrname, name):
        a = elem.getAttributeNode(attrname)
        t = a.schemaType
        self.assert_(t.namespace is None)
        self.assertEqual(t.name, name)


DUMMY_URL = "http://xml.python.org/dummy.xml"

class TestingResolver(xmlbuilder.DOMEntityResolver):
    def __init__(self, content_type):
        self._content_type = content_type

    def _create_opener(self):
        return FakeOpener(self._content_type)

if os.name == "nt":
    NULLFILE = "nul"
else:
    NULLFILE = "/dev/null"

class FakeOpener:
    def __init__(self, content_type):
        self._content_type = content_type

    def open(self, url):
        if url != DUMMY_URL:
            raise ValueError, "unexpected URL: " + repr(url)
        return FakeFile(open(NULLFILE, "rb"), self._content_type)

class FakeFile:
    def __init__(self, file, content_type):
        self._file = file
        self._content_type = content_type

    def info(self):
        return FakeMessage(self._content_type)

    def __getattr__(self, name):
        return getattr(self._file, name)

class FakeMessage:
    def __init__(self, content_type):
        self._maintype, self._subtype, self._plist = content_type

    def has_key(self, name):
        name = name.lower()
        if name != "content-type":
            raise ValueError, "unexpected has_key(%s)" % repr(name)
        return self._maintype is not None

    def getplist(self):
        return self._plist

    def getmaintype(self):
        return self._maintype or "text"

    def getsubtype(self):
        return self._subtype or "plain"

    def gettype(self):
        return "%s/%s" % (self.getmaintype(), self.getsubtype())


def test_suite():
    return unittest.makeSuite(Tests)

def test_main():
    import test_support
    test_support.run_suite(test_suite())

if __name__ == "__main__":
    import test_support
    test_support.verbose = 1
    test_main()
