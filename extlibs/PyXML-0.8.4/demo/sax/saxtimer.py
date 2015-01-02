# A simple SAX application that measures the time spent parsing a
# document with an empty document handler.

from xml.sax import saxexts
from xml.sax import saxlib
import sys,time

if len(sys.argv)<3:
    print "Usage: python <parser> <document>"
    print
    print " <document>: file name of the document to parse"
    print " <parser>:   driver package name"
    sys.exit(1)

# Load parser and driver

print "\nLoading parser..."

try:
    p=saxexts.make_parser("xml.sax.drivers.drv_" + sys.argv[1])
except saxlib.SAXException,e:
    print "ERROR: Parser not available"
    sys.exit(1)

# Ready, set, go!

sum=0
print "Starting parse..."
for ix in range(3):
    start=time.clock()

    OK=0
    pt=0
    try:
        p.parse(sys.argv[2])
        pt=time.clock()-start
        OK=1
    except IOError,e:
        print "\nERROR: "+sys.argv[2]+": "+str(e)
    except saxlib.SAXException,e:
        print "\nERROR: "+str(e)

    if OK:
        print "Parse time: "+`pt`
    else:
        print "Error occurred, parse aborted."

    sum=sum+pt

print "Average: %f" % (sum/3.0)
