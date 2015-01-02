#!/usr/bin/env python
#
# qtfmt.py v1.10
# v1.10 : Updated to use Python 2.0 Unicode type.
#
# Read a document in the quotation DTD, converting it to a list of Quotation
# objects.  The list can then be output in several formats.

__doc__ = """Usage: qtfmt.py [options] file1.xml file2.xml ...
If no filenames are provided, standard input will be read.
Available options:
  -f or --fortune   Produce output for the fortune(1) program
  -h or --html      Produce HTML output
  -t or --text      Produce plain text output
  -m N or --max N   Suppress quotations longer than N lines;
                    defaults to 0, which suppresses no quotations at all.
"""

import string, re, cgi, types
import codecs

from xml.sax import saxlib, saxexts

def simplify(t, indent="", width=79):
    """Strip out redundant spaces, and insert newlines to
    wrap the text at the given width."""
    t = string.strip(t)
    t = re.sub('\s+', " ", t)
    if t=="": return t
    t = indent + t
    t2 = ""
    while len(t) > width:
        index = string.rfind(t, ' ', 0, width)
        if index == -1: t2 = t2 + t[:width] ; t = t[width:]
        else: t2 = t2 + t[:index] ; t = t[index+1:]
        t2 = t2 + '\n'
    return t2 + t

class Quotation:
    """Encapsulates a single quotation.
    Attributes:
    stack -- used during construction and then deleted
    text -- A list of Text() instances, or subclasses of Text(),
            containing the text of the quotation.
    source -- A list of Text() instances, or subclasses of Text(),
            containing the source of the quotation.  (Optional)
    author -- A list of Text() instances, or subclasses of Text(),
            containing the author of the quotation.  (Optional)

    Methods:
    as_fortune() -- return the quotation formatted for fortune
    as_html() -- return an HTML version of the quotation
    as_text() -- return a plain text version of the quotation
    """
    def __init__(self):
        self.stack = [ Text() ]
        self.text = []

    def as_text(self):
        "Convert instance into a pure text form"
        output = ""

        def flatten(textobj):
            "Flatten a list of subclasses of Text into a list of paragraphs"
            if type(textobj) != types.ListType: textlist=[textobj]
            else: textlist = textobj

            paragraph = "" ; paralist = []
            for t in textlist:
                if (isinstance(t, PreformattedText) or
                    isinstance(t, CodeFormattedText) ):
                    paralist.append(paragraph)
                    paragraph = ""
                    paralist.append(t)
                elif isinstance(t, Break):
                    paragraph = paragraph + t.as_text()
                    paralist.append(paragraph)
                    paragraph = ""
                else:
                    paragraph = paragraph + t.as_text()
            paralist.append(paragraph)
            return paralist

        # Flatten the list of instances into a list of paragraphs
        paralist = flatten(self.text)
        if len(paralist) > 1:
            indent = 2*" "
        else:
            indent = ""

        for para in paralist:
            if isinstance(para, PreformattedText) or isinstance(para, CodeFormattedText):
                output = output + para.as_text()
            else:
                output = output + simplify(para, indent) + '\n'
        attr = ""
        for i in ['author', 'source']:
            if hasattr(self, i):
                paralist = flatten(getattr(self, i))
                text = string.join(paralist)
                if attr:
                    attr = attr + ', '
                    text = string.lower(text[:1]) + text[1:]
                attr = attr + text
        attr=simplify(attr, width = 79 - 4 - 3)
        if attr: output = output + '  -- '+re.sub('\n', '\n   ', attr)
        return output + '\n'

    def as_fortune(self):
        return self.as_text() + '%'

    def as_html(self):
        output = "<P>"
        def flatten(textobj):
            if type(textobj) != types.ListType: textlist = [textobj]
            else: textlist = textobj

            paragraph = "" ; paralist = []
            for t in textlist:
                paragraph = paragraph + t.as_html()
                if isinstance(t, Break):
                    paralist.append(paragraph)
                    paragraph = ""
            paralist.append(paragraph)
            return paralist

        paralist = flatten(self.text)
        for para in paralist: output = output + string.strip(para) + '\n'
        attr = ""
        for i in ['author', 'source']:
            if hasattr(self, i):
                paralist = flatten(getattr(self, i))
                text = string.join(paralist)
                attr=attr + ('<P CLASS=%s>' % i) + string.strip(text)
        return output + attr

# Text and its subclasses are used to hold chunks of text; instances
# know how to display themselves as plain text or as HTML.

class Text:
    "Plain text"
    def __init__(self, text=""):
        self.text = text

    # We need to allow adding a string to Text instances.
    def __add__(self, val):
        newtext = self.text + str(val)
        # __class__ must be used so subclasses create instances of themselves.
        return self.__class__(newtext)

    def __str__(self): return self.text
    def __repr__(self):
        s = string.strip(self.text)
        if len(s) > 15: s = s[0:15] + '...'
        return '<%s: "%s">' % (self.__class__.__name__, s)

    def as_text(self): return self.text
    def as_html(self): return cgi.escape(self.text)

class PreformattedText(Text):
    "Text inside <pre>...</pre>"
    def as_text(self):
        return str(self.text)
    def as_html(self):
        return '<pre>' + cgi.escape(str(self.text)) + '</pre>'

class CodeFormattedText(Text):
    "Text inside <code>...</code>"
    def as_text(self):
        return str(self.text)
    def as_html(self):
        return '<code>' + cgi.escape(str(self.text)) + '</code>'

class CitedText(Text):
    "Text inside <cite>...</cite>"
    def as_text(self):
        return '_' + simplify(str(self.text)) + '_'
    def as_html(self):
        return '<cite>' + string.strip(cgi.escape(str(self.text))) + '</cite>'

class ForeignText(Text):
    "Foreign words, from Latin or French or whatever."
    def as_text(self):
        return '_' + simplify(str(self.text)) + '_'
    def as_html(self):
        return '<i>' + string.strip(cgi.escape(str(self.text))) + '</i>'

class EmphasizedText(Text):
    "Text inside <em>...</em>"
    def as_text(self):
        return '*' + simplify(str(self.text)) + '*'
    def as_html(self):
        return '<em>' + string.strip(cgi.escape(str(self.text))) + '</em>'

class Break(Text):
    def as_text(self): return ""
    def as_html(self): return "<P>"

# The QuotationDocHandler class is a SAX handler class that will
# convert a marked-up document using the quotations DTD into a list of
# quotation objects.

class QuotationDocHandler(saxlib.HandlerBase):
    def __init__(self, process_func):
        self.process_func = process_func
        self.newqt = None

    # Errors should be signaled, so we'll output a message and raise
    # the exception to stop processing
    def fatalError(self, exception):
        sys.stderr.write('ERROR: '+ str(exception)+'\n')
        sys.exit(1)
    error = fatalError
    warning = fatalError

    def characters(self, ch, start, length):
        if self.newqt != None:
            s = ch[start:start+length]

            # Undo the UTF-8 encoding, converting to ISO Latin1, which
            # is the default character set used for HTML.
            latin1_encode = codecs.lookup('iso-8859-1') [0]
            unicode_str = s
            s, consumed = latin1_encode( unicode_str )
            assert consumed == len( unicode_str )

            self.newqt.stack[-1] = self.newqt.stack[-1] + s

    def startDocument(self):
        self.quote_list = []

    def startElement(self, name, attrs):
        methname = 'start_'+str(name)
        if hasattr(self, methname):
            method = getattr(self, methname)
            method(attrs)
        else:
            sys.stderr.write('unknown start tag: <' + name + ' ')
            for name, value in attrs.items():
                sys.stderr.write(name + '=' + '"' + value + '" ')
            sys.stderr.write('>\n')

    def endElement(self, name):
        methname = 'end_'+str(name)
        if hasattr(self, methname):
            method = getattr(self, methname)
            method()
        else:
            sys.stderr.write('unknown end tag: </' + name + '>\n')

    # There's nothing to be done for the <quotations> tag
    def start_quotations(self, attrs):
        pass
    def end_quotations(self):
        pass

    def start_quotation(self, attrs):
        if self.newqt == None: self.newqt = Quotation()

    def end_quotation(self):
        st = self.newqt.stack
        for i in range(len(st)):
            if type(st[i]) == types.StringType:
                st[i] = Text(st[i])
        self.newqt.text=self.newqt.text + st
        del self.newqt.stack
        if self.process_func: self.process_func(self.newqt)
        else:
            print "Completed quotation\n ", self.newqt.__dict__
        self.newqt=Quotation()

    # Attributes of a quotation: <author>...</author> and <source>...</source>
    def start_author(self, data):
        # Add the current contents of the stack to the text of the quotation
        self.newqt.text = self.newqt.text + self.newqt.stack
        # Reset the stack
        self.newqt.stack = [ Text() ]
    def end_author(self):
        # Set the author attribute to contents of the stack; you can't
        # have more than one <author> tag per quotation.
        self.newqt.author = self.newqt.stack
        # Reset the stack for more text.
        self.newqt.stack = [ Text() ]

    # The code for the <source> tag is exactly parallel to that for <author>
    def start_source(self, data):
        self.newqt.text = self.newqt.text + self.newqt.stack
        self.newqt.stack = [ Text() ]
    def end_source(self):
        self.newqt.source = self.newqt.stack
        self.newqt.stack = [ Text() ]

    # Text markups: <br/> for breaks, <pre>...</pre> for preformatted
    # text, <em>...</em> for emphasis, <cite>...</cite> for citations.

    def start_br(self, data):
        # Add a Break instance, and a new Text instance.
        self.newqt.stack.append(Break())
        self.newqt.stack.append( Text() )
    def end_br(self): pass

    def start_pre(self, data):
        self.newqt.stack.append( Text() )
    def end_pre(self):
        self.newqt.stack[-1] = PreformattedText(self.newqt.stack[-1])
        self.newqt.stack.append( Text() )

    def start_code(self, data):
        self.newqt.stack.append( Text() )
    def end_code(self):
        self.newqt.stack[-1] = CodeFormattedText(self.newqt.stack[-1])
        self.newqt.stack.append( Text() )

    def start_em(self, data):
        self.newqt.stack.append( Text() )
    def end_em(self):
        self.newqt.stack[-1] = EmphasizedText(self.newqt.stack[-1])
        self.newqt.stack.append( Text() )

    def start_cite(self, data):
        self.newqt.stack.append( Text() )
    def end_cite(self):
        self.newqt.stack[-1] = CitedText(self.newqt.stack[-1])
        self.newqt.stack.append( Text() )

    def start_foreign(self, data):
        self.newqt.stack.append( Text() )
    def end_foreign(self):
        self.newqt.stack[-1] = ForeignText(self.newqt.stack[-1])
        self.newqt.stack.append( Text() )

if __name__ == '__main__':
    import sys, getopt

    # Process the command-line arguments
    opts, args = getopt.getopt(sys.argv[1:], 'fthm:r',
                               ['fortune', 'text', 'html', 'max=', 'help',
                                'randomize'] )
    # Set defaults
    maxlength = 0 ; method = 'as_fortune'
    randomize = 0

    # Process arguments
    for opt, arg in opts:
        if opt in ['-f', '--fortune']:
            method='as_fortune'
        elif opt in ['-t', '--text']:
            method = 'as_text'
        elif opt in ['-h', '--html']:
            method = 'as_html'
        elif opt in ['-m', '--max']:
            maxlength = string.atoi(arg)
        elif opt in ['-r', '--randomize']:
            randomize = 1
        elif opt == '--help':
            print __doc__ ; sys.exit(0)

    # This function will simply output each quotation by calling the
    # desired method, as long as it's not suppressed by a setting of
    # --max.
    qtlist = []
    def process_func(qt, qtlist=qtlist, maxlength=maxlength, method=method):
        func = getattr(qt, method)
        output = func()
        length = string.count(output, '\n')
        if maxlength!=0 and length > maxlength: return
        qtlist.append(output)

    # Loop over the input files; use sys.stdin if no files are specified
    if len(args) == 0: args = [sys.stdin]
    for file in args:
        if type(file) == types.StringType: input = open(file, 'r')
        else: input = file

        # Enforce the use of the Expat parser, because the code needs to be
        # sure that the output will be UTF-8 encoded.
        p=saxexts.XMLParserFactory.make_parser(["xml.sax.drivers.drv_pyexpat"])
        dh = QuotationDocHandler(process_func)
        p.setDocumentHandler(dh)
        p.setErrorHandler(dh)
        p.parseFile(input)

        if type(file) == types.StringType: input.close()
        p.close()

    # Randomize the order of the quotations
    if randomize:
        import whrandom
        q2 = []
        for i in range(len(qtlist)):
            qt = whrandom.randint(0,len(qtlist)-1 )
            q2.append( qtlist[qt] )
            qtlist[qt:qt+1] = []
        assert len(qtlist) == 0
        qtlist = q2

    for quote in qtlist:
        print quote

    # We're done!
