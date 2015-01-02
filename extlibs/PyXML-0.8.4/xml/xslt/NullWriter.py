########################################################################
#
# File Name:            NullWriter.py
#
#
"""
Implements an empty writer for XSLT processor output
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 Fourthought Inc., USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import sys, cStringIO
from xml.dom import EMPTY_NAMESPACE
from xml.xslt import OutputParameters

class NullWriter:
    def __init__(self, outputParams=None, stream=None):
        self._outputParams = outputParams or OutputParameters()
        self._stream = stream or cStringIO.StringIO()
        self._savedResult = stream is None
  
    def getMediaType(self):
        return self._outputParams.mediaType

    def getResult(self):
        if self._savedResult:
            return self._stream.getvalue()
        return ''

    def startDocument(self):
        return

    def endDocument(self):
	return
    
    def text(self, text, escapeOutput=1):
        return
    
    def attribute(self, name, value, namespace=EMPTY_NAMESPACE):
        return

    def processingInstruction(self, target, data):
        return

    def comment(self, body):
        return

    def startElement(self, name, namespace=EMPTY_NAMESPACE, extraNss=None):
        return

    def endElement(self, name):
        return
