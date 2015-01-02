#!/usr/bin/env python

"""
Small utility that parses Netscape bookmarks.
"""

# TODO:
# LAST_CHARSET: put in <info><metadata owner="mozilla"><last_charset>...</info>
# H3:LAST_MODIFIED: Put in XBEL 1.2?
# Cross references?
# Descriptions


from xml.sax import sax2exts,handler
import bookmark
import string, htmlentitydefs

# --- SAX handler for Netscape bookmarks

class NetscapeHandler(handler.ContentHandler):

    def __init__(self):
        self.bms=bookmark.Bookmarks()
        self.cur_elem = None
        self.added    = None
        self.href     = None
        self.visited  = None
        self.modified = None
        self.latest   = None
        self.desc = ""

    def startElement(self,name,attrs):
        name = string.lower( name )
        d = {}
        for key, value in attrs.items():
            d[ string.lower(key) ] = value
##        print 'start', name, d
        if name=="h3":
            self.cur_elem="h3"
            if d.has_key("folded"):
                self.folded = "yes"
            else:
                self.folded = "no"
            self.id = d.get('id')
            self.added= d.get('add_date',"")
            self.modified = d.get('last_modified', "")
            folder = self.bms.add_folder('', None)
            folder.id = self.id
            folder.folded = self.folded
            folder.added = self.added
            self.latest = folder
        elif name=="a":
            self.cur_elem="a"
            self.bookmark = ""
            if d.has_key('add_date'): self.added=d["add_date"]
            else: self.added = None
            if d.has_key('last_visit'): self.visited=d["last_visit"]
            else: self.visited = None
            if d.has_key('last_modified'): self.modified=d["last_modified"]
            else: self.modified = None

            self.url=d["href"]
        elif name=='title':
            self.cur_elem = 'title'
            self.bms.title = ""
        elif name=='h1':
            self.cur_elem = 'h1'
            self.bms.desc = ""
        elif name=='hr':
            self.bms.add_separator()
        elif name=='meta':
            if d.has_key('http-equiv') and \
               string.lower(d['http-equiv'])=='content-type':
                value = string.split(d['content'], "charset=")
                if len(value) == 2:
                    the_parser.setProperty(handler.property_encoding, value[1])
        elif name in ('dt','dl'):
            if self.desc and not self.latest.desc:
                self.latest.desc = self.desc
            self.desc = ""
            self.curr_elem = ''
        elif name=='dd':
            self.cur_elem = 'dd'
            self.desc = ""


    def characters(self,data):
##        print 'char', self.cur_elem, data
        if self.cur_elem=="h3":
            self.latest.title+=data
        elif self.cur_elem=="a":
            self.bookmark = self.bookmark+data
        elif self.cur_elem=="title":
            self.bms.title = self.bms.title + data
        elif self.cur_elem=="h1":
            self.bms.desc = self.bms.desc + data
        elif self.cur_elem=="dd":
            self.desc = self.desc + data

    def skippedEntity(self, name):
        self.characters(htmlentitydefs.entitydefs[name])

    def endElement(self,name):
        name = string.lower( name )
##        print 'end', name
        if name=="a":
            self.latest = self.bms.add_bookmark(self.bookmark,
                                                added = self.added,
                                                visited = self.visited,
                                                modified = self.modified,
                                                href = self.url)
        elif name=="h3":
            self.cur_elem=None
        elif name=="dl":
            self.bms.leave_folder()
        elif name == self.cur_elem:
            self.cur_elem=None
            
    def endDocument(self):
        if self.desc and not self.latest.desc:
            self.latest.desc = self.desc
        
# --- Test-program

if __name__ == '__main__':
    import sys

    if len(sys.argv)<2 or len(sys.argv)>3:
        print
        print "A simple utility to convert Netscape bookmarks to XBEL."
        print
        print "Usage: "
        print "  ns_parse.py <ns-file> [<xbel-file>]"
        sys.exit(1)

    ns_handler=NetscapeHandler()
    the_parser = sax2exts.SGMLParserFactory.make_parser()
    the_parser.setContentHandler(ns_handler)
    # For Netscape 4, default to Latin-1
    the_parser.setProperty(handler.property_encoding, "iso-8859-1")
    file = open(sys.argv[1], 'r')
    the_parser.parse(file)
    bms = ns_handler.bms

    if len(sys.argv)==3:
        out=open(sys.argv[2],"w")
        bms.dump_xbel(out)
        out.close()
    else:
        bms.dump_xbel()

    # Done

##     ns_handler=NetscapeHandler()

##     p=saxexts.SGMLParserFactory.make_parser()
##     p.setDocumentHandler(ns_handler)
##     p.parseFile(open(r"/home/amk/.netscape/bookmarks.html"))
##     ns_handler.bms.dump_xbel()
