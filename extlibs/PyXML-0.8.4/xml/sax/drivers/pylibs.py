"""
Common code for the sgmllib, htmllib and xmllib parser drivers.

$Id: pylibs.py,v 1.6 2002/08/13 09:28:52 afayolle Exp $
"""

from xml.sax import saxlib,saxutils

import urllib2

# --- LibParser

class LibParser(saxlib.Parser,saxlib.Locator):
    "Common code for the sgmllib, htmllib and xmllib parser drivers."

    def __init__(self):
        saxlib.Parser.__init__(self)

    def parse(self,sysID):
        "Parses the referenced document."
        self.sysID=sysID
        self.parseFile(urllib2.urlopen(sysID))

    def parseFile(self,fileobj):
        "Parses the given file."
        if self._can_locate():
            self.doc_handler.setDocumentLocator(self)
        self.reset()
        while 1:
            buf=fileobj.read(16384)
            if buf=="": break

            try:
                self.feed(buf)
            except RuntimeError,e:
                self.err_handler.fatalError(saxlib.SAXException(str(e),e))

        self.close()

    def unknown_endtag(self,tag):
        "Handles end tags."
        self.doc_handler.endElement(tag)

    def handle_xml(self,encoding,standalone):
        "Remembers whether the document is standalone."
        self.standalone= standalone=="yes"

    def handle_data(self,data):
        "Handles PCDATA."
        self.doc_handler.characters(data,0,len(data))

    def handle_cdata(self,data):
        "Handles CDATA marked sections."
        self.doc_handler.characters(data,0,len(data))

    def syntax_error(self, message):
        "Handles fatal errors."
        if self._can_locate():
            self.err_handler.fatalError(saxlib.SAXParseException(message,None,
                                                                 self))
        else:
            self.err_handler.fatalError(saxlib.SAXException(message,None))


# --- SGMLParsers

class SGMLParsers(LibParser):
    "Common code for the sgmllib and htmllib parsers."

    def handle_pi(self,data):
        "Handles processing instructions."
        # Should we try to parse out the name if there is one?
        self.doc_handler.processingInstruction("",data)

    def handle_starttag(self,tag,method,attributes):
        self.unknown_starttag(tag,attributes)

    def unknown_starttag(self,tag,attributes):
        "Handles start tags."
        attrs={}
        for (a,v) in attributes:
            attrs[a]=v

        self.doc_handler.startElement(tag,saxutils.AttributeMap(attrs))

    def handle_endtag(self,tag,method):
        "Handles end tags."
        self.doc_handler.endElement(tag)

    def unknown_entityref(self,name):
        "Handles entity references by throwing an error."
        self.err_handler.fatalError(saxlib.SAXException("Reference to unknown entity "
                                                 "'%s'" % name,None))

    def unknown_charref(self,no):
        "Handles non-ASCII character references."
        self.err_handler.fatalError(saxlib.SAXException("Reference to unknown character '%d'" % no,None))

    def handle_data(self,data):
        "Handles character data in element content."
        self.doc_handler.characters(data,0,len(data))

    def report_unbalanced(self,gi):
        "Reports unbalanced tags."
        self.err_handler.fatalError(saxlib.SAXException("Unbalanced end tag for '%s'" % gi,None))

    def _can_locate(self):
        "Internal: returns true if location info is available."
        return 0
