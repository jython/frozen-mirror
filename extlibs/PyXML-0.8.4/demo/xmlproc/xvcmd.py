#!/usr/bin/python

"""
A command-line interface to the validating xmlproc parser. Prints error
messages and can output the parsed data in various formats.
"""

usage=\
"""
Usage:

  xvcmd.py [options] [urlstodocs]

  ---Options:
  -c catalog:   path to catalog file to use to resolve public identifiers
  -l language:  ISO 3166 language code for language to use in error messages
  -o format:    Format to output parsed XML. 'e': ESIS, 'x': canonical XML
                and 'n': normalized XML. No data will be output if this
                option is not specified.
  urlstodocs:   URLs to the documents to parse. (You can use plain file names
                as well.) Can be omitted if a catalog is specified and contains
                a DOCUMENT entry.
  -n:           Report qualified names as 'URI name'. (Namespace processing.)
  --nowarn:     Suppress warnings.
  --entstck:    Show entity stack on errors.
  --rawxml:     Show raw XML string where error occurred.

  Catalog files with URLs that end in '.xml' are assumed to be XCatalogs,
  all others are assumed to be SGML Open Catalogs.

  If the -c option is not specified the environment variables XMLXCATALOG
  and XMLSOCATALOG will be used (in that order).
"""

from xml.parsers.xmlproc import xmlval,catalog,xcatalog,xmlproc
import outputters
import sys, getopt, os, string

# --- Utilities

def print_usage(message):
    print message
    print usage
    sys.exit(1)

# --- Initialization

print "xmlproc version %s" % xmlval.version

p=xmlval.XMLValidator()

# --- Interpreting options

try:
    (options,sysids)=getopt.getopt(sys.argv[1:],"c:l:o:n",
                                   ["nowarn","entstck","rawxml"])
except getopt.error,e:
    print_usage("Usage error: "+e)

warnings=1
entstack=0
rawxml=0
cat=None
pf=None
namespaces=0
app=xmlproc.Application()
err_lang=None

for option in options:
    if option[0]=="-c":
        cat=option[1]
    elif option[0]=="-l":
        try:
            p.set_error_language(option[1])
            err_lang=option[1]
        except KeyError:
            print "Error: Language '%s' not available" % option[1]
    elif option[0]=="-o":
        if string.lower(option[1]) == "e":
            app = outputters.ESISDocHandler()
        elif string.lower(option[1]) == "x":
            app = outputters.Canonizer()
        elif string.lower(option[1]) == "n":
            app = outputters.DocGenerator()
        else:
            print_usage("Error: Unknown output format " + option[1])

    elif option[0]=="-n":
        namespaces=1
    elif option[0]=="--nowarn":
        warnings=0
    elif option[0]=="--entstck":
        entstack=1
    elif option[0]=="--rawxml":
        rawxml=1

# Acting on option settings

err = outputters.MyErrorHandler(p, p.parser, warnings, entstack, rawxml)
p.set_error_handler(err)

if namespaces:
    from xml.parsers.xmlproc import namespace

    nsf=namespace.NamespaceFilter(p)
    nsf.set_application(app)
    p.set_application(nsf)
else:
    p.set_application(app)

if cat!=None:
    pf=xcatalog.FancyParserFactory(err_lang)
elif cat==None and os.environ.has_key("XMLXCATALOG"):
    cat=os.environ["XMLXCATALOG"]
    pf=xcatalog.XCatParserFactory(err_lang)
elif cat==None and os.environ.has_key("XMLSOCATALOG"):
    cat=os.environ["XMLSOCATALOG"]
    pf=catalog.CatParserFactory(err_lang)

if cat!=None:
    print "Parsing catalog file '%s'" % cat
    cat=catalog.xmlproc_catalog(cat,pf,err)
    p.set_pubid_resolver(cat)

if len(sysids)==0:
    if cat==None:
        print_usage("You must specify a system identifier if no catalog is "
                    "used")
    elif cat.get_document_sysid()==None:
        print_usage("You must specify a system identifier if the catalog has "
                    "no DOCUMENT entry")

    sysids=[cat.get_document_sysid()]
    print "Parsing DOCUMENT '%s' from catalog" % sysids[0]

# --- Parsing

retval = 0
for sysid in sysids:
    print
    print "Parsing '%s'" % sysid
    p.parse_resource(sysid)
    print
    print "Parse complete, %d error(s)" % err.errors,
    if warnings:
        print "and %d warning(s)" % err.warnings
    else:
        print

    if err.errors:
        retval = 2
    if err.warnings and retval < 1:
        retval = 1        
        
    err.reset()
    p.reset()

sys.exit(retval)
