# Test suite containing code from the XML HOWTO

# SAX testing code

print "SAX tests:\n"

from xml.sax import saxutils, make_parser, ContentHandler
from xml.sax.handler import feature_namespaces
import StringIO
import string

comic_xml = StringIO.StringIO("""<collection>
  <comic title="Sandman" number='62'>
    <writer>Neil Gaiman</writer>
    <penciller pages='1-9,18-24'>Glyn Dillon</penciller>
    <penciller pages="10-17">Charles Vess</penciller>
  </comic>
  <comic title="Shade, the Changing Man" number="7">
    <writer>Peter Milligan</writer>
    <penciller>Chris Bachalo</penciller>
  </comic>
</collection>""")

class FindIssue(saxutils.DefaultHandler):
    def __init__(self, title, number):
        self.search_title, self.search_number = title, number

    def startElement(self, name, attrs):
        # If it's not a comic element, ignore it
        if name != 'comic': return

        # Look for the title and number attributes (see text)
        title = attrs.get('title', None)
        number = attrs.get('number', None)
        if title == self.search_title and number == self.search_number:
            print title, '#'+str(number), 'found'

    def error(self, exception):
        import sys
        sys.stderr.write("%s\n" % exception)

if 1:
    # Create a parser
    parser = make_parser()
    # Disable namespace processing
    parser.setFeature(feature_namespaces, 0)

    # Create the handler
    dh = FindIssue('Sandman', '62')

    # Tell the parser to use our handler
    parser.setContentHandler(dh)
    parser.setErrorHandler(dh)

    # Parse the input
    parser.parse(comic_xml)


def normalize_whitespace(text):
    "Remove redundant whitespace from a string"
    return string.join(string.split(text), ' ')

class FindWriter(ContentHandler):
    def __init__(self, search_name):
        # Save the name we're looking for
        self.search_name = normalize_whitespace(search_name)

        # Initialize the flag to false
        self.inWriterContent = 0

    def startElement(self, name, attrs):
        # If it's a comic element, save the title and issue
        if name == 'comic':
            title = normalize_whitespace(attrs.get('title', ""))
            number = normalize_whitespace(attrs.get('number', ""))
            self.this_title = title
            self.this_number = number

        # If it's the start of a writer element, set flag
        elif name == 'writer':
            self.inWriterContent = 1
            self.writerName = ""

    def characters(self, ch):
        if self.inWriterContent:
            self.writerName = self.writerName + ch

    def endElement(self, name):
        if name == 'writer':
            self.inWriterContent = 0
            self.writerName = normalize_whitespace(self.writerName)
            if self.writerName == self.search_name:
                print self.this_title, self.this_number

if 1:
    # Create a parser
    parser = make_parser()

    # Disable namespace processing
    parser.setFeature(feature_namespaces, 0)

    # Create the handler
    dh = FindWriter('Peter Milligan')

    # Tell the parser to use our handler
    parser.setContentHandler(dh)

    # Print a title
    print '\nTitles by Peter Milligan:'

    # Parse the input
    comic_xml.seek(0)
    parser.parse(comic_xml)


# DOM tests

print "DOM tests:\n"

import sys
from xml.dom.ext.reader import Sax2
from xml.dom.ext import PrettyPrint

dom_xml = """<?xml version="1.0" encoding="iso-8859-1"?>
<xbel>
  <?processing instruction?>
  <desc>No description</desc>
  <folder>
    <title>XML bookmarks</title>
    <bookmark href="http://www.python.org/sigs/xml-sig/" >
      <title>SIG for XML Processing in Python</title>
    </bookmark>
  </folder>
</xbel>"""

# Parse the input into a DOM tree
reader = Sax2.Reader()
doc = reader.fromStream( StringIO.StringIO(dom_xml) )

# Print it
# for testing, we must explicitly pass sys.stdout, as regrtest will
# bind this to a different object
PrettyPrint(doc, sys.stdout)

# whitespace-removal currently not supported
# utils.strip_whitespace(doc)
# print ' With whitespace removed:'
# print doc.toxml()

# Builder code

print 'DOM creation tests'

from xml.dom.DOMImplementation import implementation
d = implementation.createDocument(None, None, None)

# Create the root element
r = d.createElement("html")
d.appendChild(r)

# Create an empty 'head' element
r.appendChild(d.createElement("head"))

# Start the 'body' element, giving it an attribute
b = d.createElement("body")
b.setAttribute('background','#ffffff')
r.appendChild(b)

# Add a text node
b.appendChild(d.createTextNode("The body text goes here."))

# Print the document
PrettyPrint(d, sys.stdout)
