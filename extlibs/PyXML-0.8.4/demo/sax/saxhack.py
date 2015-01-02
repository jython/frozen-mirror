#
#
# $Id: saxhack.py,v 1.5 2001/12/30 12:17:32 loewis Exp $
#
# illustrate how a saxlib parser can interface directly to sgmlop
#
# history:
# 98-05-23 fl   created (derived from the coreXML parser)
#
# Copyright (c) 1998 by Secret Labs AB
#
# info@pythonware.com
# http://www.pythonware.com
#

from xml.sax.saxlib import HandlerBase
class DocumentHandler:#(HandlerBase):

    # SAX interface

    def startElement(self, tag, attrs):
        pass # print "start", tag

    def endElement(self, tag):
        pass # print "end", tag

    def characters(self, text, start, len):
        pass # print "data", text[start:start+len]

# --------------------------------------------------------------------
# sgmlop-based parser

from xml.parsers import sgmlop

class Parser:

    def setDocumentHandler(self, dh):

        self.parser = sgmlop.XMLParser()
        self.parser.register(dh, 1)

    def parseFile(self, file):

        parser = self.parser

        while 1:
            data = file.read(16384)
            if not data:
                break
            parser.feed(data)

        parser.close()

# --------------------------------------------------------------------
# xmllib-based parser

from xml.parsers import xmllib

class xmllibParser(xmllib.XMLParser):

    def setDocumentHandler(self, dh):

        self.characters = dh.characters
        self.unknown_starttag = dh.startElement
        self.unknown_endtag = dh.endElement

    def handle_data(self, data):
        self.characters(data, 0, len(data))

    def parseFile(self, file):

        while 1:
            data = file.read(16384)
            if not data:
                break
            self.feed(data)

        self.close()

# --------------------------------------------------------------------
# original xmllib-based parser

class slowParser(xmllib.SlowXMLParser):

    def setDocumentHandler(self, dh):

        self.characters = dh.characters
        self.unknown_starttag = dh.startElement
        self.unknown_endtag = dh.endElement

    def handle_data(self, data):
        self.characters(data, 0, len(data))

    def parseFile(self, file):

        while 1:
            data = file.read(16384)
            if not data:
                break
            self.feed(data)

        file.close()

# ====================================================================
# test stuff

import time, os, sys

if len(sys.argv) == 1:
    print 'Usage: saxhack.py <xml filename>'
    sys.exit(1)

FILE = sys.argv[1]

size = os.stat(FILE)[6]

p  = Parser()
dh = DocumentHandler()
p.setDocumentHandler(dh)

f = open(FILE)
t = time.clock()
p.parseFile(f) # dry run
t_direct = time.clock() - t
f.close()

#import sys ; sys.exit(0)

print t_direct
if t_direct == 0:
    print 'Measured time was too small; use a larger XML file'
    sys.exit(1)

print "sgmlop:", int(size / t_direct), "bytes per second"

p = xmllibParser()
#p=slowParser()
dh = DocumentHandler()
p.setDocumentHandler(dh)

f = open(FILE)
t = time.clock()
p.parseFile(f) # dry run
t_fast = time.clock() - t
f.close()

print "xmllib:", int(size / t_fast), "bytes per second"

p = slowParser()
dh = DocumentHandler()
p.setDocumentHandler(dh)

f = open(FILE)
t = time.clock()
p.parseFile(f) # dry run
t_slow = time.clock() - t
f.close()

print "slow xmllib:", int(size / t_slow), "bytes per second"

print
print "normalized timings:"
print "slow xmllib", 1.0
print "fast xmllib", round(t_fast / t_slow, 2), "(%sx)" % round(t_slow / t_fast, 1)
print "sgmlop     ", round(t_direct / t_slow, 2), "(%sx)" % round(t_slow / t_direct, 1)
print
