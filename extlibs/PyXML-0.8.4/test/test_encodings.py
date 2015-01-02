#!/usr/bin/env python

"""
This will show russian text in koi8-r encoding.
"""

from xml.parsers import expat
import string

# Produces ImportError in 1.5, since this test can't possibly pass there
import codecs

class XMLTree:
    def __init__(self):
        pass

    # Define a handler for start element events
    def StartElement(self, name, attrs ):
        #name = name.encode()
        print "<", repr(name), ">"
        print "attr name:", attrs.get("name",unicode("")).encode("koi8-r")
        print "attr value:", attrs.get("value",unicode("")).encode("koi8-r")

    def EndElement(self,  name ):
        print "</", repr(name), ">"

    def CharacterData(self, data ):
        if string.strip(data):
            data = data.encode("koi8-r")
            print data


    def LoadTree(self, filename):
        # Create a parser
        Parser = expat.ParserCreate()

        # Tell the parser what the start element handler is
        Parser.StartElementHandler = self.StartElement
        Parser.EndElementHandler = self.EndElement
        Parser.CharacterDataHandler = self.CharacterData

        # Parse the XML File
        ParserStatus = Parser.Parse(open(filename,'r').read(), 1)


def runTest():
    win = XMLTree()
    win.LoadTree("enc_test.xml")
    return win

runTest()
