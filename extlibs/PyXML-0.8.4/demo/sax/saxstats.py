# A simple SAX application that counts the number of elements, attributes and
# processing instructions in a document.

from xml.sax import saxexts
from xml.sax import saxlib
import sys

class CounterHandler(saxlib.DocumentHandler):

    def __init__(self):
        self.elems=0
        self.attrs=0
        self.pis=0

    def startElement(self,name,attrs):
        self.elems=self.elems+1
        self.attrs=self.attrs+len(attrs)

    def processingInstruction(self,target,data):
        self.pis=self.pis+1

# --- Main prog

if len(sys.argv)<2:
    print "Usage: python saxstats.py <document>"
    print
    print " <document>: file name of the document to parse"
    sys.exit(1)

# Load parser and driver

print "\nLoading parser..."

p=saxexts.make_parser()
ch=CounterHandler()
p.setDocumentHandler(ch)

# Ready, set, go!

print "Starting parse..."

OK=0
try:
    p.parse(sys.argv[1])
    OK=1
except IOError,e:
    print "\nERROR: "+sys.argv[1]+": "+str(e)
except saxlib.SAXException,e:
    print "\nERROR: "+str(e)

print "Parse complete:"
print "  Elements:    %d" % ch.elems
print "  Attributes:  %d" % ch.attrs
print "  Proc instrs: %d" % ch.pis
