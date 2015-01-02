#!/usr/bin/python

"""
A simple command-line interface to the DTD parser. Intended for those rare
cases when one wants to just parse a DTD and nothing more.
"""

import sys, getopt
from xml.parsers.xmlproc import xmlproc,dtdparser,utils,xmldtd

# --- Doco

usage=\
"""
Usage:

  python dtdcmd.py [--list] <urltodtd>+

  ---Options:
  --list:   List all declarations after parsing.
"""

# --- Utilities

def paired_list_to_hash(list):
    hash = {}
    for (name, value) in list:
        hash[name] = value
    return hash

# --- Functionality

def listdecls(dtd):
    print
    print "=== DECLARATIONS"
    print
    print "---Elements"

    elems = dtd.get_elements()
    elems.sort()
    for elem in elems:
        print elem

    print
    print "---Entities"

    ents = dtd.get_general_entities()
    ents.sort()
    for ent in ents:
        print ent

    print
    print "---Notations"

    nots = dtd.get_notations()
    if nots == []:
        print "No notations declared."
    else:
        nots.sort()
        for notation in nots:
            print notation

# --- Head

print
print "xmlproc version %s" % xmlproc.version

# --- Argument interpretation

try:
    (options,sysids)=getopt.getopt(sys.argv[1:],"",["list"])
except getopt.error,e:
    print "Usage error: "+e
    print usage
    sys.exit(1)

options = paired_list_to_hash(options)

list = options.has_key("--list")

# --- Initialization

parser=dtdparser.DTDParser()
if list:
    dtd = xmldtd.CompleteDTD(parser)
    parser.set_dtd_consumer(dtd)
parser.set_error_handler(utils.ErrorPrinter(parser))

# --- Parsing

for sysid in sysids:
    print "Parsing",sysid
    parser.parse_resource(sysid)
print "Parsing complete"

# --- Reporting

if list:
    listdecls(dtd)
