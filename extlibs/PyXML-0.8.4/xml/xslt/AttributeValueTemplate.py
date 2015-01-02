########################################################################
#
# File Name:   AttributeValueTemplate.py
#
#
"""
Implementation of AVTs from the XSLT Spec.
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 FourThought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import re, string
from xml.xslt import XsltException, Error
from xml.xpath import XPathParser, Conversions

g_braceSplitPattern = re.compile(r'([\{\}])')

class AttributeValueTemplate:
    def __init__(self, source,reparse = 1):
        self.source = source
        if reparse:
            self._plainParts = []
            self._parsedParts = []
            self._parse()

    def _parse(self):
        parser = XPathParser.XPathParser()
        curr_plain_part = ''
        curr_template_part = ''
        in_plain_part = 1
        split_form = re.split(g_braceSplitPattern, self.source)
        skip_flag = 0
        for i in range(len(split_form)):
            segment = split_form[i]
            if skip_flag:
                skip_flag = skip_flag - 1
                continue
            if segment in ['{', '}']:
                #Here we are accounting for a possible blank segment in between
                try:
                    next = split_form[i + 1] + split_form[i + 2]
                except IndexError:
                    next = None
                if next == segment:
                    if in_plain_part:
                        curr_plain_part = curr_plain_part + segment
                    else:
                        curr_template_part = curr_template_part + segment
                    skip_flag = 2
                elif segment == '{':
                    if in_plain_part:
                        self._plainParts.append(curr_plain_part)
                        in_plain_part = 0

                        curr_plain_part = ''
                    else:
                        raise XsltException(Error.AVT_SYNTAX)
                else:
                    if not in_plain_part:
                        parsed = parser.parseExpression(curr_template_part)
                        self._parsedParts.append(parsed)
                        in_plain_part = 1
                        curr_template_part = ''
                    else:
                        raise XsltException(Error.AVT_SYNTAX)
            else:
                if in_plain_part:
                    curr_plain_part = curr_plain_part + segment
                else:
                    curr_template_part = curr_template_part + segment
        if in_plain_part:
            self._plainParts.append(curr_plain_part)
        else:
            raise XsltException(Error.AVT_SYNTAX)

    def evaluate(self, context):
        result = ''
        expansions = map(
            lambda x, c=context: Conversions.StringValue(x.evaluate(c)),
            self._parsedParts
            )
        for i in range(len(self._parsedParts)):
            result = result + self._plainParts[i] + expansions[i]
        result = result + self._plainParts[-1]
        return result

    def __repr__(self):
        return self.source

    def __getinitargs__(self):
        return (self.source, 0)

    def __getstate__(self):
        return (self._plainParts,self._parsedParts)

    def __setstate__(self, state):
        # Nothing to do
        self._plainParts,self._parsedParts = state

