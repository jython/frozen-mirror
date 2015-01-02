"""
SAX driver for Dan Connollys XML scanner. Should work with Python 1.4.
"""

version="0.10"

import sys,urllib2,re,string

if sys.version[:3]<"1.5":
    import saxlib
else:
    from xml.sax import saxlib

import xml_dc

reg_ws="[\n\r\t ]+"
predef_ents={"lt":"<","gt":"<","amp":"&","apos":"'","quot":'"'}

# --- Driver

class SAX_xmldc(saxlib.Parser,saxlib.Locator):

    def __init__(self):
        saxlib.Parser.__init__(self)
        self.current_sysid=""
        self.reset()

    # --- Parser methods

    def parse(self, systemId):
        try:
            self.current_sysid=systemId
            infile=urllib2.urlopen(systemId)
            self.parseFile(infile)
        finally:
            self.current_sysid=""

    def parseFile(self, fileobj):
        self.doc_handler.setDocumentLocator(self)
        self.reset()

        try:
            while 1:
                buf=fileobj.read(16384)
                if buf=="":
                    break

                self.feed(buf)

            self.close()
        except xml_dc.ScanError,e:
            self.err_handler.fatalError(saxlib.SAXParseException(e,None,self))
        except xml_dc.NotWellFormed,e:
            self.err_handler.fatalError(saxlib.SAXParseException(e,None,self))

    # --- Passing on parse events to document handler

    def text(self, str):
        self.doc_handler.characters(str,0,len(str))

    def openStart(self, name):
        self.current_elem=name
        self.current_attrs_val={}
        self.current_attrs_type={}

    def attribute(self, name, type, value):
        self.current_attrs_val[name]=value
        self.current_attrs_type[name]=type

    def closeStart(self):
        self.doc_handler.startElement(self.current_elem,
                                      self.current_attrs_val)

    def closeEmpty(self):
        self.doc_handler.startElement(self.current_elem,
                                      self.current_attrs_val)
        self.doc_handler.endElement(self.current_elem)

    def endTag(self, name=None):
        self.doc_handler.endElement(name)

    def comment(self, stuff):
        pass

    def pi(self, stuff):
        match=re.search(reg_ws,stuff)

        if not match:
            self.doc_handler.processingInstruction(stuff,"")
        else:
            end_of_target,start_of_data=match.span()
            self.doc_handler.processingInstruction(stuff[:end_of_target],
                                                   stuff[start_of_data:])

    def decl(self, name, parts):
        pass

    def cref(self, numeral):
        numeral=string.atoi(numeral)
        self.doc_handler.characters(chr(numeral),0,1)

    def eref(self, name):
        pass

    def eof(self):
        pass

    # --- Locator methods

    def getLineNumber(self):
        return self.parser.line()

    def getSystemId(self):
        return self.current_sysid

    # --- EXPERIMENTAL PYTHON SAX EXTENSIONS

    def get_parser_name(self):
        return "xmldc"

    def get_parser_version(self):
        return "1.8"

    def get_driver_version(self):
        return version

    def is_validating(self):
        return 0

    def is_dtd_reading(self):
        return 0

    def reset(self):
        self.parser=xml_dc.Scanner()
        self.checker=xml_dc.WellFormed()
        self.checker.scanner(self.parser)
        self.unfed_so_far=1

    def feed(self,data):
        if self.unfed_so_far:
            self.doc_handler.startDocument()
            self.unfed_so_far=0

        self.parser.feed(data)
        self.parser.next(self)

    def close(self):
        self.checker.eof()
        self.doc_handler.endDocument()

# ---

def create_parser():
    return SAX_xmldc()
