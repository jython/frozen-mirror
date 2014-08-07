"""
SAX driver for the Java SAX parsers. Can only be used in Jython.

$Id: drv_javasax.py,v 1.5 2003/01/26 09:08:51 loewis Exp $
"""

# --- Initialization

version = "0.10"
revision = "$Revision: 1.5 $"

import string
from xml.sax import xmlreader, saxutils
from xml.sax.handler import feature_namespaces
from xml.sax import _exceptions

# we only work in jython
import sys
if sys.platform[:4] != "java":
    raise _exceptions.SAXReaderNotAvailable("drv_javasax not available in CPython", None)
del sys

# get the necessary Java SAX classes
try:
    from java.lang import String
    from org.xml.sax import ContentHandler, SAXException
    from org.xml.sax.helpers import XMLReaderFactory
except ImportError:
    raise SAXReaderNotAvailable("SAX is not on the classpath", None)

# get some JAXP stuff
try:
    from javax.xml.parsers import SAXParserFactory, ParserConfigurationException
    factory = SAXParserFactory.newInstance()
    jaxp = 1
except ImportError:
    jaxp = 0

# --- JavaSAXParser

class JavaSAXParser(xmlreader.XMLReader, ContentHandler):
    "SAX driver for the Java SAX parsers."

    def __init__(self, jdriver = None):
        self._parser = create_java_parser(jdriver)
        self._parser.setFeature(feature_namespaces, 0)
        self._parser.setContentHandler(self)
        self._attrs = AttributesImpl()
        self._nsattrs = AttributesNSImpl()

    # XMLReader methods

    def parse(self, source):
        "Parse an XML document from a URL or an InputSource."
        self._source = saxutils.prepare_input_source(source)
        try:
            self._parser.parse(source)
        except SAXException, e:
            raise _exceptions.SAXException("", e)

    def getFeature(self, name):
        return self._parser.getFeature(name)

    def setFeature(self, name, state):
        self._parser.setFeature(name, state)

    def getProperty(self, name):
        return self._parser.getProperty(name)

    def setProperty(self, name, value):
        self._parser.setProperty(name, value)

    # ContentHandler methods

    def setDocumentLocator(self, locator):
        self._cont_handler.setDocumentLocator(locator)

    def startDocument(self):
        self._cont_handler.startDocument()
        self._namespaces = self._parser.getFeature(feature_namespaces)

    def startElement(self, uri, lname, qname, attrs):
        if self._namespaces:
            self._nsattrs._attrs = attrs
            self._cont_handler.startElementNS((uri or None, lname), qname,
                                              self._nsattrs)
        else:
            self._attrs._attrs = attrs
            self._cont_handler.startElement(qname, self._attrs)

    def characters(self, char, start, len):
        self._cont_handler.characters(str(String(char, start, len)))

    def ignorableWhitespace(self, char, start, len):
        self._cont_handler.ignorableWhitespace(str(String(char, start, len)))

    def endElement(self, uri, lname, qname):
        if self._namespaces:
            self._cont_handler.endElementNS((uri or None, lname), qname)
        else:
            self._cont_handler.endElement(qname)

    def endDocument(self):
        self._cont_handler.endDocument()

    def processingInstruction(self, target, data):
        self._cont_handler.processingInstruction(target, data)

# --- AttributesImpl

class AttributesImpl:

    def __init__(self, attrs = None):
        self._attrs = attrs

    def getLength(self):
        return self._attrs.getLength()

    def getType(self, name):
        return self._attrs.getType(name)

    def getValue(self, name):
        value = self._attrs.getValue(name)
        if value == None:
            raise KeyError(name)
        return value

    def getValueByQName(self, name):
        value = self._attrs.getValueByQName(name)
        if value == None:
            raise KeyError(name)
        return value

    def getNameByQName(self, name):
        value = self._attrs.getNameByQName(name)
        if value == None:
            raise KeyError(name)
        return value

    def getQNameByName(self, name):
        value = self._attrs.getQNameByName(name)
        if value == None:
            raise KeyError(name)
        return value

    def getNames(self):
        return self._attrs.getNames()

    def getQNames(self):
        return self._attrs.getQNames()

    def __len__(self):
        return self._attrs.getLength()

    def __getitem__(self, name):
        value = self._attrs.getValue(name)
        if value == None:
            raise KeyError(name)
        return value

    def keys(self):
        qnames = []
        for ix in range(self._attrs.getLength()):
            qnames.append(self._attrs.getQName(ix))
        return qnames

    def copy(self):
        return self.__class__(self._attrs)

    def items(self):
        list = []
        for name in self._attrs.getQNames():
            list.append((name, self._attrs.getValue(name)))
        return list

    def values(self):
        return map(self._attrs.getValue, self._attrs.getQNames())

    def get(self, name, alt = None):
        value = self._attrs.getValue(name)
        if value != None:
            return value
        else:
            return alt

    def has_key(self, name):
        return self._attrs.getValue(name) != None

# --- AttributesNSImpl

class AttributesNSImpl:

    def __init__(self):
        self._attrs = None

# ---

def create_java_parser(jdriver = None):
    try:
        if jdriver:
            return XMLReaderFactory.createXMLReader(jdriver)
        elif jaxp:
            return factory.newSAXParser().getXMLReader()
        else:
            return XMLReaderFactory.createXMLReader()
    except ParserConfigurationException, e:
        raise SAXReaderNotAvailable(e.getMessage())
    except SAXException, e:
        raise SAXReaderNotAvailable(e.getMessage())

def create_parser(jdriver = None):
    return JavaSAXParser(jdriver)
