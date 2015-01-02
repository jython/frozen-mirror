# dry runs

from xml.parsers import xmllib, sgmlop
import sys
import time, string

try:
    FILE, VERBOSE = sys.argv[1], 2
except IndexError:
    FILE, VERBOSE = "hamlet.xml", 1

BLOCK = 16384

print
print "test empty parsers on", FILE
print

t = time.clock()
b = 0
for i in range(1):
    fp = open(FILE)
    parser = sgmlop.XMLParser()
    while 1:
        data = fp.read(BLOCK)
        if not data:
            break
        parser.feed(data)
        b = b + len(data)
    parser.close()
t1 = time.clock() - t

print "sgmlop", round(t1, 3), "seconds;",
print round(b / t1 / 1024, 2), "kbytes per second"

t = time.clock()
b = 0
for i in range(1):
    fp = open(FILE)
    parser = xmllib.FastXMLParser()
    while 1:
        data = fp.read(BLOCK)
        if not data:
            break
        parser.feed(data)
        b = b + len(data)
    parser.close()
t2 = time.clock() - t

print "fast xmllib", round(t2, 3), "seconds;",
print round(b / t2 / 1024, 2), "kbytes per second"

t = time.clock()
b = 0
for i in range(1):
    fp = open(FILE)
    parser = xmllib.SlowXMLParser()
    while 1:
        data = fp.read(BLOCK)
        if not data:
            break
        parser.feed(data)
        b = b + len(data)
    parser.close()
t3 = time.clock() - t

print "slow xmllib", round(t3, 3), "seconds;",
print round(b / t3 / 1024, 2), "kbytes per second"

print
print "sgmlop is", round(t3 / t1, 2), "times faster than slow xmllib"
