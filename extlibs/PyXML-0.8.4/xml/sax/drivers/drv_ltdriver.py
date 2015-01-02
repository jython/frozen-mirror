"""
A SAX driver for the LT XML Python interface.
"""

version="0.10"

from types import *
from xml.sax import saxlib,saxutils
from XMLinter import *

# --- The parser

class SAX_XMLinter(saxlib.Parser):

    def __init__(self):
        saxlib.Parser.__init__(self)

    def parse(self,sysID):
        self._parse(Open(sysID,NSL_read))

    def parseFile(self,file):
        self._parse(FOpen(file,NSL_read))

    def setLocale(self, locale):
        raise SAXException("Locales not supported")

    # --- EXPERIMENTAL PYTHON SAX EXTENSIONS:

    def get_parser_name(self):
        return "XMLinter"

    def get_parser_version(self):
        return "Unknown"

    def get_driver_version(self):
        return version

    def is_validating(self):
        return 0

    def is_dtd_reading(self):
        return 1

    def reset(self):
        raise SAXException("Incremental parsing not supported")

    def feed(self,data):
        raise SAXException("Incremental parsing not supported")

    def close(self):
        raise SAXException("Incremental parsing not supported")

    # --- INTERNAL METHODS

    def _parse(self,file):
        bit=GetNextBit(file)
        while bit:
            if bit.type=="start":
                self.doc_handler.startElement(bit.label,
                                              AttributeItem(bit.item))
            elif bit.type=="end":
                self.doc_handler.endElement(bit.label)
            elif bit.type=="text":
                self.doc_handler.characters(bit.body,0,len(bit.body))
            elif bit.type=="empty":
                self.doc_handler.startElement(bit.label,
                                              AttributeItem(bit.item))
                self.doc_handler.endElement(bit.label)
            elif bit.type=="bad":
                self.err_handler.fatalError(saxlib.SAXException("Syntax error",None))
            elif bit.type=="pi":
                print "?pi"
            else:
                print "###"+bit.type

            bit=GetNextBit(file)

# --- AttributeItem

def name(pair):
    return pair[0]

class AttributeItem:

    def __init__(self,item):
        self.item=item
        self.list=ItemActualAttributes(item)

    def getLength(self):
        return len(self.list)

    def getName(self, i):
        return self.list[i][0]

    def getType(self, i):
        return "CDATA"

    def getValue(self, i):
        if type(i)==StringType:
            return GetAttrVal(self.item,i)
        else:
            return self.list[i][1]

    def __len__(self):
        return len(self.list)

    def __getitem__(self, key):
        if type(key)==StringType:
            return GetAttrVal(self.item,key)
        else:
            return self.list[key][0]

    def keys(self):
        return map(name,self.list)

    def has_key(self, key):
        return GetAttrVal(self.item,key)

# --- Global functions

def create_parser():
    return SAX_XMLinter()

# --- Testing

if __name__=="__main__":
    p=create_parser()
    p.setDocumentHandler(saxutils.Canonizer())
    p.setErrorHandler(saxutils.ErrorPrinter())
    p.parse("tst.xml")
