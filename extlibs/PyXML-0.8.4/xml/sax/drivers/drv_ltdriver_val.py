"""
A validating-mode SAX driver for the LT XML Python interface.
"""

version="0.10"

import drv_ltdriver
from XMLinter import *

class SAX_XMLinter_val(drv_ltdriver.SAX_XMLinter):

    def __init__(self):
        drv_ltdriver.SAX_XMLinter.__init__(self)

    def parse(self,sysID):
        self._parse(Open(sysID,NSL_read | NSL_read_validate))

    def parseFile(self,file):
        self._parse(FOpen(file,NSL_read | NSL_read_validate))

    def get_parser_name(self):
        return "XMLinter_val"

    def get_driver_version(self):
        return version

    def is_validating(self):
        return 0

# --- Global functions

def create_parser():
    return SAX_XMLinter_val()

# --- Testing

if __name__=="__main__":
    from xml.sax import saxutils
    p=create_parser()
    p.setDocumentHandler(saxutils.Canonizer())
    p.setErrorHandler(saxutils.ErrorPrinter())
    p.parse("tst.xml")
