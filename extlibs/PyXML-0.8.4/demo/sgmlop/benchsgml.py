# benchmark

import time

from xml.parsers import sgmlop

import sgmllib

SIZE = 16384
FILE = "test2.htm"

bytes = len(open(FILE).read())

def t1():
    fp = open(FILE)
    parser = sgmllib.SlowSGMLParser()
    while 1:
        data = fp.read(SIZE)
        if not data:
            break
        parser.feed(data)
    parser.close()
    fp.close()

def t2():
    fp = open(FILE)
    parser = sgmllib.FastSGMLParser()
    while 1:
        data = fp.read(SIZE)
        if not data:
            break
        parser.feed(data)
    parser.close()
    fp.close()

def t3():
    fp = open(FILE)
    parser = sgmlop.SGMLParser()
    while 1:
        data = fp.read(SIZE)
        if not data:
            break
        parser.feed(data)
    parser.close()
    fp.close()

class Dummy:
    def finish_starttag(self, tag, data):
        pass
    def finish_endtag(self, tag):
        pass
    def handle_entityref(self, data):
        pass
    def handle_data(self, data):
        pass

def t4():
    fp = open(FILE)
    parser = sgmlop.SGMLParser()
    parser.register(Dummy())
    while 1:
        data = fp.read(SIZE)
        if not data:
            break
        parser.feed(data)
    parser.close()
    fp.close()

t = time.time()
t1(); t1(); t1(); t1(); t1();
t1(); t1(); t1(); t1(); t1();
t = (time.time() - t) / 10
print "t1:", t
if t: print int(bytes / t), "bytes per second"

t = time.time()
t2(); t2(); t2(); t2(); t2();
t2(); t2(); t2(); t2(); t2();
t2(); t2(); t2(); t2(); t2();
t2(); t2(); t2(); t2(); t2();
t = (time.time() - t) / 20
print "t2:", t
if t: print int(bytes / t), "bytes per second"

t = time.time()
t3(); t3(); t3(); t3(); t3();
t3(); t3(); t3(); t3(); t3();
t3(); t3(); t3(); t3(); t3();
t3(); t3(); t3(); t3(); t3();
t = (time.time() - t) / 20
print "t3:", t
if t: print int(bytes / t), "bytes per second"

t = time.time()
t4(); t4(); t4(); t4(); t4();
t4(); t4(); t4(); t4(); t4();
t4(); t4(); t4(); t4(); t4();
t4(); t4(); t4(); t4(); t4();
t = (time.time() - t) / 20
print "t4:", t
if t: print int(bytes / t), "bytes per second"
