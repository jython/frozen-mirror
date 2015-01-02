"""
A SAX driver for David Scheres XML-Toolkit parser.
"""

version="0.20"

import sys

from xml.sax import saxlib,saxutils
import XMLFactory,XMLClient,urllib2

class SAX_XTClient(saxlib.Parser,XMLClient.ClientBase):

    def __init__(self):
        XMLClient.ClientBase.__init__(self)
        saxlib.Parser.__init__(self)
        self.reset()

    def text(self,obj):
        v=obj.value()
        self.doc_handler.characters(v,0,len(v))

    def pi(self,obj):
        if obj.nameOf()=="xml": return   # Don't report the XML declaration

        content=""
        for part in obj.value():
            content=content+part.value()+" "

        self.doc_handler.processingInstruction(obj.nameOf(),content[:-1])

    def emptyTag(self,obj):
        attrs={}
        for assoc in obj.value():
            attrs[assoc.nameOf()]=assoc.value()

        self.doc_handler.startElement(obj.nameOf(),
                                      saxutils.AttributeMap(attrs))
        self.doc_handler.endElement(obj.nameOf())

    def nonEmptyTag(self,obj):
        attrs={}
        for assoc in obj.value():
            attrs[assoc.nameOf()]=assoc.value()

        self.doc_handler.startElement(obj.nameOf(),
                                      saxutils.AttributeMap(attrs))

    def endTag(self,obj):
        self.doc_handler.endElement(obj.nameOf())

    def CDATA(self,obj):
        v=obj.value()
        self.doc_handler.characters(v,0,len(v))

    def comment(self,obj):
        pass  # SAX ignores comments

    def parse(self, sysID):
        i=urllib2.urlopen(sysID)
        self.parseFile(i)
        i.close()

    def parseFile(self, file):
        self.reset()
        while 1:
            buf=file.read(16384)
            if buf=="": break
            self.feed(buf)

        self.close()

    # --- EXPERIMENTAL SAX PYTHON EXTENSIONS

    def get_parser_name(self):
        return "xmltoolkit"

    def get_parser_version(self):
        return "Unknown"

    def get_driver_version(self):
        return version

    def is_validating(self):
        return 0

    def is_dtd_reading(self):
        return 0

    def reset(self):
        self.parser=XMLFactory.XMLFactory(self)
        self.unfed_so_far=1

    def feed(self,data):
        if self.unfed_so_far:
            self.doc_handler.startDocument()
            self.unfed_so_far=0

        self.parser.feed(data)

    def close(self):
        self.parser.endfile()
        self.doc_handler.endDocument()

def create_parser():
    return SAX_XTClient()
