########################################################################
#
# File Name:            ParsedPattern.py
#
#
"""
Parse class to handle base XSLT patterns
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import sys
from xml.xpath import ParsedToken
from xml.xslt import XsltException, Error

class ParsedPattern(ParsedToken.ParsedToken):
    def __init__(self, pattern):
        ParsedToken.ParsedToken.__init__(self, 'PATTERN')
        self._patterns = [pattern]
        self._shortcuts = [pattern.getShortcut()]

    def append(self,pattern):
        self._patterns.append(pattern)
        self._shortcuts.append(pattern.getShortcut())

    def match(self, context, node):
        for pattern,axis_type in self._shortcuts:
            if pattern.match(context, node, axis_type):
                return 1
        return 0

    def getMatchShortcuts(self):
        return map(lambda a, b: (a, b), self._patterns, self._shortcuts)

    def pprint(self, indent=''):
        print indent + str(self)
        for pattern in self._patterns:
            pattern.pprint(indent + '  ')

    def __str__(self):
        return '<Pattern at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        rt = repr(self._patterns[0])
        for pattern in self._patterns[1:]:
            rt = rt + ' | ' + repr(pattern)
        return rt
