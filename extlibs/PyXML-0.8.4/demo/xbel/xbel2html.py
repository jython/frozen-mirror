#! /usr/bin/env python
"""
A simple XBEL to HTML converter written with SAX.
"""

# Limitations: will screw up if a folder lacks a 'title' element.
#              no checking of the command-line args

import sys

from xml.sax import make_parser,saxlib,saxutils

# --- HTML templates

top=\
"""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<HTML>
<HEAD>
  <TITLE>%s</TITLE>
  <META NAME="Generator" CONTENT="xbel2html">
  <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=%s">
</HEAD>

<BODY>
<H1>%s</H1>
"""

bottom=\
"""
<HR>
<ADDRESS>
Converted from XBEL by xbel2html.
</ADDRESS>
</BODY>
</HTML>
"""

# --- DocumentHandler

class XBELHandler(saxlib.ContentHandler):

    def __init__(self,writer=sys.stdout,encoding='utf-8'):
        self.stack=[]
        self.writer=writer
        self.last_url=None
        self.inside_ul=0
        self.level=0
        self.encoding=encoding

    def startElement(self,name,attrs):
        self.stack.append(name)
        self.data = ''
        if name=="bookmark":
            self.last_url=attrs["href"].encode(self.encoding)

    def characters(self,data):
        self.data += data.encode(self.encoding)


    def endElement(self,name):
        data = self.data
        if self.stack[-1]=="title" and self.stack[-2]=="xbel":
            self.writer.write(top % (data,self.encoding,data))
            self.state=None

        if self.stack[-1]=="desc" and self.stack[-2]=="xbel":
            self.writer.write("<P>%s</P>\n" % data)

        if self.stack[-1]=="title" and self.stack[-2]=="bookmark":
            if not self.inside_ul:
                self.inside_ul=1
                self.writer.write("<UL>\n")

            self.writer.write('<LI><A HREF="%s">%s</A>. \n' %
                              (self.last_url,data))

        if self.stack[-1]=="desc" and self.stack[-2]=="bookmark":
            self.writer.write(data+"\n\n")

        if self.stack[-1]=="title" and self.stack[-2]=="folder":
            self.writer.write("<LI><B>%s</B>\n" % data)
            self.writer.write("<UL>\n")
            self.inside_ul=1

        del self.stack[-1]

        if name=="folder":
            self.writer.write("</UL>\n")

    def endDocument(self):
        self.writer.write("</UL>\n")
        self.writer.write(bottom)

# --- Main program

if __name__ == '__main__':
    p=make_parser()
    from xml.sax.handler import feature_external_ges
    p.setFeature(feature_external_ges, 0)
    p.setContentHandler(XBELHandler())
    p.setErrorHandler(saxutils.ErrorPrinter())
    p.parse(sys.argv[1])
