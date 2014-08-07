########################################################################
#
# File Name:            XPatternParser.py
#
#
"""
Implement the XSLT pattern parsing engine
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.xpath import pyxpath

class XPatternParser:
    def parsePattern(self,st):
        return pyxpath.parser.parsePattern(st)

if __name__ == '__main__':
    st = raw_input(">>> ")
    parser = XPatternParser()
    try:
        result = parser.parsePattern(st)
        result.pprint()
    except XPatternParserBase.InternalException, e:
        XPatternParserBase.PrintInternalException(e)
    except XPatternParserBase.SyntaxException, e:
        XPatternParserBase.PrintSyntaxException(e)
