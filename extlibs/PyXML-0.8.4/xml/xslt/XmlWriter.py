########################################################################
#
# File Name:            XmlWriter.py
#
#
"""
Implements the XML output writer for XSLT processor output
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 Fourthought Inc., USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import os, re, string
import xml.dom.ext
from xml.dom.ext.Printer import TranslateCdata, TranslateCdataAttr
from xml.dom.html import TranslateHtmlCdata
from xml.xslt import XSL_NAMESPACE, NullWriter, XsltException, Error
from xml.dom.html import HTML_4_TRANSITIONAL_INLINE, HTML_4_STRICT_INLINE
from xml.dom import XML_NAMESPACE, EMPTY_NAMESPACE
from xml.dom.html import HTML_FORBIDDEN_END


class ElementData:
    def __init__(self, name, cdataElement, attrs, extraNss=None):
        self.name = name
        self.cdataElement = cdataElement
        self.attrs = attrs
        self.extraNss = extraNss or {}
        return


class XmlWriter(NullWriter.NullWriter):
    def __init__(self, outputParams, stream=None):
        NullWriter.NullWriter.__init__(self, outputParams, stream)
        self._outputParams.encoding = outputParams.encoding or 'UTF-8'
        self._outputParams.indent = outputParams.indent == 'yes'
        self._outputParams.mediaType = outputParams.mediaType or 'text/xml'
        self._currElement = None
        self._namespaces = [{'': EMPTY_NAMESPACE, 'xml': XML_NAMESPACE}]
        self._indent = ''
        self._nextNewLine = 0
        self._cdataSectionElement = 0
        self._first_element = 1
        self._cached = []
        return

    def _doctype(self, docElem):
        external_id = ''
        if self._outputParams.doctypePublic and self._outputParams.doctypeSystem:
            external_id = ' PUBLIC "' + self._outputParams.doctypePublic + '" "' + self._outputParams.doctypeSystem + '"'
        elif self._outputParams.doctypeSystem:
            external_id = ' SYSTEM "' + self._outputParams.doctypeSystem + '"'
        if external_id:
            self._stream.write('<!DOCTYPE %s%s>\n' % (docElem, external_id))
        self._first_element = 0

    def startDocument(self):
        if self._outputParams.omitXmlDeclaration in [None,'no']:
            self._stream.write("<?xml version='%s' encoding='%s'" % (
                self._outputParams.version,
                self._outputParams.encoding))
            if self._outputParams.standalone:
                self._stream.write(" standalone='%s'" % self._outputParams.standalone)
            self._stream.write("?>\n")
        return
        
    def endDocument(self):
        self._completeLastElement(0)
        return

    def text(self, text, escapeOutput=1):
        self._completeLastElement(0)
        if escapeOutput:
            if text and text[0] == '>':
                self._stream.seek(-2, 2)
                last_chars = self._stream.read()
            else:
                last_chars = ''
            text = TranslateCdata(
                text,
                self._outputParams.encoding,
                last_chars,
                markupSafe=self._cdataSectionElement
                )
        self._stream.write(text)
        self._nextNewLine = 0
        return

    def attribute(self, name, value, namespace=EMPTY_NAMESPACE):
        if not self._currElement:
            raise XsltException(Error.ATTRIBUTE_ADDED_AFTER_ELEMENT)
        value = TranslateCdata(value, self._outputParams.encoding)
        self._currElement.attrs[name] = TranslateCdataAttr(value)
        (prefix, local) = xml.dom.ext.SplitQName(name)
        self._namespaces[-1][prefix] = namespace
        return

    def processingInstruction(self, target, data):
        self._completeLastElement(0)
        target = string.strip(TranslateCdata(target, self._outputParams.encoding, ''))
        data = string.strip(TranslateCdata(data, self._outputParams.encoding, ''))
        pi = '<?%s %s?>' % (target, data)
        if self._outputParams.indent:
            self._stream.write("%s%s\n" % (self._indent, pi))
        else:
            self._stream.write(pi)
        self._nextNewLine = 1
        return

    def comment(self, body):
        self._completeLastElement(0)
        body = TranslateCdata(body, self._outputParams.encoding, '')
        comment = "<!--%s-->" % body
        if self._outputParams.indent:
            self._stream.write("%s%s\n" % (self._indent, comment))
        else:
            self._stream.write(comment)
        self._nextNewLine = 1
        return

    def startElement(self, name, namespace=EMPTY_NAMESPACE, extraNss=None):
        extraNss = extraNss or {}

        self._completeLastElement(0)

        if self._first_element:
            self._doctype(name)

        (prefix, local) = xml.dom.ext.SplitQName(name)
        cdatas_flag = (namespace, local) in self._outputParams.cdataSectionElements
        self._currElement = ElementData(name, cdatas_flag, {}, extraNss)
        self._namespaces.append(self._namespaces[-1].copy())
        self._namespaces[-1][prefix] = namespace
        return

    def endElement(self, name):
        if self._currElement:
            elementIsEmpty = 1
            self._completeLastElement(1)
        else:
            elementIsEmpty = 0
        if self._outputParams.indent:
            self._indent = self._indent[:-2]
        if self._cdataSectionElement:
            self._stream.write(']]>')
            self._cdataSectionElement = 0
        if self._outputParams.indent and self._nextNewLine and not elementIsEmpty:
            self._stream.write('\n' + self._indent)
        self._stream.write((not elementIsEmpty) and ('</%s>' % name) or '')
        self._nextNewLine = 1
        del self._namespaces[-1]
        return

    def _completeLastElement(self, elementIsEmpty):
        if self._currElement:
            elem = self._currElement
            if self._outputParams.indent and self._nextNewLine:
                self._stream.write('\n' + self._indent)
            self._stream.write('<' + elem.name)
            for (name, (value, delimiter)) in elem.attrs.items():
                self._stream.write(' %s=%s%s%s' % (name,delimiter,value,delimiter))
            #Handle namespaces
            nss = elem.extraNss
            nss.update(self._namespaces[-1])
            for prefix in nss.keys():
                ns = nss[prefix]
                prev_ns = self._namespaces[-2].get(prefix, None)
                if ns and not prev_ns:
                    if prefix:
                        self._stream.write(" xmlns:%s='%s'" % (prefix, ns))
                    else:
                        self._stream.write(" xmlns='%s'" % ns)
            self._namespaces[-1] = nss
            if elementIsEmpty:
                self._stream.write('/>')
            else:
                self._stream.write('>')
                if self._currElement.cdataElement:
                    self._stream.write('<![CDATA[')
                    self._cdataSectionElement = 1
            self._nextNewLine = 1

            if self._outputParams.indent:
                self._indent = self._indent + '  '
            self._currElement = None
        return
