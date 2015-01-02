"""SAX document handlers that support output generation of XML, SGML,
and XHTML.

This module provides three different groups of objects: the actual SAX
document handlers that drive the output, DTD information containers,
and syntax descriptors (of limited public use in most cases).


Output Drivers
--------------

The output drivers conform to the SAX C<DocumentHandler> protocol.
They can be used anywhere a C<DocumentHandler> is used.  Two drivers
are provided: a `basic' driver which creates a fairly minimal output
without much intelligence, and a `pretty-printing' driver that
performs pretty-printing with nice indentation and the like.  Both can
optionally make use of DTD information and syntax objects.


DTD Information Containers
--------------------------



Each DTD information object provides an attribute C<syntax> which
describes the expected output syntax; an alternate can be provided to
the output drivers if desired.


Syntax Descriptors
------------------

Syntax descriptor objects provide several attributes which describe
the various lexical components of XML & SGML markup.  The attributes
have names that reflect the shorthand notation from the SGML world,
but the values are strings which give the appropriate characters for
the markup language being described.  The one addition is the
C<empty_stagc> attribute which should be used to end the start tag of
elements which have no content.  This is needed to properly support
XML and XHTML.

"""
__version__ = '$Revision: 1.9 $'

import string

import xml.parsers.xmlproc.dtdparser
import xml.parsers.xmlproc.xmlapp
from xml.sax.saxutils import escape


DEFAULT_LINELENGTH = 74



class Syntax:
    com = "--"                          # comment start or end
    cro = "&#"                          # character reference open
    refc = ";"                          # reference close
    dso = "["                           # declaration subset open
    dsc = "]"                           # declaration subset close
    ero = "&"                           # entity reference open
    lit = '"'                           # literal start or end
    lit_quoted = '&quot;'               # quoted literal
    lita = "'"                          # literal start or end (alternative)
    mdo = "<!"                          # markup declaration open
    mdc = ">"                           # markup declaration close
    msc = "]]"                          # marked section close
    pio = "<?"                          # processing instruciton open
    stago = "<"                         # start tag open
    etago = "</"                        # end tag open
    tagc = ">"                          # tag close
    vi = "="                            # value indicator

    def __init__(self):
        if self.__class__ is Syntax:
            raise RuntimeError, "Syntax must be subclassed to be used!"


class SGMLSyntax(Syntax):
    empty_stagc = ">"
    pic = ">"                           # processing instruction close
    net = "/"                           # null end tag


class XMLSyntax(Syntax):
    empty_stagc = "/>"
    pic = "?>"                          # processing instruction close
    net = None                          # null end tag not supported


class XHTMLSyntax(XMLSyntax):
    empty_stagc = " />"



class DoctypeInfo:
    syntax = XMLSyntax()

    fpi = None
    sysid = None

    def __init__(self):
        self.__empties = {}
        self.__elements_only = {}
        self.__attribs = {}

    def is_empty(self, gi):
        return self.__empties.has_key(gi)

    def get_empties_list(self):
        return self.__empties.keys()

    def has_element_content(self, gi):
        return self.__elements_only.has_key(gi)

    def get_element_containers_list(self):
        return self.__elements_only.keys()

    def get_attributes_list(self, gi):
        return self.__attribs.get(gi, {}).keys()

    def get_attribute_info(self, gi, attr):
        return self.__attribs[gi][attr]

    def add_empty(self, gi):
        self.__empties[gi] = 1

    def add_element_container(self, gi):
        self.__elements_only[gi] = gi

    def add_attribute_defn(self, gi, attr, type, decl, default):
        try:
            d = self.__attribs[gi]
        except KeyError:
            d = self.__attribs[gi] = {}
        if not d.has_key(attr):
            d[attr] = (type, decl, default)
        else:
            print "<%s> attribute %s already defined" % (gi, attr)

    def load_pubtext(self, pubtext):
        raise NotImplementedError, "sublasses must implement load_pubtext()"


class _XMLDTDLoader(xml.parsers.xmlproc.xmlapp.DTDConsumer):
    def __init__(self, info, parser):
        self.info = info
        xml.parsers.xmlproc.xmlapp.DTDConsumer.__init__(self, parser)
        self.new_attribute = info.add_attribute_defn

    def new_element_type(self, gi, model):
        if model[0] == "|" and model[1][0] == ("#PCDATA", ""):
            # no action required
            pass
        elif model == ("", [], ""):
            self.info.add_empty(gi)
        else:
            self.info.add_element_container(gi)


class XMLDoctypeInfo(DoctypeInfo):
    def load_pubtext(self, sysid):
        parser = xml.parsers.xmlproc.dtdparser.DTDParser()
        loader = _XMLDTDLoader(self, parser)
        parser.set_dtd_consumer(loader)
        parser.parse_resource(sysid)


class XHTMLDoctypeInfo(XMLDoctypeInfo):
    # Bogus W3C cruft requires the extra space when terminating empty elements.
    syntax = XHTMLSyntax()


class SGMLDoctypeInfo(DoctypeInfo):
    syntax = SGMLSyntax()

    import re
    __element_prefix_search = re.compile("<!ELEMENT", re.IGNORECASE).search
    __element_prefix_len = len("<!ELEMENT")
    del re

    def load_pubtext(self, sysid):
        #
        # Really should build a proper SGML DTD parser!
        #
        pubtext = open(sysid).read()
        m = self.__element_prefix_search(pubtext)
        while m:
            pubtext = pubtext[m.end():]
            if pubtext and pubtext[0] in string.whitespace:
                pubtext = string.lstrip(pubtext)
            else:
                continue
            gi, pubtext = string.split(pubtext, None, 1)
            pubtext = string.lstrip(pubtext)
            # maybe need to remove/collect tag occurance specifiers
            # ...
            raise NotImplementedError, "implementation incomplete"
            #
            m = self.__element_prefix_search(pubtext)



class XmlWriter:
    """Basic XML output handler."""

    def __init__(self, fp, standalone=None, dtdinfo=None,
                 syntax=None, linelength=None, encoding='iso-8859-1'):
        self._offset = 0
        self._packing = 1
        self._flowing = 1
        self._write = fp.write
        self._dtdflowing = None
        self._prefix = ''
        self._encoding = encoding
        self.__stack = []
        self.__lang = None
        self.__pending_content = 0
        self.__pending_doctype = 1
        self.__standalone = standalone
        self.__dtdinfo = dtdinfo
        if syntax is None:
            if dtdinfo:
                syntax = dtdinfo.syntax
            else:
                syntax = XMLSyntax()
        self.__syntax = syntax
        self.indentation = 0
        self.indentEndTags = 0
        if linelength is None:
            self.lineLength = DEFAULT_LINELENGTH
        else:
            self.lineLength = linelength

    def setDocumentLocator(self, locator):
        self.locator = locator

    def startDocument(self):
        if self.__syntax.pic == "?>":
            lit = self.__syntax.lit
            s = '%sxml version=%s1.0%s encoding%s%s%s%s' % (
                self.__syntax.pio, lit, lit, self.__syntax.vi, lit,
                self._encoding, lit)
            if self.__standalone:
                s = '%s standalone%s%s%s%s' % (
                    s, self.__syntax.vi, lit, self.__standalone, lit)
            self._write("%s%s\n" % (s, self.__syntax.pic))

    def endDocument(self):
        if self.__stack:
            raise RuntimeError, "open element stack cannot be empty on close"

    def startElement(self, tag, attrs={}):
        if self.__pending_doctype:
            self.handle_doctype(tag)
        self._check_pending_content()
        self.__pushtag(tag)
        self.__check_flowing(tag, attrs)
        if attrs.has_key("xml:lang"):
            self.__lang = attrs["xml:lang"]
            del attrs["xml:lang"]
        if self._packing:
            prefix = ""
        elif self._flowing:
            prefix = self._prefix[:-self.indentation]
        else:
            prefix = ""
        stag = "%s%s%s" % (prefix, self.__syntax.stago, tag)
        prefix = "%s %s" % (prefix, (len(tag) * " "))
        lit = self.__syntax.lit
        lita = self.__syntax.lita
        vi = self.__syntax.vi
        a = ''
        if self._flowing != self.__stack[-1][0]:
            if self._dtdflowing is not None \
               and self._flowing == self._dtdflowing:
                pass
            else:
                a = ' xml:space%s%s%s%s' \
                    % (vi, lit, ["default", "preserve"][self._flowing], lit)
        if self.__lang != self.__stack[-1][1]:
            a = '%s xml:lang%s%s%s%s' % (a, vi, lit, self.lang, lit)
        line = stag + a
        self._offset = self._offset + len(line)
        a = ''
        for k, v in attrs.items():
            if v is None:
                continue
            v = str(v)
            if string.find(v, lit) == -1:
                a = ' %s%s%s%s%s' % (k, vi, lit, escape(str(v)), lit)
            elif string.find(v, lita) == -1:
                a = ' %s%s%s%s%s' % (k, vi, lita, escape(str(v)), lita)
            else:
                a = ' %s%s%s%s%s' % (k, vi, lit,
                                     escape(str(v), {lit:self.__syntax.lit_quoted}),
                                     lita)
            if (self._offset + len(a)) > self.lineLength:
                self._write(line + "\n")
                line = prefix + a
                self._offset = len(line)
            else:
                line = line + a
                self._offset = self._offset + len(a)
        self._write(line)
        self.__pending_content = 1
        if (  self.__dtdinfo and not
              (self.__dtdinfo.has_element_content(tag)
               or self.__dtdinfo.is_empty(tag))):
            self._packing = 1

    def endElement(self, tag):
        if self.__pending_content:
            if self._flowing:
                self._write(self.__syntax.empty_stagc)
                if self._packing:
                    self._offset = self._offset \
                                   + len(self.__syntax.empty_stagc)
                else:
                    self._write("\n")
                    self._offset = 0
            else:
                self._write(self.__syntax.empty_stagc)
                self._offset = self._offset + len(self.__syntax.empty_stagc)
            self.__pending_content = 0
            self.__poptag(tag)
            return
        depth = len(self.__stack)
        if depth == 1 or self._packing or not self._flowing:
            prefix = ''
        else:
            prefix = self._prefix[:-self.indentation] \
                     + (" " * self.indentEndTags)
        self.__poptag(tag)
        self._write("%s%s%s%s" % (
            prefix, self.__syntax.etago, tag, self.__syntax.tagc))
        if self._packing:
            self._offset = self._offset + len(tag) + 3
        else:
            self._write("\n")
            self._offset = 0

    def characters(self, data, start, length):
        data = data[start: start+length]
        if data:
            self._check_pending_content()
            data = escape(data)
            if "\n" in data:
                p = string.find(data, "\n")
                self._offset = len(data) - (p + 1)
            else:
                self._offset = self._offset + len(data)
            self._check_pending_content()
            self._write(data)

    def comment(self, data, start, length):
        data = data[start: start+length]
        self._check_pending_content()
        s = "%s%s%s%s%s" % (self.__syntax.mdo, self.__syntax.com,
                            data, self.__syntax.com, self.__syntax.mdc)
        p = string.rfind(s, "\n")
        if self._packing:
            if p >= 0:
                self._offset = len(s) - (p + 1)
            else:
                self._offset = self._offset + len(s)
        else:
            self._write("%s%s\n" % (self._prefix, s))
            self._offset = 0

    def ignorableWhitespace(self, data, start, length):
        pass

    def processingInstruction(self, target, data):
        self._check_pending_content()
        s = "%s%s %s%s" % (self.__syntax.pio, target, data, self.__syntax.pic)
        prefix = self._prefix[:-self.indentation] \
                 + (" " * self.indentEndTags)
        if "\n" in s:
            p = string.rfind(s, "\n")
            if self._flowing and not self._packing:
                self._write(prefix + s + "\n")
                self._offset = 0
            else:
                self._write(s)
                self._offset = len(s) - (p + 1)
        elif self._flowing and not self._packing:
            self._write(prefix + s + "\n")
            self._offset = 0
        else:
            self._write(s)
            self._offset = self._offset + len(s)


    # This doesn't actually have a SAX equivalent, so we'll use it as
    # an internal helper.

    def handle_doctype(self, root):
        self.__pending_doctype = 0
        if self.__dtdinfo:
            fpi = self.__dtdinfo.fpi
            sysid = self.__dtdinfo.sysid
        else:
            fpi = sysid = None
        lit = self.__syntax.lit
        isxml = self.__syntax.pic == "?>"
        if isxml and sysid:
            s = '%sDOCTYPE %s\n' % (self.__syntax.mdo, root)
            if fpi:
                s = s + '  PUBLIC %s%s%s\n' % (lit, fpi, lit)
                s = s + '         %s%s%s>\n' % (lit, sysid, lit)
            else:
                s = s + '  SYSTEM %s%s%s>\n' % (lit, sysid, lit)
            self._write(s)
            self._offset = 0
        elif not isxml:
            s = "%sDOCTYPE %s" % (self.__syntax.mdo, root)
            if fpi:
                s = '%s\n  PUBLIC %s%s%s' % (s, lit, fpi, lit)
            if sysid:
                s = '%s\n  SYSTEM %s%s%s' % (s, lit, sysid, lit)
            self._write("%s%s\n" % (s, self.__syntax.mdc))
            self._offset = 0

    def handle_cdata(self, data):
        self._check_pending_content()
        # There should be a better way to generate '[CDATA['
        start = self.__syntax.mdo + "[CDATA["
        end = self.__syntax.msc + self.__syntax.mdc
        s = "%s%s%s" % (start, escape(data), end)
        if self._packing:
            if "\n" in s:
                rpos = string.rfind(s, "\n")
                self._offset = len(s) - (rpos + 1) + len(end)
            else:
                self._offset = self._offset + len(s) + len(start + end)
            self._write(s)
        else:
            self._offset = 0
            self._write(s + "\n")


    # Internal helper methods.

    def __poptag(self, tag):
        state = self.__stack.pop()
        self._flowing, self.__lang, expected_tag, \
                       self._packing, self._dtdflowing = state
        if tag != expected_tag:
            raise RuntimeError, \
                  "expected </%s>, got </%s>" % (expected_tag, tag)
        self._prefix = self._prefix[:-self.indentation]

    def __pushtag(self, tag):
        self.__stack.append((self._flowing, self.__lang, tag,
                             self._packing, self._dtdflowing))
        self._prefix = self._prefix + " " * self.indentation

    def __check_flowing(self, tag, attrs):
        """Check the contents of attrs and the DTD information to determine
        whether the following content should be flowed.

        tag -- general identifier of the element being opened
        attrs -- attributes dictionary as reported by the parser or
                 application

        This sets up both the _flowing and _dtdflowing (object) attributes.
        """
        docspec = dtdspec = None
        if self.__dtdinfo:
            try:
                info = self.__dtdinfo.get_attribute_info(tag, "xml:space")
            except KeyError:
                info = None
            if info is not None:
                self._flowing = info[2] != "preserve"
                self._dtdflowing = self._flowing
        if attrs.has_key("xml:space"):
            self._flowing = attrs["xml:space"] != "preserve"
            del attrs["xml:space"]

    def _check_pending_content(self):
        if self.__pending_content:
            s = self.__syntax.tagc
            if self._flowing and not self._packing:
                s = s + "\n"
                self._offset = 0
            else:
                self._offset = self._offset + len(s)
            self._write(s)
            self.__pending_content = 0


class PrettyPrinter(XmlWriter):
    """Pretty-printing XML output handler."""

    def __init__(self, fp, standalone=None, dtdinfo=None,
                 syntax=None, linelength=None,
                 indentation=2, endtagindentation=None):
        XmlWriter.__init__(self, fp, standalone=standalone, dtdinfo=dtdinfo,
                           syntax=syntax, linelength=linelength)
        self.indentation = indentation
        if endtagindentation is not None:
            self.indentEndTags = endtagindentation
        else:
            self.indentEndTags = indentation

    def characters(self, data, start, length):
        data = data[start: start + length]
        if not data:
            return
        self._check_pending_content()
        data = escape(data)
        if not self._flowing:
            self._write(data)
            return
        words = string.split(data)
        begspace = data[0] in string.whitespace
        endspace = words and (data[-1] in string.whitespace)
        prefix = self._prefix
        if len(prefix) > 40:
            prefix = "    "
        offset = self._offset
        L = []
        append = L.append
        if begspace:
            append(" ")
            offset = offset + 1
        ws = ""
        ws_len = 0
        while words:
            w = words[0]
            del words[0]
            if (offset + ws_len + len(w)) > self.lineLength:
                append("\n")
                append(prefix)
                append(w)
                offset = len(prefix) + len(w)
            else:
                append(ws)
                ws, ws_len = " ", 1
                append(w)
                offset = offset + 1 + len(w)
        if endspace:
            append(" ")
            offset = offset + 1
        self._offset = offset
        self._write(string.join(L, ""))
