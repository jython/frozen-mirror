########################################################################
#
# File Name:            HtmlWriter.py
#
#
"""
Implements the HTML output writer for XSLT processor output
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 Fourthought Inc., USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import string
from xml.dom import EMPTY_NAMESPACE
from xml.dom.ext.Printer import TranslateCdata, TranslateCdataAttr
from xml.dom.html import TranslateHtmlCdata
from xml.xslt import NullWriter, XsltException, Error

INDENT = ' '*2

INLINE_ELEMENT = 0
FORBIDDEN_END = 1
PCDATA_ELEMENT = 2
CDATA_CONTENT = 3
HEAD_ELEMENT = 4
NO_STRIP = 5

g_elementTable = {}
g_attributeTable = {}
g_defaultInfo = (0, 0, 0, 0, 0, 0)

def InitTables():
    from xml.dom.html import HTML_4_STRICT_INLINE
    from xml.dom.html import HTML_FORBIDDEN_END
    from xml.dom.html import HTML_BOOLEAN_ATTRS
    
    table = {}
    for tagname in HTML_4_STRICT_INLINE:
        info = list(g_defaultInfo)
        info[INLINE_ELEMENT] = 1
        table[tagname] = info

    for tagname in HTML_FORBIDDEN_END:
        info = table.get(tagname, list(g_defaultInfo))
        info[FORBIDDEN_END] = 1
        table[tagname] = info
        
    # PCDATA containing elements
    for tagname in ['APPLET', 'IMG', 'OBJECT']:
        info = table.get(tagname, list(g_defaultInfo))
        info[PCDATA_ELEMENT] = 1
        table[tagname] = info
                           
    # CDATA containing elements
    for tagname in ['SCRIPT', 'STYLE']:
        info = table.get(tagname, list(g_defaultInfo))
        info[CDATA_CONTENT] = 1
        table[tagname] = info

    # Elements to not strip whitespace from
    for tagname in ['SCRIPT', 'STYLE', 'PRE', 'TEXTAREA']:
        info = table.get(tagname, list(g_defaultInfo))
        info[NO_STRIP] = 1
        table[tagname] = info

    tagname = 'HEAD'
    info = table.get(tagname, list(g_defaultInfo))
    info[HEAD_ELEMENT] = 1
    table[tagname] = info

    for (tagname, value) in table.items():
        g_elementTable[string.upper(tagname)] = tuple(value)

    for name in HTML_BOOLEAN_ATTRS:
        g_attributeTable[string.upper(name)] = 1

InitTables()

class HtmlWriter(NullWriter.NullWriter):
    def __init__(self, outputParams, stream=None, restrictElements=None):
        NullWriter.NullWriter.__init__(self, outputParams, stream)
        # Defaults
        self._outputParams.indent = outputParams.indent in [None, 'yes']
        self._outputParams.encoding = outputParams.encoding or 'iso-8859-1'
        self._outputParams.mediaType = outputParams.mediaType or 'text/html'
        # Process flags
        self._indentLevel = 0
        self._inUnescapedElement = 0
        self._inNoStrip = 0
        self._isInline = [0]
        self._inPCdata = 1
        self._inElement = 0
        self._inHead = 0
        self._first_element = 1
        self._elementRestrictions = restrictElements
        return

    def _tryNewLine(self):
        if not self._inPCdata:
            self._stream.write('\n')
            self._stream.write(INDENT*self._indentLevel)
        return
            
    def _doctype(self, docElem):
        external_id = ''
        if self._outputParams.doctypePublic:
            external_id = ' PUBLIC "' + self._outputParams.doctypePublic + '"'
            if self._outputParams.doctypeSystem:
                external_id = external_id + ' "' + self._outputParams.doctypeSystem + '"'
        elif self._outputParams.doctypeSystem:
            external_id = external_id + ' SYSTEM "' + self._outputParams.doctypeSystem + '"'
        if external_id:
            self._stream.write('<!DOCTYPE %s%s>\n' % (docElem, external_id))
        self._first_element = 0
        return

    def _closeElement(self):
        if self._inElement:
            self._stream.write('>')
            self._inElement = 0
        if self._inHead and self._outputParams.encoding:
            self._inHead = 0
            self.startElement('meta')
            self.attribute('http-equiv', 'Content-Type')
            self.attribute('content', '%s; charset=%s' % (self.getMediaType(),
                                                          self._outputParams.encoding))
            self.endElement('meta')
        return

    def endDocument(self):
        self._closeElement()
        self._stream.flush()
        return
        
    def text(self, text, escapeOutput=1):
        if (self._outputParams.indent and
            not self._inPCdata and
            not self._inNoStrip):
            text = string.strip(text) and text or ''
        if text:
            self._closeElement()
            if not self._inUnescapedElement and escapeOutput:
                if text and text[0] == '>':
                    self._stream.seek(-2, 2)
                    last_chars = self._stream.read()
                else:
                    last_chars = ''
                text = TranslateHtmlCdata(
                    text,
                    self._outputParams.encoding,
                    last_chars
                    )
            self._stream.write(text)
            self._inPCdata = 1
        return

    def attribute(self, name, value, namespace=EMPTY_NAMESPACE):
        self._stream.write(' %s' % name)
        # Output boolean attributes in minimized form 
        
        name = string.upper(name)
        if not (g_attributeTable.get(name) and name == string.upper(value)):
            value = TranslateCdata(value, self._outputParams.encoding)
            value, delimiter = TranslateCdataAttr(value)
            self._stream.write('=%s%s%s' % (delimiter, value, delimiter))
        return

    def processingInstruction(self, target, data):
        self._closeElement()
        self._outputParams.indent and self._tryNewLine()
        target = TranslateCdata(target, self._outputParams.encoding, '')
        data = TranslateCdata(data, self._outputParams.encoding, '')
        self._stream.write('<?%s %s>' % (target, data))
        return

    def comment(self, body):
        self._closeElement()
        body = TranslateCdata(body, self._outputParams.encoding, '')
        self._outputParams.indent and self._tryNewLine()
        self._stream.write('<!--%s-->' % body)
        return

    def startElement(self, name, namespace=EMPTY_NAMESPACE, extraNss=None):
        if self._elementRestrictions is not None:
            if name not in self._elementRestrictions:
                raise XsltException(Error.RESTRICTED_OUTPUT_VIOLATION, name)
        # Close previous element, if any
        self._closeElement()
        self._inElement = 1
            
        info = g_elementTable.get(string.upper(name), g_defaultInfo)
        
        if self._outputParams.indent:
            if not self._isInline[-1] and not self._first_element:
                self._tryNewLine()
            self._indentLevel = self._indentLevel + 1

        if self._first_element:
            self._doctype(name)

        self._stream.write('<' + name)

        self._inPCdata = 0
        self._isInline.append(info[INLINE_ELEMENT])
        self._inUnescapedElement = info[CDATA_CONTENT]
        self._inHead = info[HEAD_ELEMENT]
        self._inNoStrip = info[NO_STRIP]
        return
        
    def endElement(self, name):
        # Close previous element, if any
        empty = self._inElement
        self._closeElement()

        info = g_elementTable.get(string.upper(name), g_defaultInfo)
            
        indent = self._outputParams.indent
        if indent:
            self._indentLevel = self._indentLevel - 1
            
        if not info[FORBIDDEN_END]:
            if (indent and not empty and not self._inPCdata
                and (not self._isInline[-1] or not info[INLINE_ELEMENT])):
                self._tryNewLine()
            self._isInline.pop()
            self._stream.write('</%s>' % name)

        self._inPCdata = info[PCDATA_ELEMENT]
        self._inUnescapedElement = 0
        return

