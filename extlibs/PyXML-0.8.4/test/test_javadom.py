"""
A suite of unit tests for javadom.py. Hopefully this can also be used with
4DOM.
"""

import sys
import unittest

from xml.dom import javadom

# --- Document

class DocumentTestCase(unittest.TestCase):

    def setUp(self):
        self.document = self.createDocument()

    def checkNodeType(self):
        assert self.document._get_nodeType() == javadom.DOCUMENT_NODE

    def checkNodeName(self):
        assert self.document._get_nodeName() == "#document"

    def checkNodeValue(self):
        assert self.document._get_nodeValue() == None

    def checkAttributes(self):
        assert self.document._get_attributes() == None

    def checkChildNodes(self):
        assert len(self.document._get_childNodes()) == 0

    def checkParentNode(self):
        assert self.document._get_parentNode() == None

    def checkFirstChild(self):
        assert self.document._get_firstChild() == None

    def checkLastChild(self):
        assert self.document._get_lastChild() == None

    def checkPreviousSibling(self):
        assert self.document._get_previousSibling() == None

    def checkNextSibling(self):
        assert self.document._get_nextSibling() == None

    def checkOwnerDocument(self):
        assert self.document._get_ownerDocument() == None

    def checkGetDoctype(self):
        assert self.document._get_doctype() == None

    def checkGetImplementation(self):
        assert self.document._get_implementation() != None

    def checkGetDocumentElement(self):
        assert self.document._get_documentElement() == None

# --- Element

class ElementTestCase(unittest.TestCase):

    def setUp(self):
        self.element = self.createDocument().createElement("per")

    def checkNodeType(self):
        assert self.element._get_nodeType() == javadom.ELEMENT_NODE

    def checkNodeName(self):
        assert self.element._get_nodeName() == "per"

    def checkNodeValue(self):
        assert self.element._get_nodeValue() == None

    def checkAttributes(self):
        assert self.element._get_attributes()._get_length() == 0

    def checkChildNodes(self):
        assert len(self.element._get_childNodes()) == 0

    def checkParentNode(self):
        assert self.element._get_parentNode() == None

    def checkFirstChild(self):
        assert self.element._get_firstChild() == None

    def checkLastChild(self):
        assert self.element._get_lastChild() == None

    def checkPreviousSibling(self):
        assert self.element._get_previousSibling() == None

    def checkNextSibling(self):
        assert self.element._get_nextSibling() == None

    def checkOwnerDocument(self):
        assert self.element._get_ownerDocument() != None

    def checkTagName(self):
        assert self.element._get_tagName() == "per"

    def checkGetAttribute(self):
        assert self.element.getAttribute("ugga") == ""

    def checkGetAttributeNode(self):
        assert self.element.getAttributeNode("ugga") == None

    def checkNormalize(self):
        self.element.normalize()

    def checkRemoveAttribute(self):
        self.element.removeAttribute("ugga")

#     def checkRemoveAttributeNode(self):
#         try:
#             self.element.removeAttributeNode("ugga")  # must have a node
#             result = 0
#         except javadom.DOMException, e:
#             result = 1
#         except:
#             result = 2

#         assert result == 1

# missing: normalize, setAttribute, setAttributeNode, getElementsByTagName

# --- CharacterData

class CharacterDataTestCase(unittest.TestCase):

    def checkChildNodes(self):
        assert len(self.chardata._get_childNodes()) == 0

    def checkParentNode(self):
        assert self.chardata._get_parentNode() == None

    def checkFirstChild(self):
        assert self.chardata._get_firstChild() == None

    def checkLastChild(self):
        assert self.chardata._get_lastChild() == None

    def checkPreviousSibling(self):
        assert self.chardata._get_previousSibling() == None

    def checkNextSibling(self):
        assert self.chardata._get_nextSibling() == None

    def checkOwnerDocument(self):
        assert self.chardata._get_ownerDocument() != None

    def checkGetData(self):
        assert self.chardata._get_data() == "com"

    def checkSetData(self):
        self.chardata._set_data("data")
        assert self.chardata._get_data() == "data"

    def checkGetLength(self):
        assert self.chardata._get_length() == 3

    def checkSubstringData(self):
        assert self.chardata.substringData(0, 2) == "co"

    def checkAppendData(self):
        self.chardata.appendData("com")
        assert self.chardata._get_data() == "comcom"

    def checkInsertData(self):
        self.chardata.insertData(2, "com")
        assert self.chardata._get_data() == "cocomm"

    def checkDeleteData(self):
        self.chardata.deleteData(1, 1)
        assert self.chardata._get_data() == "cm"

    def checkReplaceData(self):
        self.chardata.replaceData(1, 3, "uuuu")
        assert self.chardata._get_data() == "cuuuu"

# --- Comment

class CommentTestCase(CharacterDataTestCase):

    def setUp(self):
        self.chardata = self.createDocument().createComment("com")

    def checkNodeType(self):
        assert self.chardata._get_nodeType() == javadom.COMMENT_NODE

    def checkNodeName(self):
        assert self.chardata._get_nodeName() == "#comment"

    def checkNodeValue(self):
        assert self.chardata._get_nodeValue() == "com"

    def checkAttributes(self):
        assert self.chardata._get_attributes() == None

# --- ProcessingInstruction

class ProcessingInstructionTestCase(unittest.TestCase):

    def setUp(self):
        self.pi = self.createDocument().createProcessingInstruction("pit",
                                                                    "pid")

    def checkNodeType(self):
        assert self.pi._get_nodeType() == javadom.PROCESSING_INSTRUCTION_NODE

    def checkNodeName(self):
        assert self.pi._get_nodeName() == "pit"

    def checkNodeValue(self):
        assert self.pi._get_nodeValue() == "pid"

    def checkAttributes(self):
        assert self.pi._get_attributes() == None

    def checkChildNodes(self):
        assert len(self.pi._get_childNodes()) == 0

    def checkParentNode(self):
        assert self.pi._get_parentNode() == None

    def checkFirstChild(self):
        assert self.pi._get_firstChild() == None

    def checkLastChild(self):
        assert self.pi._get_lastChild() == None

    def checkPreviousSibling(self):
        assert self.pi._get_previousSibling() == None

    def checkNextSibling(self):
        assert self.pi._get_nextSibling() == None

    def checkOwnerDocument(self):
        assert self.pi._get_ownerDocument() != None

    def checkGetTarget(self):
        assert self.pi._get_target() == "pit"

    def checkGetData(self):
        assert self.pi._get_data() == "pid"

    def checkSetData(self):
        self.pi._set_data("uggg")
        assert self.pi._get_data() == "uggg"

# --- Text

class TextTestCase(CharacterDataTestCase):

    def setUp(self):
        self.chardata = self.createDocument().createTextNode("com")

    def checkNodeType(self):
        assert self.chardata._get_nodeType() == javadom.TEXT_NODE

    def checkNodeName(self):
        assert self.chardata._get_nodeName() == "#text"

    def checkNodeValue(self):
        assert self.chardata._get_nodeValue() == "com"

    def checkAttributes(self):
        assert self.chardata._get_attributes() == None

# --- CDATASection

class CDATASectionTestCase(TextTestCase):

    def setUp(self):
        self.chardata = self.createDocument().createCDATASection("com")

    def checkNodeType(self):
        assert self.chardata._get_nodeType() == javadom.CDATA_SECTION_NODE

    def checkNodeName(self):
        assert self.chardata._get_nodeName() == "#cdata-section"

    def checkNodeValue(self):
        assert self.chardata._get_nodeValue() == "com"

    def checkAttributes(self):
        assert self.chardata._get_attributes() == None

# --- Attr

class AttrTestCase(unittest.TestCase):

    def setUp(self):
        self.attr = self.createDocument().createAttribute("name")

    def checkNodeType(self):
        assert self.attr._get_nodeType() == javadom.ATTRIBUTE_NODE

    def checkNodeName(self):
        assert self.attr._get_nodeName() == "name"

    def checkNodeValue(self):
        assert self.attr._get_nodeValue() == None

    def checkAttributes(self):
        assert self.attr._get_attributes() == None

    def checkChildNodes(self):
        assert len(self.attr._get_childNodes()) == 0

    def checkParentNode(self):
        assert self.attr._get_parentNode() == None

    def checkFirstChild(self):
        assert self.attr._get_firstChild() == None

    def checkLastChild(self):
        assert self.attr._get_lastChild() == None

    def checkPreviousSibling(self):
        assert self.attr._get_previousSibling() == None

    def checkNextSibling(self):
        assert self.attr._get_nextSibling() == None

    def checkOwnerDocument(self):
        assert self.attr._get_ownerDocument() != None

    def checkGetName(self):
        assert self.attr._get_name() == "name"

    def checkGetSpecified(self):
        assert self.attr._get_specified()

    def checkGetValue(self):
        assert self.attr._get_value() == None

    def checkSetValue(self):
        self.attr._set_value("14")
        assert self.attr._get_value() == "14"

# --- EntityReference

class EntityReferenceTestCase(unittest.TestCase):

    def setUp(self):
        self.entref = self.createDocument().createEntityReference("eref")

    def checkNodeType(self):
        assert self.entref._get_nodeType() == javadom.ENTITY_REFERENCE_NODE

    def checkNodeName(self):
        assert self.entref._get_nodeName() == "eref"

    def checkNodeValue(self):
        assert self.entref._get_nodeValue() == None

    def checkAttributes(self):
        assert self.entref._get_attributes() == None

    def checkChildNodes(self):
        assert len(self.entref._get_childNodes()) == 0

    def checkParentNode(self):
        assert self.entref._get_parentNode() == None

    def checkFirstChild(self):
        assert self.entref._get_firstChild() == None

    def checkLastChild(self):
        assert self.entref._get_lastChild() == None

    def checkPreviousSibling(self):
        assert self.entref._get_previousSibling() == None

    def checkNextSibling(self):
        assert self.entref._get_nextSibling() == None

    def checkOwnerDocument(self):
        assert self.entref._get_ownerDocument() != None

# --- DocumentFragment

class DocumentFragmentTestCase(unittest.TestCase):

    def setUp(self):
        self.docfrag = self.createDocument().createDocumentFragment()

    def checkNodeType(self):
        assert self.docfrag._get_nodeType() == javadom.DOCUMENT_FRAGMENT_NODE

    def checkNodeName(self):
        assert self.docfrag._get_nodeName() == "#document-fragment"

    def checkNodeValue(self):
        assert self.docfrag._get_nodeValue() == None

    def checkAttributes(self):
        assert self.docfrag._get_attributes() == None

    def checkChildNodes(self):
        assert len(self.docfrag._get_childNodes()) == 0

    def checkParentNode(self):
        assert self.docfrag._get_parentNode() == None

    def checkFirstChild(self):
        assert self.docfrag._get_firstChild() == None

    def checkLastChild(self):
        assert self.docfrag._get_lastChild() == None

    def checkPreviousSibling(self):
        assert self.docfrag._get_previousSibling() == None

    def checkNextSibling(self):
        assert self.docfrag._get_nextSibling() == None

    def checkOwnerDocument(self):
        assert self.docfrag._get_ownerDocument() != None

# --- NodeList

class NodeListTestCase(unittest.TestCase):

    def setUp(self):
        self.list = self.createDocument().createElement("foo")._get_childNodes()

    def checkLen(self):
        assert len(self.list) == 0

    def checkGetLength(self):
        assert self.list._get_length() == 0

    def checkItem(self):
        assert self.list.item(0) == None

    def checkGetItem(self):
        try:
            self.list[0]
            case = 0
        except IndexError:
            case = 1
        except:
            case = 2

        assert case == 1

    def checkGetSlice(self):
        assert self.list[2 : 5] == []

# --- NamedNodeMap

class NamedNodeMapTestCase(unittest.TestCase):

    def setUp(self):
        self.map = self.createDocument().createElement("foo")._get_attributes()

    def checkLen(self):
        assert len(self.map) == 0

    def checkGetLength(self):
        assert self.map._get_length() == 0

    def checkGetNamedItem(self):
        assert self.map.getNamedItem("uuu") == None

    # setNamedItem

    def checkRemoveNamedItem(self):
        try:
            self.map.removeNamedItem("uuu")
            case = 0
        except javadom.DOMException:
            case = 1
        except:
            case = 2

        assert case == 1

    def checkItem(self):
        assert self.map.item(0) == None

    def checkGetItem(self):
        try:
            self.map["uuu"]
            case = 0
        except KeyError:
            case = 1
        except:
            case = 2

        assert case == 1

    def checkGet(self):
        assert self.map.get("uuu", 5) == 5

    def checkHasKey(self):
        assert not self.map.has_key("uuu")

    def checkItems(self):
        assert self.map.items() == []

    def checkKeys(self):
        assert self.map.keys() == []

    def checkValues(self):
        assert self.map.values() == []

# --- Implementation versions

class XercesBase:

    def createDocument(self):
        return javadom.XercesDomImplementation().createDocument()

class BrownellBase:

    def createDocument(self):
        return javadom.BrownellDomImplementation().createDocument()

class SunBase:

    def createDocument(self):
        return javadom.SunDomImplementation().createDocument()

class FourthoughtBase:

    def createDocument(self):
        return Document(None)

class IndelvBase:

    def createDocument(self):
        return javadom.IndelvDomImplementation().createDocument()

class SxpBase:

    def createDocument(self):
        return javadom.SxpDomImplementation().createDocument()

class OpenXmlBase:

    def createDocument(self):
        return javadom.OpenXmlDomImplementation().createDocument()

# --- Create test suite and run it

cases = [DocumentTestCase, ElementTestCase, CommentTestCase,
         ProcessingInstructionTestCase, CDATASectionTestCase,
         TextTestCase, AttrTestCase, EntityReferenceTestCase,
         DocumentFragmentTestCase, NodeListTestCase, NamedNodeMapTestCase]

impls = [XercesBase, BrownellBase, SunBase,# FourthoughtBase,
         IndelvBase, SxpBase, OpenXmlBase]

outf = open("out.txt", "w")

for impl in impls:
    suite = unittest.TestSuite()
    implname = impl.__name__[ : -4]
    outf.write("===== %s =====\n" % implname)

    for case in cases:
        casename = case.__name__[ : -8]
        exec ("class %s%sTestCase(%sBase, %sTestCase): pass" %
              (implname, casename, implname, casename))
        tc = locals()["%s%sTestCase" % (implname, casename)]
        suite.addTests(unittest.makeSuite(tc, 'check')._tests)

    runner = unittest.TextTestRunner(outf)
    runner.run(suite)
    outf.write("\n\n")

outf.close()
