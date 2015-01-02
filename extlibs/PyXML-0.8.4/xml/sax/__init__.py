"""Simple API for XML (SAX) implementation for Python.

This module provides an implementation of the SAX 2 interface;
information about the Java version of the interface can be found at
http://www.megginson.com/SAX/.  The Python version of the interface is
documented at <...>.

This package contains the following interface classes and functions:

ContentHandler, ErrorHandler - base classes for SAX2 handlers
SAXException, SAXNotRecognizedException,
SAXParseException, SAXNotSupportedException - SAX exceptions

make_parser            - creation of a new parser object
parse, parseString     - parse a document, using a provided handler

"""

from xmlreader import InputSource
from handler import ContentHandler, ErrorHandler
from _exceptions import SAXException, SAXNotRecognizedException,\
                        SAXParseException, SAXNotSupportedException,\
                        SAXReaderNotAvailable

from sax2exts import make_parser

def parse(filename_or_stream, handler, errorHandler=ErrorHandler()):
    parser = make_parser()
    parser.setContentHandler(handler)
    parser.setErrorHandler(errorHandler)
    parser.parse(filename_or_stream)

def parseString(string, handler, errorHandler=ErrorHandler()):
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO

    if errorHandler is None:
        errorHandler = ErrorHandler()
    parser = make_parser()
    parser.setContentHandler(handler)
    parser.setErrorHandler(errorHandler)

    inpsrc = InputSource()
    inpsrc.setByteStream(StringIO(string))
    parser.parse(inpsrc)
