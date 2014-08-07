#!/usr/bin/python

"""
A command-line interface to the xmlproc parser. It continues parsing
even after fatal errors, in order to be find more errors, since this
does not mean feeding data to the application after a fatal error
(which would be in violation of the spec).
"""

usage=\
"""
Usage:

  xpcmd.py [options] [urltodoc]

  ---Options:
  -l language: ISO 3166 language code for language to use in error messages
  -o format:   Format to output parsed XML. 'e': ESIS, 'x': canonical XML
               and 'n': normalized XML. No data will be output if this
               option is not specified.
  urltodoc:    URL to the document to parse. (You can use plain file names
               as well.) Can be omitted if a catalog is specified and contains
               a DOCUMENT entry.
  -n:          Report qualified names as 'URI name'. (Namespace processing.)
  --nowarn:    Don't write warnings to console.
  --entstck:   Show entity stack on errors.
  --extsub:    Read the external subset of documents.
"""

# --- INITIALIZATION

import sys,outputters,getopt
from xml.parsers.xmlproc import xmlproc

# --- Interpreting options

try:
    (options,sysids)=getopt.getopt(sys.argv[1:],"l:o:n",
                                   ["nowarn","entstck","rawxml","extsub"])
except getopt.error,e:
    print "Usage error: "+e
    print usage
    sys.exit(1)

pf=None
namespaces=0
app=xmlproc.Application()
warnings=1
entstack=0
rawxml=0
extsub=0

p=xmlproc.XMLProcessor()

for option in options:
    if option[0]=="-l":
        try:
            p.set_error_language(option[1])
        except KeyError:
            print "Error language '%s' not available" % option[1]
    elif option[0]=="-o":
        if option[1]=="e" or option[1]=="E":
            app=outputters.ESISDocHandler()
        elif option[1]=="x" or option[1]=="X":
            app=outputters.Canonizer()
        elif option[1]=="n" or option[1]=="N":
            app=outputters.DocGenerator()
        else:
            print "Error: Unknown output format "+option[1]
            print usage
    elif option[0]=="-n":
        namespaces=1
    elif option[0]=="--nowarn":
        warnings=0
    elif option[0]=="--entstck":
        entstack=1
    elif option[0]=="--rawxml":
        rawxml=1
    elif option[0]=="--extsub":
        extsub=1

# Acting on option settings

err=outputters.MyErrorHandler(p, p, warnings, entstack, rawxml)
p.set_error_handler(err)

if namespaces:
    from xml.parsers.xmlproc import namespace

    nsf=namespace.NamespaceFilter(p)
    nsf.set_application(app)
    p.set_application(nsf)
else:
    p.set_application(app)

if len(sysids)==0:
    print "You must specify a file to parse"
    print usage
    sys.exit(1)

if extsub:
    p.set_read_external_subset(extsub)

# --- Starting parse

print "xmlproc version %s" % xmlproc.version

for sysid in sysids:
    print
    print "Parsing '%s'" % sysid
    p.set_data_after_wf_error(0)
    p.parse_resource(sysid)
    print "Parse complete, %d error(s)" % err.errors,

    if warnings:
        print "and %d warning(s)" % err.warnings
    else:
        print

    err.reset()
    p.reset()
