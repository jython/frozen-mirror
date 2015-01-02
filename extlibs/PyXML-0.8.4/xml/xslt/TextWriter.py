########################################################################
#
# File Name:            TextWriter.py
#
#
"""
Implement the core Writer for XSLT processor output
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 Fourthought Inc., USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import os, re, string, cStringIO
from xml.dom import EMPTY_NAMESPACE
import xml.dom.ext
from xml.dom.ext.Printer import TranslateCdata, TranslateCdataAttr
from xml.dom.html import TranslateHtmlCdata
from xml.xslt import XSL_NAMESPACE, TextSax
from xml.dom.html import HTML_4_TRANSITIONAL_INLINE, HTML_4_STRICT_INLINE
from xml.dom import XML_NAMESPACE
from xml.dom.html import HTML_FORBIDDEN_END


class ElementData:
    def __init__(self, name, cdataElement, attrs, extraNss=None):
        self.name = name
        self.cdataElement = cdataElement
        self.attrs = attrs
        self.extraNss = extraNss or {}
        return


class TextWriter:
    def __init__(self, outputParams):
        self._currElement = None
        self._namespaces = [{'': EMPTY_NAMESPACE, 'xml': XML_NAMESPACE}]
        self._result = cStringIO.StringIO()
        self._outputParams = outputParams
        self._outputParams.mediaType = outputParams.mediaType or 'text/plain'
        self._indent = ''
        self._nextNewLine = 0
        self._cdataSectionElement = 0
        self._first_element = 1
        self._strict_inline = [0]
        self._cachedPis = []
        return

    def _prolog(self, docElem):
        if self._outputParams.method == 'html' and self._outputParams.indent is None:
            self._outputParams.indent = 'yes'
        if self._outputParams.method in [None, 'xml']:
            #FIXME: Case-sensitivity?
            if self._outputParams.omitXmlDeclaration in [None,'no']:
                self._result.write("<?xml version='%s' encoding='%s'" % (self._outputParams.version, self._outputParams.encoding or 'UTF-8'))
                if self._outputParams.standalone:
                    self._result.write(" standalone='%s'" % self._outputParams.standalone)
                self._result.write("?>\n")
            if self._outputParams.doctypeSystem:
                self._result.write('<!DOCTYPE ' + docElem + ' SYSTEM "' + self._outputParams.doctypeSystem + '"')
                if self._outputParams.doctypePublic:
                    self._result.write(' PUBLIC "' + self._outputParams.doctypePublic + '"')
                self._result.write('>\n')
        for target,data in self._cachedPis:
            self._writePiOrXmlDecl(target,data)
            self._result.write('\n' + self._indent)
        self._nextNewLine = 0
        return

    def getResult(self):
        self._completeLastElement(0)
        return self._result.getvalue()

    def text(self, text, escapeOutput=1):
        self._completeLastElement(0)
        if escapeOutput:
            if text and text[0] == '>':
                self._result.seek(-2, 2)
                last_chars = self._result.read()
            else:
                last_chars = ''
            new_text = text
            if self._outputParams.method == 'html':
                new_text = TranslateHtmlCdata(
                    new_text,
                    self._outputParams.encoding or 'UTF-8',
                    last_chars
                    )
            else:
                new_text = TranslateCdata(
                    new_text,
                    self._outputParams.encoding or 'UTF-8',
                    last_chars,
                    markupSafe=self._cdataSectionElement
                    )
            self._result.write(new_text)
        else:
            self._result.write(text)
        self._nextNewLine = 0
        return

    def attribute(self, name, value, namespace=EMPTY_NAMESPACE):
        self._currElement.attrs[name] = value
        (prefix, local) = xml.dom.ext.SplitQName(name)
        if self._outputParams.method == 'xml':
            self._namespaces[-1][prefix] = namespace
        return

    def processingInstruction(self, target, data):
        if self._first_element:
            self._cachedPis.append((target,data))
            return
        self._completeLastElement(0)
        self._writePiOrXmlDecl(target,data)
        return

    def _writePiOrXmlDecl(self, target, data):
        pi = '<?%s %s?>' % (target, data)
        if self._outputParams.indent == 'yes':
            self._result.write("%s%s\n" % (self._indent, pi))
        else:
            self._result.write(pi)
        self._nextNewLine = 1
        return

    def comment(self, body):
        self._completeLastElement(0)
        if self._outputParams.indent == 'yes':
            self._result.write(self._indent + "<!--%s-->\n"%(body))
        else:
            self._result.write("<!--%s-->"%(body))
        self._nextNewLine = 1
        return

    def startElement(self, name, namespace=EMPTY_NAMESPACE, extraNss=None):
        extraNss = extraNss or {}
        self._strict_inline.append(string.upper(name) in HTML_4_STRICT_INLINE)
        if self._first_element:
            if not self._outputParams.method:
                if string.upper(name) == 'HTML':
                    self._outputParams.method = 'html'
                else:
                    self._outputParams.method = 'xml'
            self._first_element = 0
            self._prolog(name)
        self._completeLastElement(0)
        (prefix, local) = xml.dom.ext.SplitQName(name)
        cdatas_flag = 0
        if self._outputParams.method == 'xml':
            cdatas_flag = (namespace, local) in self._outputParams.cdataSectionElements
        self._currElement = ElementData(name, cdatas_flag, {}, extraNss)
        self._namespaces.append(self._namespaces[-1].copy())
        if self._outputParams.method == 'xml':
            self._namespaces[-1][prefix] = namespace
        return

    def endElement(self, name):
        if self._currElement:
            elementIsEmpty = 1
            endElementHandled = self._completeLastElement(1)
        else:
            elementIsEmpty = endElementHandled = 0
        if self._outputParams.indent == 'yes':
            self._indent = self._indent[:-2]
        if self._outputParams.method == 'xml' and self._cdataSectionElement:
            self._result.write(']]>')
            self._cdataSectionElement = 0
        if self._outputParams.method == 'html':
            if (string.upper(name) not in HTML_FORBIDDEN_END):
                if self._outputParams.indent == 'yes' and not self._strict_inline[-1]:
                    if self._nextNewLine and not elementIsEmpty:
                        self._result.write('\n' + self._indent)
                    self._result.write((not endElementHandled) and ('</%s>' % name) or '')
                else:
                    self._result.write((not endElementHandled) and ('</%s>' % name) or '')
        else:
            if self._outputParams.indent == 'yes' and self._nextNewLine and not elementIsEmpty:
                self._result.write('\n' + self._indent)
            self._result.write((not endElementHandled) and ('</%s>' % name) or '')
        self._nextNewLine = 1
        del self._namespaces[-1]
        self._strict_inline.pop()
        return

    def _completeLastElement(self, elementIsEmpty):
        endElementHandled = 1
        if self._currElement:
            elem = self._currElement
            if self._outputParams.indent == 'yes' and self._nextNewLine and not self._strict_inline[-1]:
                self._result.write('\n' + self._indent)
            self._result.write('<' + elem.name)
            encoding = self._outputParams.encoding or 'UTF-8'
            for name,value in elem.attrs.items():
                value = TranslateCdata(value, encoding)
                value, delimiter = TranslateCdataAttr(value)
                self._result.write(' %s=%s%s%s' % (name,delimiter,value,delimiter))
            if self._outputParams.method == 'xml':
                #Handle namespaces
                nss = elem.extraNss
                nss.update(self._namespaces[-1])
                for prefix in nss.keys():
                    ns = nss[prefix]
                    prev_ns = self._namespaces[-2].get(prefix, None)
                    if ns and not prev_ns:
                        if prefix:
                            self._result.write(" xmlns:%s='%s'" % (prefix, ns))
                        else:
                            self._result.write(" xmlns='%s'" % ns)
                self._namespaces[-1] = nss
            if elementIsEmpty:
                if self._outputParams.method != 'html':
                    self._result.write('/>')
                else:
                    self._result.write('>')
                    endElementHandled = 0
            else:
                self._result.write('>')
                if self._currElement.cdataElement:
                    self._result.write('<![CDATA[')
                    self._cdataSectionElement = 1
            self._nextNewLine = 1

            if self._outputParams.indent == 'yes':
                self._indent = self._indent + '  '
            self._currElement = None
        return endElementHandled




"""
Note: excerpt from Mike Kay on xsl-list 2000-06-14

In Saxon, for method="html", the highly pragmatic rules for output of
non-ASCII characters are:

for characters in the range 160-255, use an entity reference, e.g.
"&eacute;"
for other non-ASCII characters, use the native character if supported by the
selected encoding, otherwise use a numeric character reference.

There's nothing in the spec to say it has to be this way, the rules have
simply evolved to minimize the number of user complaints.
"""
