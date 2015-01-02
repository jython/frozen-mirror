# -*- coding: iso-8859-1 -*-
"""
SAX driver for the Pyexpat C module.

$Id: drv_pyexpat.py,v 1.19 2004/11/29 13:38:23 loewis Exp $
"""

# Event handling can be speeded up by bypassing the driver for some events.
# This will be implemented later when I can test this driver.
#
# This driver has been much improved by Geir Ove Grønmo.

version="0.13"

from xml.sax import saxlib, saxutils, SAXReaderNotAvailable

try:
    from xml.parsers import expat
except ImportError:
    raise SAXReaderNotAvailable("expat not supported",None)

import urllib2,types

# --- SAX_expat

class SAX_expat(saxlib.Parser,saxlib.Locator):
    "SAX driver for the Pyexpat C module."

    def __init__(self):
        saxlib.Parser.__init__(self)
        self.reset()

    def startElement(self,name,attrs):
        at = {}
        # Backward compatibility code, for older versions of the
        # PyExpat module
        if type(attrs) == type({}):
            at = attrs
        else:
            # Assume it's a list containing alternating names & values
            at = {}
            for i in range(0, len(attrs), 2):
                at[attrs[i]] = attrs[i+1]

        self.doc_handler.startElement(name,saxutils.AttributeMap(at))

    # FIXME: bypass!
    def endElement(self,name):
        self.doc_handler.endElement(name)

    def characters(self,data):
        self.doc_handler.characters(data,0,len(data))

    # FIXME: bypass!
    def processingInstruction(self,target,data):
        self.doc_handler.processingInstruction(target,data)

    def parse(self,sysID):
        self.parseFile(urllib2.urlopen(sysID),sysID)

    def parseFile(self,fileobj,sysID=None):
        self.reset()
        self.sysID=sysID
        self.doc_handler.startDocument()

        buf = fileobj.read(16384)
        while buf != "":
            if self.parser.Parse(buf, 0) != 1:
                self.__report_error()
            buf = fileobj.read(16384)
        self.parser.Parse("", 1)

        self.doc_handler.endDocument()
        self.close(needFinal=0)

    # --- Locator methods. Only usable after errors.

    def getSystemId(self):
        if self.sysID!=None:
            return self.sysID
        else:
            return "Unknown"

    def getLineNumber(self):
        return self.parser.ErrorLineNumber

    def getColumnNumber(self):
        return self.parser.ErrorColumnNumber

    # --- Internal

    def __report_error(self):
        errc=self.parser.ErrorCode
        msg=expat.ErrorString(errc)
        exc=saxlib.SAXParseException(msg,None,self)
        self.err_handler.fatalError(exc)

    # --- EXPERIMENTAL PYTHON SAX EXTENSIONS

    def get_parser_name(self):
        return "pyexpat"

    def get_parser_version(self):
        return "Unknown"

    def get_driver_version(self):
        return version

    def is_validating(self):
        return 0

    def is_dtd_reading(self):
        return 0

    def reset(self):
        self.sysID=None
        self.parser=expat.ParserCreate()
        self.parser.StartElementHandler = self.startElement
        self.parser.EndElementHandler = self.endElement
        self.parser.CharacterDataHandler = self.characters
        self.parser.ProcessingInstructionHandler = self.processingInstruction
        self.doc_handler.setDocumentLocator(self)

    def feed(self, data):
        if self.parser.Parse(data, 0) != 1:
            self.__report_error()

    def close(self, needFinal=1):
        if self.parser is None:
            # make sure close is idempotent
            return
        if needFinal:
            if self.parser.Parse("", 1) != 1:
                self.__report_error()
        self.parser = None

# --- An expat driver that uses the lazy map

class LazyExpatDriver(SAX_expat):

    def __init__(self):
        SAX_expat.__init__(self)
        self.map=LazyAttributeMap([])

    def startElement(self,name,attrs):
        self.map.list=attrs
        self.doc_handler.startElement(name,self.map)

# --- A lazy attribute map

# This avoids the costly conversion from a list to a hash table

class LazyAttributeMap:
    """A lazy implementation of AttributeList that takes an
    [attr,val,attr,val,...] list and uses it to implement the AttributeList
    interface."""

    def __init__(self, list):
        self.list=list

    def getLength(self):
        return len(self.list)/2

    def getName(self, i):
        try:
            return self.list[2*i]
        except IndexError,e:
            return None

    def getType(self, i):
        return "CDATA"

    def getValue(self, i):
        try:
            if type(i)==types.IntType:
                return self.list[2*i+1]
            else:
                for ix in range(0,len(self.list),2):
                    if self.list[ix]==i:
                        return self.list[ix+1]

                return None
        except IndexError,e:
            return None

    def __len__(self):
        return len(self.list)/2

    def __getitem__(self, key):
        if type(key)==types.IntType:
            return self.list[2*key+1]
        else:
            for ix in range(0,len(self.list),2):
                if self.list[ix]==key:
                    return self.list[ix+1]

            return None

    def items(self):
        result=[""]*(len(self.list)/2)
        for ix in range(0,len(self.list),2):
            result[ix/2]=(self.list[ix],self.list[ix+1])
        return result

    def keys(self):
        result=[""]*(len(self.list)/2)
        for ix in range(0,len(self.list),2):
            result[ix/2]=self.list[ix]
        return result

    def has_key(self,key):
        for ix in range(0,len(self.list),2):
            if self.list[ix]==key:
                return 1

        return 0

    def get(self, key, alternative):
        for ix in range(0,len(self.list),2):
            if self.list[ix]==key:
                return self.list[ix+1]

        return alternative

# ---

def create_parser():
    return SAX_expat()
