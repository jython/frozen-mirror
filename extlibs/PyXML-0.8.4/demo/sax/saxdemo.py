# A demo SAX application: using SAX to parse XML documents into ESIS
# or canonical XML.

from xml.sax import saxexts, saxlib, saxutils

import sys,urllib2,getopt

### Interpreting arguments (rather crudely)

try:
    (args,trail)=getopt.getopt(sys.argv[1:],"sed:")
    assert trail, "No argument provided"
except Exception,e:
    print "ERROR: %s" % e
    print
    print "Usage: python saxdemo.py [-e] [-d drv] filename [outfilename]"
    print
    print " -e: Output ESIS instead of normalized XML."
    print " -s: Silent (no messages except error messages)"
    print " -d: Use driver 'drv', where 'drv' is a module name."
    print " outfilename: Write to this file."
    sys.exit(1)

driver=None
esis=0
silent=0
in_sysID=trail[0]

if len(trail)==2:
    out_sysID=trail[1]
else:
    out_sysID=""

for (arg,val) in args:
    if arg=="-d":
        driver="xml.sax.drivers.drv_" + val
    elif arg=="-e":
        esis=1
    elif arg=="-s":
        silent=1

p=saxexts.make_parser(driver)
p.setErrorHandler(saxutils.ErrorPrinter())

if out_sysID=="":
    out=sys.stdout
else:
    try:
        out=urllib2.urlopen(out_sysID)
    except IOError,e:
        print out_sysID+": "+str(e)

if esis:
    dh=saxutils.ESISDocHandler(out)
else:
    dh=saxutils.Canonizer(out)

### Ready. Let's go!

if not silent:
    print "Parser: %s (%s, %s)" % (p.get_parser_name(),p.get_parser_version(),
                                   p.get_driver_version())
    print

try:
    p.setDocumentHandler(dh)
    p.parse(in_sysID)
except IOError,e:
    print in_sysID+": "+str(e)
except saxlib.SAXException,e:
    print str(e)

### Cleaning up.

out.close()
