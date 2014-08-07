"""
A SAX driver for xmlproc

$Id: drv_xmlproc.py,v 1.13 2001/12/30 12:13:45 loewis Exp $
"""

version="0.95"

from xml.sax import saxlib, saxutils
from xml.parsers.xmlproc import xmlproc

import os

# --- SAX_XPParser

class SAX_XPParser(saxlib.Parser,xmlproc.Application,xmlproc.DTDConsumer,
                   xmlproc.ErrorHandler,xmlproc.PubIdResolver):

    def __init__(self):
        saxlib.Parser.__init__(self)
        self.reset()
        self.ns_separator=" "
        self.locator=1
        self.is_parsing=0
        self.stop_on_error=1

    def parse(self,sysID):
        self.reset()
        try:
            self.is_parsing=1
            self.parser.parse_resource(sysID)
        finally:
            self.is_parsing=0

    def parseFile(self,file):
        self.reset()
        try:
            self.is_parsing=1
            self.parser.read_from(file)
            self.parser.flush()
            self.parser.parseEnd()
        finally:
            self.is_parsing=0

    def _create_parser(self):
        return xmlproc.XMLProcessor()

    def setLocale(self, locale):
        try:
            self.parser.set_error_language(locale)
        except KeyError:
            raise saxlib.SAXNotSupportedException("Locale '%s' not supported" % locale)

    # --- data event methods

    def doc_start(self):
        if self.locator:
            self.doc_handler.setDocumentLocator(self)
        self.doc_handler.startDocument()

    def doc_end(self):
        self.doc_handler.endDocument()

    def handle_data(self,data,start,end):
        self.doc_handler.characters(data,start,end-start)

    def handle_ignorable_data(self,data,start,end):
        self.doc_handler.ignorableWhitespace(data,start,end-start)

    def handle_pi(self, target, data):
        self.doc_handler.processingInstruction(target,data)

    def handle_start_tag(self, name, attrs):
        self.doc_handler.startElement(name,saxutils.AttributeMap(attrs))

    def handle_end_tag(self, name):
        self.doc_handler.endElement(name)

    # --- pubid resolution

    def resolve_entity_pubid(self,pubid,sysid):
        return self.ent_handler.resolveEntity(pubid,sysid)

    def resolve_doctype_pubid(self,pubid,sysid):
        return self.ent_handler.resolveEntity(pubid,sysid)

    # --- error handling

    def warning(self,msg):
        self.err_handler.warning(saxlib.SAXParseException(msg,None,self))

    def error(self,msg):
        self.err_handler.error(saxlib.SAXParseException(msg,None,self))

    def fatal(self,msg):
        self.err_handler.fatalError(saxlib.SAXParseException(msg,None,self))

    # --- location handling

    def getColumnNumber(self):
        return self.parser.get_column()

    def getLineNumber(self):
        return self.parser.get_line()

    def getSystemId(self):
        return self.parser.get_current_sysid()

    # --- DTD parsing

    def new_external_entity(self,name,pubid,sysid,ndata):
        if ndata!="":
            self.dtd_handler.unparsedEntityDecl(name,pubid,sysid,ndata)

    def new_notation(self,name,pubid,sysid):
        self.dtd_handler.notationDecl(name,pubid,sysid)

    # --- entity events

    def resolve_entity(self,pubid,sysid):
        newsysid=self.ent_handler.resolveEntity(pubid,sysid)
        if newsysid==None:
            return sysid
        else:
            return newsysid

    # --- EXPERIMENTAL PYTHON SAX EXTENSIONS:

    def get_parser_name(self):
        return "xmlproc"

    def get_parser_version(self):
        return xmlproc.version

    def get_driver_version(self):
        return version

    def is_validating(self):
        return 0

    def is_dtd_reading(self):
        return 1

    def reset(self):
        if hasattr(self, "parser"):
            self.parser.deref()
        self.parser=self._create_parser()
        self.parser.set_application(self)
        self.parser.set_error_handler(self)
        self.parser.set_pubid_resolver(self)
        self.parser.set_dtd_listener(self)
        self.parser.reset()

    def feed(self,data):
        self.parser.feed(data)

    def close(self):
        self.parser.close()
        self.parser.deref()
        # Dereferencing to avoid circular references (grrrr)
        self.err_handler = self.dtd_handler = self.doc_handler = None
        self.parser = self.locator = self.ent_handler = None

# --- Global functions

def create_parser():
    return SAX_XPParser()
