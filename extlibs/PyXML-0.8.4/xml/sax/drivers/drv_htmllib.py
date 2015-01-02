"""
SAX driver for htmllib.py

$Id: drv_htmllib.py,v 1.5 2001/12/30 12:13:44 loewis Exp $
"""

version="0.10"

from xml.sax import saxutils,saxlib
from xml.sax.drivers import pylibs

import htmllib,sys,string

# --- SAX_HLParser

class SAX_HLParser(pylibs.SGMLParsers,htmllib.HTMLParser):
    "SAX driver for htmllib.py."

    def __init__(self):
        htmllib.HTMLParser.__init__(self,None)
        pylibs.LibParser.__init__(self)
        self.standalone=0

    # --- EXPERIMENTAL PYTHON SAX EXTENSIONS

    def get_parser_name(self):
        return "htmllib"

    def get_parser_version(self):
        return sys.version[:string.find(sys.version," ")]

    def get_driver_version(self):
        return version

    def is_validating(self):
        return 0

    def is_dtd_reading(self):
        return 0

    # reset and feed are taken care of by the subclassing :-)

    def close(self):
        htmllib.HTMLParser.close(self)
        self.doc_handler.endDocument()

# --- Global functions

def create_parser():
    return SAX_HLParser()
