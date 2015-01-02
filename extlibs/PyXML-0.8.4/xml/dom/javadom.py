"""An adapter for Java DOM implementations that makes it possible to
access them through the same interface as the Python DOM implementations.

Supports:
- Sun's Java Project X
- Xerces
- David Brownell's SAX 2.0 Utilities / DOM2
- Indelv DOM
- SXP
- OpenXML

$Id: javadom.py,v 1.7 2001/02/19 15:21:50 fdrake Exp $
"""

# Todo:
# - extend test suite
# - start using _set_up_attributes, or give up as too slow?
# - support level 2

import string

# --- Supported Java DOM implementations

class BaseDomImplementation:
    """An abstract DomImplementation with some reusable implementations
    of build* methods that depend on a lower-level _parse_from_source
    method."""

    def buildDocumentString(self, string):
        from java.io import StringReader
        from org.xml.sax import InputSource
        return self._parse_from_source(InputSource(StringReader(string)))

    def buildDocumentUrl(self, url):
        return self._parse_from_source(url)

    def buildDocumentFile(self, filename):
        return self.buildDocumentUrl(filetourl(filename))

class SunDomImplementation:

    def createDocument(self):
        from com.sun.xml.tree import XmlDocument
        return Document(XmlDocument())

    def buildDocumentString(self, string):
        from com.sun.xml.tree import XmlDocumentBuilder
        return Document(XmlDocumentBuilder.createXmlDocument(string))

    def buildDocumentUrl(self, url):
        from com.sun.xml.tree import XmlDocument
        return Document(XmlDocument.createXmlDocument(url))

    def buildDocumentFile(self, filename):
        return self.buildDocumentUrl(filetourl(filename))

class XercesDomImplementation(BaseDomImplementation):

    def createDocument(self):
        from org.apache.xerces.dom import DocumentImpl
        return Document(DocumentImpl())

    def _parse_from_source(self, source):
        from org.apache.xerces.parsers import DOMParser
        p = DOMParser()
        p.parse(source)
        return Document(p.getDocument())

class BrownellDomImplementation(BaseDomImplementation):

    def createDocument(self):
        from org.brownell.xml.dom import DomDocument
        return Document(DomDocument())

    def _parse_from_source(self, source):
        from org.brownell.xml import DomBuilder
        return Document(DomBuilder.createDocument(source))

class IndelvDomImplementation(BaseDomImplementation):

    def createDocument(self):
        from com.indelv.dom import DOMImpl
        return Document(DOMImpl.createNewDocument())

    def _parse_from_source(self, source):
        from com.indelv.dom.util import XMLReader
        from org.xml.sax import InputSource
        return Document(XMLReader.parseDocument(InputSource(source)))

class SxpDomImplementation(BaseDomImplementation):

    def createDocument(self):
        from fr.loria.xml import DOMFactory
        return Document(DOMFactory().createDocument())

    def _parse_from_source(self, source):
        from fr.loria.xml import DocumentLoader
        loader = DocumentLoader()

        if type(source) == type(""):
            doc = loader.loadDocument(source)
        elif source.getCharacterStream() != None:
            doc = loader.loadDocument(source.getCharacterStream())
        elif source.getByteStream() != None:
            doc = loader.loadDocument(source.getByteStream())
        elif source.getSystemId() != None:
            doc = loader.loadDocument(source.getSystemId())

        return Document(doc)

class OpenXmlDomImplementation(BaseDomImplementation):

    def createDocument(self):
        from org.openxml.dom import DocumentImpl
        return Document(DocumentImpl())

    def _parse_from_source(self, source):
        from org.openxml.dom import SAXBuilder
        from org.openxml.parser import XMLSAXParser

        builder = SAXBuilder()
        parser = XMLSAXParser()
        parser.setDocumentHandler(builder)
        parser.parse(source)
        return Document(builder.getDocument())

# ===== Utilities

def filetourl(file):
    # A Python port of James Clark's fileToURL from XMLTest.java.
    from java.io import File
    from java.net import URL
    from java.lang import System

    file = File(file).getAbsolutePath()
    sep = System.getProperty("file.separator")

    if sep != None and len(sep) == 1:
        file = file.replace(sep[0], '/')

    if len(file) > 0 and file[0] != '/':
        file = '/' + file

    return URL('file', None, file).toString()

def _wrap_node(node):
    if node == None:
        return None

    return NODE_CLASS_MAP[node.getNodeType()] (node)

# ===== Constants

ELEMENT_NODE                = 1
ATTRIBUTE_NODE              = 2
TEXT_NODE                   = 3
CDATA_SECTION_NODE          = 4
ENTITY_REFERENCE_NODE       = 5
ENTITY_NODE                 = 6
PROCESSING_INSTRUCTION_NODE = 7
COMMENT_NODE                = 8
DOCUMENT_NODE               = 9
DOCUMENT_TYPE_NODE          = 10
DOCUMENT_FRAGMENT_NODE      = 11
NOTATION_NODE               = 12

# ===== DOMException

try:
    from org.w3c.dom import DOMException
except ImportError, e:
    pass

# ===== DOMImplementation

class DOMImplementation:

    def __init__(self, impl):
        self._impl = impl

    def hasFeature(self, feature, version):
        if version == None or version == "1.0":
            return string.lower(feature) == "xml" and \
                   self._impl.hasFeature(feature, version)
        else:
            return 0

    def __repr__(self):
        return "<DOMImplementation javadom.py, using '%s'>" % self._impl

# ===== Node

class Node:

    def __init__(self, impl):
        self.__dict__['_impl'] = impl

    # attributes

    def _get_nodeName(self):
        return self._impl.getNodeName()

    def _get_nodeValue(self):
        return self._impl.getNodeValue()

    def _get_nodeType(self):
        return self._impl.getNodeType()

    def _get_parentNode(self):
        return _wrap_node(self._impl.getParentNode())

    def _get_childNodes(self):
        children = self._impl.getChildNodes()
        if children is None:
            return children
        else:
            return NodeList(children)

    def _get_firstChild(self):
        return _wrap_node(self._impl.getFirstChild())

    def _get_lastChild(self):
        return _wrap_node(self._impl.getLastChild())

    def _get_previousSibling(self):
        return _wrap_node(self._impl.getPreviousSibling())

    def _get_nextSibling(self):
        return _wrap_node(self._impl.getNextSibling())

    def _get_ownerDocument(self):
        return _wrap_node(self._impl.getOwnerDocument())

    def _get_attributes(self):
        atts = self._impl.getAttributes()
        if atts is None:
            return None
        else:
            return NamedNodeMap(atts)

    # methods

    def insertBefore(self, new, neighbour):
        self._impl.insertBefore(new._impl, neighbour._impl)

    def replaceChild(self, new, old):
        self._impl.replaceChild(new._impl, old._impl)
        return old

    def removeChild(self, old):
        self._impl.removeChild(old._impl)
        return old

    def appendChild(self, new):
        return self._impl.appendChild(new._impl)

    def hasChildNodes(self):
        return self._impl.hasChildNodes()

    def cloneNode(self):
        return _wrap_node(self._impl.cloneNode())

    # python

    def __getattr__(self, name):
        if name[ : 5] != '_get_':
            return getattr(self, '_get_' + name) ()

        raise AttributeError, name

    def __setattr__(self, name, value):
        getattr(self, '_set_' + name) (value)

# ===== Document

class Document(Node):

    def __init__(self, impl):
        Node.__init__(self, impl)

    # methods

    def createTextNode(self, data):
        return Text(self._impl.createTextNode(data))

    def createEntityReference(self, name):
        return EntityReference(self._impl.createEntityReference(name))

    def createElement(self, name):
        return Element(self._impl.createElement(name))

    def createDocumentFragment(self):
        return DocumentFragment(self._impl.createDocumentFragment())

    def createComment(self, data):
        return Comment(self._impl.createComment(data))

    def createCDATASection(self, data):
        return CDATASection(self._impl.createCDATASection(data))

    def createProcessingInstruction(self, target, data):
        return ProcessingInstruction(self._impl.createProcessingInstruction(target, data))

    def createAttribute(self, name):
        return Attr(self._impl.createAttribute(name))

    def getElementsByTagName(self, name):
        return NodeList(self._impl.getElementsByTagName(name))

    # attributes

    def _get_doctype(self):
        return self._impl.getDoctype()

    def _get_implementation(self):
        return DOMImplementation(self._impl.getImplementation())

    def _get_documentElement(self):
        return _wrap_node(self._impl.getDocumentElement())

    # python

    def __repr__(self):
        docelm = self._impl.getDocumentElement()
        if docelm:
            return "<Document with root '%s'>" % docelm.getTagName()
        else:
            return "<Document with no root>"

# ===== Element

class Element(Node):

    def __init__(self, impl):
        Node.__init__(self, impl)

        self.__dict__['_get_tagName']    = self._impl.getTagName
        self.__dict__['getAttribute']    = self._impl.getAttribute
        self.__dict__['setAttribute']    = self._impl.setAttribute
        self.__dict__['removeAttribute'] = self._impl.removeAttribute
        self.__dict__['normalize']       = self._impl.normalize

    # methods

    def getAttributeNode(self, name):
        node = self._impl.getAttributeNode(name)
        if node == None:
            return node
        else:
            return Attr(node)

    def setAttributeNode(self, attr):
        self._impl.setAttributeNode(attr._impl)

    def removeAttributeNode(self, attr):
        self._impl.removeAttributeNode(attr._impl)

    def getElementsByTagName(self, name):
        return NodeList(self._impl.getElementsByTagName(name))

    # python

    def __repr__(self):
        return "<Element '%s' with %d attributes and %d children>" % \
               (self._impl.getTagName(),
                self._impl.getAttributes().getLength(),
                self._impl.getChildNodes().getLength())

# ===== CharacterData

class CharacterData(Node):

    def __init__(self, impl):
        Node.__init__(self, impl)

        self.__dict__['_get_data']     = self._impl.getData
        self.__dict__['_set_data']     = self._impl.setData
        self.__dict__['_get_length']   = self._impl.getLength

        self.__dict__['substringData'] = self._impl.substringData
        self.__dict__['appendData']    = self._impl.appendData
        self.__dict__['insertData']    = self._impl.insertData
        self.__dict__['deleteData']    = self._impl.deleteData
        self.__dict__['replaceData']   = self._impl.replaceData

# ===== Comment

class Comment(CharacterData):

    def __repr__(self):
        return "<Comment of length %d>" % self.getLength()

# ===== ProcessingInstruction

class ProcessingInstruction(Node):

    def __init__(self, impl):
        Node.__init__(self, impl)

        self.__dict__['_get_target'] = self._impl.getTarget
        self.__dict__['_get_data']   = self._impl.getData
        self.__dict__['_set_data']   = self._impl.setData

    def __repr__(self):
        return "<PI with target '%s'>" % self._impl.getTarget()

# ===== Text

class Text(CharacterData):

    def splitText(self, offset):
        return Text(self._impl.splitText(offset))

    def __repr__(self):
        return "<Text of length %d>" % self._impl.getLength()

# ===== CDATASection

class CDATASection(Text):

    def __repr__(self):
        return "<CDATA section of length %d>" % self._impl.getLength()

# ===== Attr

class Attr(Node):

    def __init__(self, impl):
        Node.__init__(self, impl)

        self.__dict__['_get_name']      = self._impl.getName
        self.__dict__['_get_specified'] = self._impl.getSpecified
        self.__dict__['_get_value']     = self._impl.getValue
        self.__dict__['_set_value']     = self._impl.setValue

    def __repr__(self):
        return "<Attr '%s'>" % self._impl.getName()

# ===== EntityReference

class EntityReference(Node):

    def __repr__(self):
        return "<EntityReference '%s'>" % self.getNodeName()

# ===== DocumentType

class DocumentType(Node):

    def __init__(self, impl):
        Node.__init__(self, impl)

        self.__dict__['_get_name'] = self._impl.getName

    def _get_entities(self):
        return NamedNodeMap(self._impl.getEntities())

    def _get_notations(self):
        return NamedNodeMap(self._impl.getNotations())

    def __repr__(self):
        return "<DocumentType '%s'>" % self._impl.getNodeName()

# ===== Notation

class Notation(Node):

    def __init__(self, impl):
        Node.__init__(self, impl)

        self.__dict__['_get_publicId'] = self._impl.getPublicId
        self.__dict__['_get_systemId'] = self._impl.getSystemId

    def __repr__(self):
        return "<Notation '%s'>" % self._impl.getNodeName()

# ===== Entity

class Entity(Node):

    def __init__(self, impl):
        Node.__init__(self, impl)

        self.__dict__['_get_publicId']     = self._impl.getPublicId
        self.__dict__['_get_systemId']     = self._impl.getSystemId
        self.__dict__['_get_notationName'] = self._impl.getNotationName

    def __repr__(self):
        return "<Entity '%s'>" % self._impl.getNodeName()

# ===== DocumentFragment

class DocumentFragment(Node):

    def __repr__(self):
        return "<DocumentFragment>"

# ===== NodeList

class NodeList:

    def __init__(self, impl):
        self._impl = impl

        self.__dict__['__len__']     = self._impl.getLength
        self.__dict__['_get_length'] = self._impl.getLength
        self.__dict__['item']        = self._impl.item

    # Python list methods

    def __getitem__(self, ix):
        if ix < 0:
            ix = len(self) + ix

        node = self._impl.item(ix)
        if node == None:
            raise IndexError, ix
        else:
            return _wrap_node(node)

    def __setitem__(self, ix, item):
        raise TypeError, "NodeList instances don't support item assignment"

    def __delitem__(self, ix, item):
        raise TypeError, "NodeList instances don't support item deletion"

    def __setslice__(self, i, j, list):
        raise TypeError, "NodeList instances don't support slice assignment"

    def __delslice__(self, i, j):
        raise TypeError, "NodeList instances don't support slice deletion"

    def append(self, item):
        raise TypeError, "NodeList instances don't support .append()"

    def insert(self, i, item):
        raise TypeError, "NodeList instances don't support .insert()"

    def pop(self, i=-1):
        raise TypeError, "NodeList instances don't support .pop()"

    def remove(self, item):
        raise TypeError, "NodeList instances don't support .remove()"

    def reverse(self):
        raise TypeError, "NodeList instances don't support .reverse()"

    def sort(self, *args):
        raise TypeError, "NodeList instances don't support .sort()"

    def __add__(self, *args):
        raise TypeError, "NodeList instances don't support +"

    def __radd__(self, *args):
        raise TypeError, "NodeList instances don't support +"

    def __mul__(self, *args):
        raise TypeError, "NodeList instances don't support *"

    def __rmul__(self, *args):
        raise TypeError, "NodeList instances don't support *"

    def count(self, *args):
        raise TypeError, "NodeList instances can't support count without equality"

    def count(self, *args):
        raise TypeError, "NodeList instances can't support index without equality"

    def __getslice__(self, i, j):
        if i < len(self):
            i = len(self) + i
        if j < len(self):
            j = len(self) + j

        slice = []
        for ix in range(i, min(j, len(self))):
            slice.append(self[ix])
        return slice

    def __repr__(self):
        return "<NodeList [ %s ]>" % string.join(map(repr, self), ", ")

# ===== NamedNodeMap

class NamedNodeMap:

    def __init__(self, impl):
        self._impl = impl

        self.__dict__['_get_length'] = self._impl.getLength
        self.__dict__['__len__']     = self._impl.getLength

    # methods

    def getNamedItem(self, name):
        return _wrap_node(self._impl.getNamedItem(name))

    def setNamedItem(self, node):
        return _wrap_node(self._impl.setNamedItem(node._impl))

    def removeNamedItem(self, name):
        return _wrap_node(self._impl.removeNamedItem(name))

    def item(self, index):
        return _wrap_node(self._impl.item(index))

    # Python dictionary methods

    def __getitem__(self, key):
        node = self._impl.getNamedItem(key)

        if node is None:
            raise KeyError, key
        else:
            return _wrap_node(node)

    def get(self, key, alternative = None):
        node = self._impl.getNamedItem(key)
        if node is None:
            return alternative
        else:
            return _wrap_node(node)

    def has_key(self, key):
        return self._impl.getNamedItem(key) != None

    def items(self):
        list = []
        for ix in range(self._impl.getLength()):
            node = self._impl.item(ix)
            list.append((node.getNodeName(), _wrap_node(node)))
        return list

    def keys(self):
        list = []
        for ix in range(self._impl.getLength()):
            list.append(self._impl.item(ix)._get_nodeName())
        return list

    def values(self):
        list = []
        for ix in range(self._impl.getLength()):
            list.append(_wrap_node(self._impl.item(ix)))
        return list

    def __setitem__(self, key, item):
        assert key == item._impl._get_nodeName()
        self._impl.setNamedItem(item._impl)

    def update(self, nnm):
        for v in nnm.values():
            self._impl.setNamedItem(v._impl)

    def __repr__(self):
        pairs = []
        for pair in self.items():
            pairs.append("'%s' : %s" % pair)
        return "<NamedNodeMap { %s }>" % string.join(pairs, ", ")

# ===== Various stuff

NODE_CLASS_MAP = {
    ELEMENT_NODE : Element,
    ATTRIBUTE_NODE : Attr,
    TEXT_NODE : Text,
    CDATA_SECTION_NODE : CDATASection,
    ENTITY_REFERENCE_NODE : EntityReference,
    ENTITY_NODE : Entity,
    PROCESSING_INSTRUCTION_NODE : ProcessingInstruction,
    COMMENT_NODE : Comment,
    DOCUMENT_NODE : Document,
    DOCUMENT_TYPE_NODE : DocumentType,
    DOCUMENT_FRAGMENT_NODE : DocumentFragment,
    NOTATION_NODE : Notation
    }

# ===== Self-test

if __name__ == "__main__":
    impl = BrownellDomImplementation() #XercesDomImplementation()  #SunDomImplementation()
    doc2 = impl.createDocument()
    print doc2
    print doc2._get_implementation()
    root = doc2.createElement("doc")
    print root
    doc2.appendChild(root)
    txt = doc2.createTextNode("This is a simple sample \n")
    print txt
    root.appendChild(txt)

    print root._get_childNodes()[0]
    print root._get_childNodes()

    root.setAttribute("huba", "haba")
    print root
    print root._get_attributes()
