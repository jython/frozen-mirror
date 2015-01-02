#! /usr/bin/env python

# The seven examples from the Canonical XML spec.
# http://www.w3.org/TR/2001/REC-xml-c14n-20010315

try:
    u = unicode
except NameError:
    def u(x):return x

eg1 = """<?xml version="1.0"?>

<?xml-stylesheet   href="doc.xsl"
   type="text/xsl"   ?>

<!DOCTYPE doc SYSTEM "doc.dtd">

<doc>Hello, world!<!-- Comment 1
--></doc>

<?pi-without-data     ?>

<!-- Comment 2 -->

<!-- Comment 3 -->
"""

eg2 = """<doc>
   <clean>   </clean>
   <dirty>   A   B   </dirty>
   <mixed>
      A
      <clean>   </clean>
      B
      <dirty>   A   B   </dirty>
      C
   </mixed>
</doc>
"""

eg3 = """<!DOCTYPE doc [<!ATTLIST e9 attr CDATA "default">]>
<doc>
   <e1   />
   <e2   ></e2>
   <e3    name = "elem3"   id="elem3"    />
   <e4    name="elem4"   id="elem4"    ></e4>
   <e5 a:attr="out" b:attr="sorted" attr2="all" attr="I'm"
       xmlns:b="http://www.ietf.org"
       xmlns:a="http://www.w3.org"
       xmlns="http://example.org"/>
   <e6 xmlns="" xmlns:a="http://www.w3.org">
       <e7 xmlns="http://www.ietf.org">
           <e8 xmlns="" xmlns:a="http://www.w3.org">
               <e9 xmlns="" xmlns:a="http://www.ietf.org"/>
           </e8>
       </e7>
   </e6>
</doc>
"""

eg3 = """<!DOCTYPE doc [<!ATTLIST e9 attr CDATA "default">]>
<doc xmlns:foo="http://www.bar.org">
   <e1   />
   <e2   ></e2>
   <e3    name = "elem3"   id="elem3"    />
   <e4    name="elem4"   id="elem4"    ></e4>
   <e5 a:attr="out" b:attr="sorted" attr2="all" attr="I'm"
       xmlns:b="http://www.ietf.org"
       xmlns:a="http://www.w3.org"
       xmlns="http://example.org"/>
   <e6 xmlns="" xmlns:a="http://www.w3.org">
       <e7 xmlns="http://www.ietf.org">
           <e8 xmlns="" xmlns:a="http://www.w3.org" a:foo="bar">
               <e9 xmlns="" xmlns:a="http://www.ietf.org"/>
           </e8>
       </e7>
   </e6>
</doc>
"""

eg4 = """<!DOCTYPE doc [ <!ATTLIST normId id ID #IMPLIED> <!ATTLIST normNames attr NMTOKENS #IMPLIED> ]> <doc>
   <text>First line&#x0d;&#10;Second line</text>
   <value>&#x32;</value>
   <compute><![CDATA[value>"0" && value<"10" ?"valid":"error"]]></compute>
   <compute expr='value>"0" &amp;&amp; value&lt;"10" ?"valid":"error"'>valid</compute>
   <norm attr=' &apos;   &#x20;&#13;&#xa;&#9;   &apos; '/>
   <normNames attr='   A   &#x20;&#13;&#xa;&#9;   B   '/>
   <normId id=' &apos;   &#x20;&#13;&#xa;&#9;   &apos; '/>
</doc>"""

eg5 = """<!DOCTYPE doc [
<!ATTLIST doc attrExtEnt ENTITY #IMPLIED>
<!ENTITY ent1 "Hello">
<!ENTITY ent2 SYSTEM "world.txt">
<!ENTITY entExt SYSTEM "earth.gif" NDATA gif>
<!NOTATION gif SYSTEM "viewgif.exe">
]>
<doc attrExtEnt="entExt">
   &ent1;, &ent2;!
</doc>

<!-- Let world.txt contain "world" (excluding the quotes) -->
"""

eg6 = """<?xml version="1.0" encoding="ISO-8859-1"?>
<doc>&#169;</doc>"""

eg7 = """<!DOCTYPE doc [
<!ATTLIST e2 xml:space (default|preserve) 'preserve'>
<!ATTLIST e3 id ID #IMPLIED>
]>
<doc xmlns="http://www.ietf.org" xmlns:w3c="http://www.w3.org">
   <e1>
      <e2 xmlns="">
         <e3 id="E3"/>
      </e2>
   </e1>
</doc>"""

examples = [ eg1, eg2, eg3, eg4, eg5, eg6, eg7]
test_results = {
    eg1: '''PD94bWwtc3R5bGVzaGVldCBocmVmPSJkb2MueHNsIgogICB0eXBlPSJ0ZXh0L3hz
    bCIgICA/Pgo8ZG9jPkhlbGxvLCB3b3JsZCE8IS0tIENvbW1lbnQgMQotLT48L2Rv
    Yz4KPD9waS13aXRob3V0LWRhdGE/Pgo8IS0tIENvbW1lbnQgMiAtLT4KPCEtLSBD
    b21tZW50IDMgLS0+''',

    eg2: '''PGRvYz4KICAgPGNsZWFuPiAgIDwvY2xlYW4+CiAgIDxkaXJ0eT4gICBBICAgQiAg
    IDwvZGlydHk+CiAgIDxtaXhlZD4KICAgICAgQQogICAgICA8Y2xlYW4+ICAgPC9j
    bGVhbj4KICAgICAgQgogICAgICA8ZGlydHk+ICAgQSAgIEIgICA8L2RpcnR5Pgog
    ICAgICBDCiAgIDwvbWl4ZWQ+CjwvZG9jPg==''',

    eg3: '''PGRvYyB4bWxuczpmb289Imh0dHA6Ly93d3cuYmFyLm9yZyI+CiAgIDxlMT48L2Ux
    PgogICA8ZTI+PC9lMj4KICAgPGUzIGlkPSJlbGVtMyIgbmFtZT0iZWxlbTMiPjwv
    ZTM+CiAgIDxlNCBpZD0iZWxlbTQiIG5hbWU9ImVsZW00Ij48L2U0PgogICA8ZTUg
    eG1sbnM9Imh0dHA6Ly9leGFtcGxlLm9yZyIgeG1sbnM6YT0iaHR0cDovL3d3dy53
    My5vcmciIHhtbG5zOmI9Imh0dHA6Ly93d3cuaWV0Zi5vcmciIGF0dHI9IkknbSIg
    YXR0cjI9ImFsbCIgYjphdHRyPSJzb3J0ZWQiIGE6YXR0cj0ib3V0Ij48L2U1Pgog
    ICA8ZTYgeG1sbnM6YT0iaHR0cDovL3d3dy53My5vcmciPgogICAgICAgPGU3IHht
    bG5zPSJodHRwOi8vd3d3LmlldGYub3JnIj4KICAgICAgICAgICA8ZTggeG1sbnM9
    IiIgYTpmb289ImJhciI+CiAgICAgICAgICAgICAgIDxlOSB4bWxuczphPSJodHRw
    Oi8vd3d3LmlldGYub3JnIiBhdHRyPSJkZWZhdWx0Ij48L2U5PgogICAgICAgICAg
    IDwvZTg+CiAgICAgICA8L2U3PgogICA8L2U2Pgo8L2RvYz4=''',

    eg4: '''PGRvYz4KICAgPHRleHQ+Rmlyc3QgbGluZSYjeEQ7ClNlY29uZCBsaW5lPC90ZXh0
    PgogICA8dmFsdWU+MjwvdmFsdWU+CiAgIDxjb21wdXRlPnZhbHVlJmd0OyIwIiAm
    YW1wOyZhbXA7IHZhbHVlJmx0OyIxMCIgPyJ2YWxpZCI6ImVycm9yIjwvY29tcHV0
    ZT4KICAgPGNvbXB1dGUgZXhwcj0idmFsdWU+JnF1b3Q7MCZxdW90OyAmYW1wOyZh
    bXA7IHZhbHVlJmx0OyZxdW90OzEwJnF1b3Q7ID8mcXVvdDt2YWxpZCZxdW90Ozom
    cXVvdDtlcnJvciZxdW90OyI+dmFsaWQ8L2NvbXB1dGU+CiAgIDxub3JtIGF0dHI9
    IiAnICAgICYjeEQmI3hBJiN4OSAgICcgIj48L25vcm0+CiAgIDxub3JtTmFtZXMg
    YXR0cj0iQSAmI3hEJiN4QSYjeDkgQiI+PC9ub3JtTmFtZXM+CiAgIDxub3JtSWQg
    aWQ9IicgJiN4RCYjeEEmI3g5ICciPjwvbm9ybUlkPgo8L2RvYz4=''',

    eg5: '''PGRvYyBhdHRyRXh0RW50PSJlbnRFeHQiPgogICBIZWxsbywgd29ybGQhCjwvZG9j
    Pg==''',

    eg6: '''PGRvYz7CqTwvZG9jPg==''',

    eg7: '''PGRvYyB4bWxucz0iaHR0cDovL3d3dy5pZXRmLm9yZyIgeG1sbnM6dzNjPSJodHRw
    Oi8vd3d3LnczLm9yZyI+CiAgIDxlMT4KICAgICAgPGUyIHhtbG5zPSIiIHhtbDpz
    cGFjZT0icHJlc2VydmUiPgogICAgICAgICA8ZTMgaWQ9IkUzIj48L2UzPgogICAg
    ICA8L2UyPgogICA8L2UxPgo8L2RvYz4=''',

}

# Load XPath and Parser
import sys, types, traceback, StringIO, base64, string
from xml import xpath
from xml.xpath.Context import Context
from xml.dom.ext.reader import PyExpat
#from c14n import Canonicalize
from xml.dom.ext import Canonicalize

# My special reader.
PYE = PyExpat.Reader
class ReaderforC14NExamples(PYE):
    '''A special reader to handle resolution of the C14N examples.
    '''
    def initParser(self):
        PYE.initParser(self)
        self.parser.ExternalEntityRefHandler = self.entity_ref

    def entity_ref(self, *args):
        if args != (u('ent2'), None, u('world.txt'), None): return 0
        self.parser.CharacterDataHandler('world')
        return 1

    # Override some methods from PyExpat.Reader
    def unparsedEntityDecl(self, *args): pass
    def notationDecl(self, *args): pass


try:
    import codecs
    utf8_writer = codecs.lookup('utf-8')[3]
except ImportError:
    def utf8_writer(s):
        return s

def builtin():
    '''Run the builtin tests from the C14N spec.'''
    for i in range(len(examples)):
        num = i+1
        eg = examples[i]

        filename = 'out%d.xml' % num
        try:
            os.unlink(filename)
        except:
            pass

        print 'Doing %d, %s...' % (num, string.replace(eg[0:30], '\n', '\\n')),

        r = ReaderforC14NExamples()
        try:
            dom = r.fromString(eg)
        except Exception, e:
            print '\nException', repr(e)
            traceback.print_exc()
            continue

        # Get the nodeset; the tests have some special cases.
        pattern = '(//. | //@* | //namespace::*)'
        con = Context(dom)
        if eg == eg5:
            pattern = '(//. | //@* | //namespace::*)[not (self::comment())]'
        elif eg == eg7:
            con = Context(dom, processorNss={'ietf': 'http://www.ietf.org'})
            
        nodelist = xpath.Evaluate(pattern, context=con)

        s = StringIO.StringIO()
        outf = utf8_writer(s)

        #Get the unsuppressedPrefixes for exc-c14n; the tests have special casese
        pfxlist = []

        # Canonicalize a DOM with a document subset list according to XML-C14N
        if eg == eg1:
            Canonicalize(dom, outf, subset=nodelist, comments=1)
        else:
            Canonicalize(dom, outf, subset=nodelist)

        expected = base64.decodestring(test_results[eg])
        if s.getvalue() == expected:
            print 'Ok'
        else:
            print 'Error!'
            print 'Got:\n', s.getvalue()
            print 'Expected:\n', expected
            
def usage():
    print '''Options accepted:
    -b, --builtin            Run the C14N builtin tests
    -e                       Exclusive C14N
    -p                       Exclusive C14N inclusive prefixes
    -n string,               Additional NSPrefixes (whitespace delimited)
        --namespaces=string
    -i file, --in=file       Read specified file* (default is stdin)
    -o file, --out=file      Write to specified file* (default is stdout)
    -h, --help               Print this text
    -x query, --xpath=query  Specify an XPATH nodelist
If file (for input/output) is like xxx,name then xxx is used as an
encoding (e.g., "utf-8,foo.txt").
'''

if __name__ != "__main__":
    builtin()
else:
    if len(sys.argv) == 1: sys.argv.append('-b')

    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], "cehbi:o:n:p:x:",
            [ "comments", "exclusive", "help", "builtin", 
            "in=", "out=", "namespaces=", "prefixes=", "xpath=" ])
    except getopt.GetoptError, e:
        print sys.argv[0] + ':', e, '\nTry --help for help.\n'
        sys.exit(1)
    if len(args):
        print 'No arguments, only flags. Try --help for help.'
        sys.exit(1)


    IN, OUT = sys.stdin, sys.stdout
    query = '(//. | //@* | //namespace::*)'
    comments = 0
    exclusive, pfxlist = None, []
    nsdict = {}
    for opt,arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(0)
        if opt in ('-b', '--builtin'):
            builtin()
            sys.exit(0)
        elif opt in ('-c', '--comments'):
            comments = 1
        elif opt in ('-n', '--namespaces'):
            # convert every pair of whitespace delimited  values to dictionary
            nsl = arg.split()
            for i in range(0, len(nsl), 2):
                nsdict[nsl[i]] = nsl[i+1]
        #    print "Namespace prefix arguments is not supported yet."
        elif opt in ('-e', '--exclusive'):
            exclusive = 1
        elif opt in ( '-p', '--prefixes'):
            pfxlist = arg.split(',')
        elif opt in ('-i', '--in'):
            if arg.find(',') == -1:
                IN = open(arg, 'r')
            else:
                import codecs
                encoding, filename = arg.split(',')
                reader = codecs.lookup(encoding)[2]
                IN = reader(open(filename, 'r'))
        elif opt in ('-o', '--out'):
            if arg.find(',') == -1:
                OUT = open(arg, 'w')
            else:
                import codecs
                encoding, filename = arg.split(',')
                writer = codecs.lookup(encoding)[3]
                OUT = writer(open(filename, 'w'))
        elif opt in ('-x', '--xpath'):
            query = arg
            
    r = PYE()
    dom = r.fromStream(IN)
    context = Context(dom, processorNss=nsdict)
    nodelist = xpath.Evaluate(query, context=context)
    if exclusive:
        Canonicalize(dom, OUT, subset=nodelist, comments=comments, unsuppressedPrefixes=pfxlist)
    else:
        Canonicalize(dom, OUT, subset=nodelist, comments=comments) #    nsdict=nsdict
    OUT.close()
