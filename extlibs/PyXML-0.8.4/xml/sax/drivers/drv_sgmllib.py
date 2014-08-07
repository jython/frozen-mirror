"""
SAX driver for sgmllib.py
"""

version="0.10"

from xml.sax import saxutils,saxlib
from xml.sax.drivers import pylibs

import sgmllib,string,sys

# --- SAX_SLParser

class SAX_SLParser(pylibs.SGMLParsers,sgmllib.SGMLParser):
    "SAX driver for sgmllib.py."

    def __init__(self):
        sgmllib.SGMLParser.__init__(self)
        pylibs.LibParser.__init__(self)
        self.standalone=0

    # --- EXPERIMENTAL PYTHON SAX EXTENSIONS

    def get_parser_name(self):
        return "sgmllib"

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
        sgmllib.SGMLParser.close(self)
        self.doc_handler.endDocument()

# --- Global functions

def create_parser():
    return SAX_SLParser()
