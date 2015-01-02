"""
SAX2 driver for the sgmlop parser.

$Id: drv_sgmlop.py,v 1.7 2003/01/21 12:42:28 loewis Exp $
"""

version = "0.1"

from xml.parsers.sgmllib import SGMLParser
from xml.sax import saxlib, handler
from xml.sax.xmlreader import AttributesImpl, XMLReader
from xml.sax.saxutils import ContentGenerator, prepare_input_source

try:
    import codecs
    def to_xml_string(str,encoding):
        try:
            decoder = codecs.lookup(encoding)[1]
            return decoder(str)[0]
        except LookupError:
            return str
except ImportError:
    from xml.unicode.iso8859 import wstring
    def to_xml_string(str,encoding):
        if string.lower(self._encoding) == 'utf-8':
            return str
        else:
            return wstring.decode(encoding,str).utf8()



class SaxParser(SGMLParser, XMLReader):
    """ Implements IncrementalReader """

    def __init__(self, bufsize = 65536, encoding = 'UTF-8'):
        XMLReader.__init__(self)
        SGMLParser.__init__(self)
        self._bufsize = bufsize
        self._lexical_handler = None
        self._encoding = encoding
        self.documentStarted = 0

    def parse(self, source):
        source = prepare_input_source(source)

        self.prepareParser(source)
        file = source.getByteStream()
        buffer = file.read(self._bufsize)
        while buffer != "":
            self.feed(buffer)
            buffer = file.read(self._bufsize)
        self.close()

    def feed(self,buffer):
        if not self.documentStarted:
            self._cont_handler.startDocument()
            self.documentStarted = 1
        SGMLParser.feed(self,buffer)

    def prepareParser(self, source):
        # not used
        pass

    def close(self):
        """This method is called when the entire XML document has been
        passed to the parser through the feed method, to notify the
        parser that there are no more data. This allows the parser to
        do the final checks on the document and empty the internal
        data buffer.

        The parser will not be ready to parse another document until
        the reset method has been called.

        close may raise SAXException."""
        SGMLParser.close(self)
        self._cont_handler.endDocument()

    def _make_attr_dict(self,attr_list):
        d = {}
        cvrt = lambda str,e=self._encoding:to_xml_string(str,e)
        for (a,b) in attr_list:
            d[cvrt(a)]=cvrt(b)
        return d

    def unknown_starttag(self,tag,attrs):
        self._cont_handler.startElement(to_xml_string(tag,self._encoding),
                                        AttributesImpl(self._make_attr_dict(attrs)))

    def unknown_endtag(self,tag):
        self._cont_handler.endElement(to_xml_string(tag,self._encoding))

    def handle_data(self,data):
        self._cont_handler.characters(to_xml_string(data,self._encoding))

    def unknown_entityref(self, entity):
        self._cont_handler.skippedEntity(to_xml_string(entity,self._encoding))

    def handle_comment(self,data):
        if self._lexical_handler is not None:
            self._lexical_handler.comment(to_xml_string(data,self._encoding))

    def setProperty(self,name,value):
        if name == handler.property_lexical_handler:
            self._lexical_handler = value
        elif name == handler.property_encoding:
            self._encoding = value
        else:
            raise SAXNotRecognizedException("Property '%s' not recognized" % name)
    def getProperty(self, name):
        if name == handler.property_lexical_handler:
            return self._lexical_handler
        elif name == handler.property_encoding:
            return self._encoding
        raise SAXNotRecognizedException("Property '%s' not recognized" % name)

##    def getFeature(self, name):
##        if name == handler.feature_namespaces:
##            return self._namespaces
##        raise SAXNotRecognizedException("Feature '%s' not recognized" % name)

##    def setFeature(self, name, state):
##        if self._parsing:
##            raise SAXNotSupportedException("Cannot set features while parsing")
##        if name == handler.feature_namespaces:
##            self._namespaces = state
##        else:
##            raise SAXNotRecognizedException("Feature '%s' not recognized" %
##                                            name)

def create_parser():
    return SaxParser()
