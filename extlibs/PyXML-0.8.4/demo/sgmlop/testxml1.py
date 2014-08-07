# basic tests

import sys
import time, string
from xml.parsers import sgmlop

try:
    from xml.parsers import xmllib
    have_xmllib = 1
except ImportError:
    have_xmllib = 0
    class xmllib:
        class FastXMLParser:pass
        class SlowXMLParser:pass

try:
    FILE, VERBOSE = sys.argv[1], 2
except IndexError:
    FILE, VERBOSE = "hamlet.xml", 1

print
print "test collecting parsers on", FILE
print

# --------------------------------------------------------------------
# sgmlop

class myCollector:
    def __init__(self):
        self.data = []
        self.text = []
    def finish_starttag(self, tag, data):
        if self.text:
            self.data.append(repr(string.join(self.text, "")))
            self.text = []
        self.data.append(("start", tag, data))
    def handle_proc(self, tag, data):
        if self.text:
            self.data.append(repr(string.join(self.text, "")))
            self.text = []
        self.data.append(("pi", tag, data))
    def handle_special(self, data):
        if self.text:
            self.data.append(repr(string.join(self.text, "")))
            self.text = []
        self.data.append(("special", data))
    def handle_entityref(self, data):
        if self.text:
            self.data.append(repr(string.join(self.text, "")))
            self.text = []
        self.data.append(("entity", data))
    def handle_data(self, data):
        self.text.append(data)
    def handle_cdata(self, data):
        self.text.append("CDATA" + data)

t = time.clock()
for i in range(1000):
    out = myCollector()
    fp = open(FILE)
    parser = sgmlop.XMLUnicodeParser()
    parser.register(out)
    b = 0
    while 1:
        data = fp.read(1024)
        if not data:
            break
        parser.feed(data)
        b = b + len(data)
    parser.close()
t1 = time.clock() - t

print "raw sgmlop:", len(out.data), "items;", round(t1, 3), "seconds;",
print round(b / t1 / 1024, 2), "kbytes per second"
print out.data

# --------------------------------------------------------------------
# xmllib

class FastXMLParser(xmllib.FastXMLParser):
    def __init__(self):
        xmllib.FastXMLParser.__init__(self)
        self.data = []
        self.text = []
    def unknown_starttag(self, tag, data):
        if self.text:
            self.data.append(repr(string.join(self.text, "")))
            self.text = []
        self.data.append("start", tag, data)
    def handle_proc(self, tag, data):
        if self.text:
            self.data.append(repr(string.join(self.text, "")))
            self.text = []
        self.data.append("pi", tag, data)
    def handle_special(self, data):
        if self.text:
            self.data.append(repr(string.join(self.text, "")))
            self.text = []
        self.data.append("special", data)
    def handle_entityref(self, data):
        if self.text:
            self.data.append(repr(string.join(self.text, "")))
            self.text = []
        self.data.append("entity", data)
    def handle_data(self, data):
        self.text.append(data)
    def handle_cdata(self, data):
        self.text.append("CDATA" + data)

if have_xmllib:
    t = time.clock()
    for i in range(1):
        fp = open(FILE)
        parser2 = FastXMLParser()
        b = 0
        while 1:
            data = fp.read(1024)
            if not data:
                break
            parser2.feed(data)
            b = b + len(data)
        parser2.close()
    t2 = time.clock() - t

    print "fast xmllib:", len(parser2.data), "items;", round(t2, 3), "seconds;",
    print round(b / t2 / 1024, 2), "kbytes per second"

class SlowXMLParser(xmllib.SlowXMLParser):
    def __init__(self):
        xmllib.SlowXMLParser.__init__(self)
        self.data = []
        self.text = []
    def unknown_starttag(self, tag, data):
        if self.text:
            self.data.append(repr(string.join(self.text, "")))
            self.text = []
        self.data.append("start", tag, data)
    def handle_proc(self, tag, data):
        if self.text:
            self.data.append(repr(string.join(self.text, "")))
            self.text = []
        self.data.append("pi", tag, data)
    def handle_special(self, data):
        if self.text:
            self.data.append(repr(string.join(self.text, "")))
            self.text = []
        self.data.append("special", data)
    def handle_entityref(self, data):
        if self.text:
            self.data.append(repr(string.join(self.text, "")))
            self.text = []
        self.data.append("entity", data)
    def handle_data(self, data):
        self.text.append(data)
    def handle_cdata(self, data):
        self.text.append("CDATA" + data)

if have_xmllib:
    t = time.clock()
    for i in range(1):
        fp = open(FILE)
        parser3 = SlowXMLParser()
        b = 0
        while 1:
            data = fp.read(1024)
            if not data:
                break
            parser3.feed(data)
            b = b + len(data)
        parser3.close()
    t3 = time.clock() - t

    print "slow xmllib:", len(parser3.data), "items;", round(t3, 3), "seconds;",
    print round(b / t3 / 1024, 2), "kbytes per second"

    print
    print "normalized timing:"
    print "slow xmllib", 1.0
    print "fast xmllib", round(t2 / t3, 2), "(%sx)" % round(t3 / t2, 1)
    print "sgmlop     ", round(t1 / t3, 2), "(%sx)" % round(t3 / t1, 1)
    print

    print "looking for differences:"

    items = min(len(parser2.data), len(parser3.data))

    for i in xrange(items):
        if parser2.data[i] != parser3.data[i]:
            for j in range(max(i-5, 0), min(i+5, items)):
                if parser2.data[j] != parser3.data[j]:
                    print "+", j+1, parser2.data[j]
                    print "*", j+1, parser3.data[j]
                else:
                    print "=", j+1, parser2.data[j]
            break
    else:
        print "   (none found)"
