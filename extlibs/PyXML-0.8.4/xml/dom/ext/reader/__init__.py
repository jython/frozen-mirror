########################################################################
#
# File Name:            __init__.py
#
#
"""
The 4DOM reader module has routines for deserializing XML and HTML to DOM
WWW: http://4suite.org/4DOM         e-mail: support@4suite.org

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""

import string, urllib2, urlparse, cStringIO, os
from xml.dom.ext import ReleaseNode

try:
    import codecs
    from types import UnicodeType
    encoder = codecs.lookup("utf-8")[0] # encode,decode,reader,writer
    def StrStream(st):
        if type(st) is UnicodeType:
            st = encoder(st)[0]
        return cStringIO.StringIO(st)
except ImportError:
    StrStream = lambda x: cStringIO.StringIO(x)


class BaseUriResolver:
    def resolve(self, uri, base=''):
        #scheme, netloc, path, params, query, fragment
        scheme = urlparse.urlparse(uri)[0]
        if scheme in ['', 'http', 'ftp', 'file', 'gopher']:
            uri = urlparse.urljoin(base, uri)
        if os.access(uri, os.F_OK):
            #Hack because urllib breaks on Windows paths
            stream = open(uri)
        else:
            stream = urllib2.urlopen(uri)
        return stream

BASIC_RESOLVER = BaseUriResolver()

class Reader:
    def clone(self):
        """Used to create a new copy of this instance"""
        if hasattr(self,'__getinitargs__'):
            return apply(self.__class__,self.__getinitargs__())
        else:
            return self.__class__()

    def fromStream(self, stream, ownerDoc=None):
        """Create a DOM from a stream"""
        raise "NOT OVERIDDEN"

    def fromString(self, str, ownerDoc=None):
        """Create a DOM from a string"""
        stream = StrStream(str)
        try:
            return self.fromStream(stream, ownerDoc)
        finally:
            stream.close()

    def fromUri(self, uri, ownerDoc=None):
        stream = BASIC_RESOLVER.resolve(uri)
        try:
            return self.fromStream(stream, ownerDoc)
        finally:
            stream.close()

    def releaseNode(self, node):
        "Free a DOM tree"
        node and ReleaseNode(node)
