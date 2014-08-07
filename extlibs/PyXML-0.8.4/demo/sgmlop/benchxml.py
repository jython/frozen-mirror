# benchmark

import time, sys, os
from xml.parsers import xmllib, sgmlop

SIZE = 16384
FILE = "hamlet.xml"

try:
    FILE = sys.argv[1]
except IndexError:
    pass

print "---", FILE, "---"

bytes = os.stat(FILE)[6]

# --------------------------------------------------------------------
# 1) sgmlop with null parser (no registered callbacks)

def test1():
    fp = open(FILE)
    parser = sgmlop.XMLParser()
    while 1:
        data = fp.read(SIZE)
        if not data:
            break
        parser.feed(data)
    parser.close()
    fp.close()

# --------------------------------------------------------------------
# 2) sgmlop with dummy parser

class sgmlopDummy:
    def finish_starttag(self, tag, data):
        pass
    def finish_endtag(self, tag):
        pass
    def handle_entityref(self, data):
        pass
    def handle_data(self, data):
        pass
    def handle_proc(self, name, data):
        pass
    def handle_cdata(self, data):
        pass
    def handle_charref(self, data):
        pass
    def handle_comment(self, data):
        pass
    def handle_special(self, data):
        pass

def test2():
    fp = open(FILE)
    out = sgmlopDummy()
    parser = sgmlop.XMLParser()
    parser.register(out)
    while 1:
        data = fp.read(SIZE)
        if not data:
            break
        parser.feed(data)
    parser.close()
    fp.close()

# --------------------------------------------------------------------
# 3) accelerated xmllib

class FastXMLParser(xmllib.FastXMLParser):
    def unknown_starttag(self, tag, data):
        pass
    def unknown_endtag(self, tag):
        pass
    def handle_entityref(self, data):
        pass
    def handle_data(self, data):
        pass
    def handle_cdata(self, data):
        pass

def test3():
    fp = open(FILE)
    parser = FastXMLParser()
    while 1:
        data = fp.read(SIZE)
        if not data:
            break
        parser.feed(data)
    parser.close()
    fp.close()

# --------------------------------------------------------------------
# 4) old xmllib

class SlowXMLParser(xmllib.SlowXMLParser):
    def unknown_starttag(self, tag, data):
        pass
    def unknown_endtag(self, tag):
        pass
    def handle_entityref(self, data):
        pass
    def handle_data(self, data):
        pass
    def handle_cdata(self, data):
        pass

def test4():
    fp = open(FILE)
    parser = SlowXMLParser()
    while 1:
        data = fp.read(SIZE)
        if not data:
            break
        parser.feed(data)
    parser.close()
    fp.close()

# --------------------------------------------------------------------
# 5) xmltok parser

try:
    import xmltok
except (ImportError, SystemError):
    xmltok = None

class xmltokDummy:
    def do_tag(self, tag, data):
        pass
    def do_endtag(self, tag):
        pass
    def do_entity(self, tag, data):
        pass
    def do_data(self, data):
        pass

def test5():
    fp = open(FILE)
    out = xmltokDummy()
    parser = xmltok.ParserCreate()
    parser.StartElementHandler = out.do_tag
    parser.EndElementHandler = out.do_endtag
    parser.CharacterDataHandler = out.do_data
    parser.ProcessingInstructionHandler = out.do_entity
    while 1:
        data = fp.read(SIZE)
        if not data:
            break
        parser.Parse(data)
    parser.Parse("", 1)
    fp.close()


# ====================================================================
# main

test = test1
t = time.clock()
test(); test(); test(); test(); test();
t = (time.clock() - t) / 5
print "sgmlop/null parser:", round(t, 3), "seconds;",
print int(bytes / t), "bytes per second"
time1 = t

test = test2
t = time.clock()
test(); test(); test(); test(); test();
t = (time.clock() - t) / 5
print "sgmlop/dummy parser:", round(t, 3), "seconds;",
print int(bytes / t), "bytes per second"
time2 = t

test = test3
t = time.clock()
test(); test();
t = (time.clock() - t) / 2
print "xmllib/fast parser:", round(t, 3), "seconds;",
print int(bytes / t), "bytes per second"
time3 = t

test = test4
t = time.clock()
test();
t = (time.clock() - t) / 1
print "xmllib/slow parser:", round(t, 3), "seconds;",
print int(bytes / t), "bytes per second"
time4 = t

print
print "normalized timings:"
print "slow xmllib ", 1.0
print "fast xmllib ", round(time3/time4, 3), "(%sx)" % round(time4/time3, 1)
print "sgmlop dummy", round(time2/time4, 3), "(%sx)" % round(time4/time2, 1)
print "sgmlop null ", round(time1/time4, 3), "(%sx)" % round(time4/time1, 1)
print
