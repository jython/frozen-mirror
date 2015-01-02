"""
SAX driver for the sgmlop parser.

$Id: drv_sgmlop.py,v 1.10 2002/08/13 09:28:52 afayolle Exp $
"""

version="0.12"

from xml.parsers import sgmlop
from xml.sax import saxlib,saxutils
from xml.sax import SAXException
import urllib2,string

# --- Driver

class Parser(saxlib.Parser):

    def __init__(self):
        saxlib.Parser.__init__(self)
        self.reset()

    def setDocumentHandler(self, dh):
        self.parser.register(self) # older version wanted ,1 arg
        self.doc_handler=dh

    def parse(self, url):
        self.parseFile(urllib2.urlopen(url))

    def parseFile(self, file):
        self._parsing = 1
        self.doc_handler.startDocument()
        parser = self.parser

        while 1:
            data = file.read(16384)
            if not data:
                break
            parser.feed(data)

        self.close()

    # --- SAX 1.0 METHODS

    def handle_cdata(self, data):
        self.doc_handler.characters(data,0,len(data))

    def handle_data(self, data):
        #ignore white space outside the toplevel element
        if self._nesting == 0:
            if string.strip(data)!="":
                # It's not whitespace?
                self.err_handler.error(SAXException(
                    "characters '%s' outside root element" % data))
            return
        self.doc_handler.characters(data,0,len(data))

    def handle_proc(self, target, data):
        if target=='xml':
            # Don't report <?xml?> as a processing instruction
            return
        self.doc_handler.processingInstruction(target,data)

    def handle_charref(self, charno):
        if charno<256:
            self.doc_handler.characters(chr(charno),0,1)

    def finish_starttag(self, name, attrs):
        self._nesting = self._nesting + 1
        self.doc_handler.startElement(name,saxutils.AttributeMap(attrs))

    def finish_endtag(self,name):
        self._nesting = self._nesting - 1
        self.doc_handler.endElement(name)

    # --- EXPERIMENTAL PYTHON SAX EXTENSIONS

    def get_parser_name(self):
        return "sgmlop"

    def get_parser_version(self):
        return "Unknown"

    def get_driver_version(self):
        return version

    def is_validating(self):
        return 0

    def is_dtd_reading(self):
        return 0

    def reset(self):
        self.parser=sgmlop.XMLParser()
        self._parsing=0
        self._nesting=0

    def feed(self,data):
        if not self._parsing:
            self.doc_handler.startDocument()
            self._parsing=1
        self.parser.feed(data)

    def close(self):
        self.parser.close()
        self.doc_handler.endDocument()

# ----

def create_parser():
    return Parser()
