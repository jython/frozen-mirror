"""
A SAX 2.0 driver for sgmllib.

$Id: drv_sgmllib.py,v 1.3 2001/12/30 12:13:45 loewis Exp $
"""

import types, string

import sgmllib
from xml.sax import SAXNotSupportedException, SAXNotRecognizedException
from xml.sax.xmlreader import IncrementalParser

# ===== DRIVER

class SgmllibDriver(sgmllib.SGMLParser, IncrementalParser):

    # ===== SAX 2.0 INTERFACES

    # --- XMLReader methods

    def __init__(self):
        sgmllib.SGMLParser.__init__(self)
        IncrementalParser.__init__(self)
        self._sysid = None
        self._pubid = None

    def prepareParser(self, source):
        self._sysid = source.getSystemId()
        self._pubid = source.getPublicId()
        self._cont_handler.startDocument()

    def close(self):
        sgmllib.SGMLParser.close(self)
        self._cont_handler.endDocument()

    def setLocale(self, locale):
        raise SAXNotSupportedException("setLocale not supported")

    def getFeature(self, name):
        raise SAXNotRecognizedException("Feature '%s' not recognized" % name)

    def setFeature(self, name, state):
        raise SAXNotRecognizedException("Feature '%s' not recognized" % name)

    def getProperty(self, name):
        raise SAXNotRecognizedException("Property '%s' not recognized" % name)

    def setProperty(self, name, value):
        raise SAXNotRecognizedException("Property '%s' not recognized" % name)

    # --- Locator methods

    def getColumnNumber(self):
        return -1

    def getLineNumber(self):
        return -1

    def getPublicId(self):
        return self._pubid

    def getSystemId(self):
        return self._sysid

    # ===== HTMLLIB INTERFACES

    def unknown_starttag(self, name, attrs):
        self._cont_handler.startElement(name, AttributesImpl(attrs))

    def unknown_endtag(self, name):
        self._cont_handler.endElement(name)

    def handle_data(self, data):
        self._cont_handler.characters(data)

# ===== ATTRIBUTESIMPL =====

class AttributesImpl:

    def __init__(self, attrs):
        "attrs has the form [(name, value), (name, value)...]"
        self._attrs = attrs

    def getLength(self):
        return len(self._attrs)

    def getType(self, name):
        return "CDATA"

    def getValue(self, name):
        for (aname, avalue) in self._attrs:
            if aname == name:
                return avalue
        raise KeyError, name

    def getValueByQName(self, name):
        for (aname, avalue) in self._attrs:
            if aname == name:
                return avalue
        raise KeyError, name

    def getNameByQName(self, name):
        for (aname, avalue) in self._attrs:
            if aname == name:
                return name
        raise KeyError, name

    def getQNameByName(self, name):
        return self.getNameByQName(name)

    def getNames(self):
        return map(lambda x: x[0], self._attrs)

    def getQNames(self):
        return map(lambda x: x[0], self._attrs)

    def __len__(self):
        return len(self._attrs)

    def __getitem__(self, name):
        for (aname, avalue) in self._attrs:
            if aname == name:
                return avalue
        raise KeyError, name

    def keys(self):
        return self.getNames()

    def has_key(self, name):
        for (aname, avalue) in self._attrs:
            if aname == name:
                return 1
        return 0

    def get(self, name, alternative=None):
        for (aname, avalue) in self._attrs:
            if aname == name:
                return avalue

    def copy(self):
        return self.__class__(self._attrs)

    def items(self):
        return self._attrs

    def values(self):
        return map(lambda x: x[1], self._attrs)

# ---

def create_parser():
    return SgmllibDriver()
