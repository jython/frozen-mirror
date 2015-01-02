"""
A SAX driver for xmlproc with validation and DTD information.

$Id: drv_xmlproc_val.py,v 1.9 2001/12/30 12:13:45 loewis Exp $
"""

version="0.92"

from xml.sax import saxlib,saxutils
from xml.parsers.xmlproc import xmlval
from xml.sax.drivers.drv_xmlproc import *

import types

# --- SAX_XPValParser

class SAX_XPValParser(SAX_XPParser):

    def __init__(self):
        SAX_XPParser.__init__(self)

    def _create_parser(self):
        return xmlval.XMLValidator()

    def handle_start_tag(self, name, attrs):
        try:
            self.doc_handler.startElement(name,
                                          XPAttributes(attrs,\
                                                       self.parser.dtd.get_elem(name)))
        except KeyError,e:
            self.doc_handler.startElement(name,XPAttributes(attrs,None))

    # --- EXPERIMENTAL PYTHON SAX EXTENSIONS:

    def get_parser_name(self):
        return "xmlproc_val"

    def get_driver_version(self):
        return version

    def is_validating(self):
        return 1

# --- XPAttributes

class XPAttributes(saxutils.AttributeMap):

    def __init__(self,map,elemdecl):
        saxutils.AttributeMap.__init__(self,map)
        self.elemdecl=elemdecl

        if elemdecl==None:
            self.getType=self.getTypeStatic

    def getTypeStatic(self,i):
        return "CDATA"        # Used for undeclared elements

    def getType(self, i):
        if type(i)==types.IntType:
            try:
                i=self.map.keys()[i]
            except KeyError,e:
                return "CDATA"

        try:
            return self.elemdecl.get_attr(i).get_type()
        except KeyError,e:
            return "CDATA"

# --- Global functions

def create_parser():
    return SAX_XPValParser()
