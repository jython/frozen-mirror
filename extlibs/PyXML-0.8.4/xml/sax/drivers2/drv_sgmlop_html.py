"""
SAX2 driver for parsing HTML with the sgmlop parser.

$Id: drv_sgmlop_html.py,v 1.3 2002/05/10 14:50:06 akuchling Exp $
"""

version = "0.1"

from drv_sgmlop import *
from xml.dom.html import HTML_CHARACTER_ENTITIES, HTML_FORBIDDEN_END, HTML_OPT_END, HTML_DTD
from string import strip, upper

class SaxHtmlParser(SaxParser):

    def __init__(self, bufsize = 65536, encoding = 'iso-8859-1', verbose = 0):
        SaxParser.__init__(self, bufsize, encoding)
        self.verbose = verbose

    def finish_starttag(self, tag, attrs):
        """uses the HTML DTD to automatically generate events
        for missing tags"""

        # guess omitted close tags
        while self.stack and \
              upper(self.stack[-1]) in HTML_OPT_END and \
              tag not in HTML_DTD.get(self.stack[-1],[]):
            self.unknown_endtag(self.stack[-1])
            del self.stack[-1]

        if self.stack and tag not in HTML_DTD.get(self.stack[-1],[]) and self.verbose:
            print 'Warning : trying to add %s as a child of %s'%\
                  (tag,self.stack[-1])

        self.unknown_starttag(tag,attrs)
        if upper(tag) in HTML_FORBIDDEN_END:
            # close immediately tags for which we won't get an end
            self.unknown_endtag(tag)
            return 0
        else:
            self.stack.append(tag)
        return 1

    def finish_endtag(self, tag):
        if tag in HTML_FORBIDDEN_END :
            # do nothing: we've already closed it
            return
        if tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.unknown_endtag(self.stack[-1])
                del self.stack[-1]
            self.unknown_endtag(tag)
            del self.stack[-1]
        elif self.verbose:
            print "Warning: I don't see where tag %s was opened"%tag


    def handle_data(self,data):
        if self.stack:
            if '#PCDATA' not in HTML_DTD.get(self.stack[-1],[]) and not strip(data):
                # this is probably ignorable whitespace
                self._cont_handler.ignorableWhitespace(data)
            else:
                self._cont_handler.characters(to_xml_string(data,self._encoding))

    def close(self):
        SGMLParser.close(self)
        self.stack.reverse()
        for tag in self.stack:
            self.unknown_endtag(tag)
        self.stack = []
        self._cont_handler.endDocument()


def create_parser():
    return SaxHtmlParser()
