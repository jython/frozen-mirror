"""
SAX driver for xmllib.py
"""

version="0.91"

from xml.sax import saxutils
from xml.sax.drivers import pylibs

import xmllib

# Make it generate Unicode if possible, UTF-8 else
try:
    unicode("")
except NameError:
    from xml.unicode.iso8859 import wstring
    def unicode(str, encoding):
        return wstring.decode(encoding, str).utf8()

# --- SAX_XLParser

class SAX_XLParser(pylibs.LibParser, xmllib.XMLParser):
    "SAX driver for xmllib.py."

    def __init__(self):
        xmllib.XMLParser.__init__(self)
        pylibs.LibParser.__init__(self)
        self.standalone = 0
        self.reset()

    def _convert(self, str):
        return unicode(str, self.encoding)

    def unknown_starttag(self, tag, attributes):
        tag = unicode(tag, self.encoding)
        newattr = {}
        for k, v in attributes.items():
            newattr[unicode(k, self.encoding)] = unicode(v, self.encoding)
        self.doc_handler.startElement(tag, saxutils.AttributeMap(newattr))

    def handle_endtag(self, tag, method):
        self.doc_handler.endElement(unicode(tag, self.encoding))

    def handle_proc(self, name, data):
        self.doc_handler.processingInstruction(name, data[1:])

    def handle_xml(self, encoding, standalone):
        self.standalone = standalone == "yes"
        if encoding is not None:
            self.encoding = encoding

    def handle_data(self, data):
        "Handles PCDATA."
        data = unicode(data, self.encoding)
        self.doc_handler.characters(data, 0, len(data))

    def handle_cdata(self, data):
        "Handles CDATA marked sections."
        data = unicode(data, self.encoding)
        self.doc_handler.characters(data, 0, len(data))

    def getLineNumber(self):
        return self.lineno

    def getSystemId(self):
        return self.sysID

    def _can_locate(self):
        "Internal: returns true if location info is available."
        return 1

    # --- EXPERIMENTAL SAX PYTHON EXTENSIONS

    def get_parser_name(self):
        return "xmllib"

    def get_parser_version(self):
        return xmllib.version

    def get_driver_version(self):
        return version

    def is_validating(self):
        return 0

    def is_dtd_reading(self):
        return 0

    def reset(self):
        xmllib.XMLParser.reset(self)
        self.unfed_so_far = 1
        self.encoding = "utf-8"

    def feed(self, data):
        if self.unfed_so_far:
            self.doc_handler.startDocument()
            self.unfed_so_far = 0

        xmllib.XMLParser.feed(self, data)

    def close(self):
        xmllib.XMLParser.close(self)
        self.doc_handler.endDocument()

# --- Global functions

def create_parser():
    return SAX_XLParser()
