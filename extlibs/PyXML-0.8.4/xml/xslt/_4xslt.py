#!/usr/bin/env python
########################################################################
#
# File Name:            4xslt.py
#
#
"""
Command-line invokation of the 4XSLT processor
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999 FourThought LLC, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import re, string, os, sys, getopt, cStringIO, traceback
import xml.dom.ext
from xml import xpath, xslt
from xml.xslt import XsltException
from xml.xslt.Processor import Processor

MAX_PYTHON_RECURSION_DEPTH=10000

g_paramBindingPattern = re.compile(r"([\d\D_\.\-]*:?[\d\D_\.\-]+)=(.*)")

g_usage = """
4XSLT version %s

Usage: %s [options] <source uri> [<stylesheet uri>]...
Options:
  -i                Ignore stylesheet processing instructions in the
                     input file.
  -v                Validate the input file as it is being parsed.
  -D<name>=<value>  Bind a top-level parameter, overriding any binding in
                     the stylesheet.
  -o<filename>      Specify a filename for the output.  This file will be
                     overwritten if present.

Note: if you use "-" as the name of the source document, the source will
instead be read from standard input.
"""

if sys.hexversion >= 0x2000000:
    sys.setrecursionlimit(MAX_PYTHON_RECURSION_DEPTH)

def ParseCommandLine(argv):
    validate_flag = 0
    out_file = None
    ignore_pis = 0
    top_level_params = {}
    command_line_error = 0
    trace_on_error = 0
    stylesheets = []
    source = ""
    try:
        optlist, args = getopt.getopt(argv[1:], 'ivD:o:', ['trace-on-error'])
        source = args[0]
        for k, v in optlist:
            if k == "-v":
                validate_flag = 1
            elif k == "-i":
                ignore_pis = 1
            elif k == "-o":
                out_file = v
            elif k == "-D":
                match = g_paramBindingPattern.match(v)
                top_level_params[match.group(1)] = match.group(2)
            elif k == "--trace-on-error":
                trace_on_error = 1
            else:
                command_line_error = 1
        if len(args) > 1:
            stylesheets = args[1:]
    except:
        command_line_error = 1

    if command_line_error:
        import Ft
        print g_usage % (Ft.__version__, os.path.basename(argv[0]))
        sys.exit(1)

    return (validate_flag,out_file,ignore_pis,top_level_params,stylesheets,source,trace_on_error,command_line_error)


def Run(argv):
    (validate_flag, out_file, ignore_pis, top_level_params,
     stylesheets, source, trace_on_error, command_line_error) = ParseCommandLine(argv)

    out_file = out_file and open(out_file, 'w') or sys.stdout

    processor = Processor()
    import os
    try:
        from Ft.Lib import pDomlette
        BETA_DOMLETTE = os.environ.get("BETA_DOMLETTE")
        if BETA_DOMLETTE and not validate_flag:
            from Ft.Lib import cDomlette
            g_readerClass = cDomlette.RawExpatReader
            reader = cDomlette.RawExpatReader()
        elif validate_flag:
            reader = pDomlette.SaxReader(validate=1)
        else:
            reader = pDomlette.PyExpatReader()
    except ImportError:
        import minisupport
        reader = minisupport.MinidomReader(validate_flag)

    try:
        processor.setDocumentReader(reader)
        for sty in stylesheets:
            processor.appendStylesheetUri(sty)
        if source == '-':
            result = processor.runStream(sys.stdin, ignore_pis,
                                      topLevelParams=top_level_params)
        else:
            result = processor.runUri(source, ignore_pis,
                                      topLevelParams=top_level_params)
    except XsltException, e:
        s = cStringIO.StringIO()
        traceback.print_exc(1000, s)
        sys.stderr.write(s.getvalue())
        sys.stderr.write(str(e) + '\n')
        sys.exit(-1)
    except (xpath.SyntaxException, xpath.InternalException, xslt.SyntaxException, xslt.InternalException), e:
        s = cStringIO.StringIO()
        traceback.print_exc(1000, s)
        sys.stderr.write(s.getvalue())
        if hasattr(e, 'stylesheetUri'):
            sys.stderr.write("While processing %s\n"%e.stylesheetUri)
        sys.stderr.write(str(e) + '\n')
        sys.exit(-1)
    out_file.write(result + '\n')
    out_file.close()


if __name__ == '__main__':
    import sys
    Run(sys.argv)
