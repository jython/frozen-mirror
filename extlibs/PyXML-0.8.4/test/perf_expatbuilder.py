"""\
Performance comparison for the xml.dom.expatbuilder DOM loader.

Usage:  %(program)s [-f file] [-p] [file]

        -f file    Read the document to use from `file'.
        -p         Enable profiling support.

        file       Read the document to use from `file'.  Use this or
                   the `-f' option; not both.
"""

import getopt
import os
import sys
import time

from xml.dom import minidom, expatbuilder

# XXX What's the right mix of markup items to text?  What type of
# XXX markup items?

## FRAGMENT = '''\
## <element attr1="foo" attr2="bar">
##   <subelement/>
## </element>
## '''

FRAGMENT = '''\
<element attr1="foo" attr2="bar">
  This is &lt; sample &gt; text.
</element>
'''

CHUNKS = 12000
LOGFILE = "hotshot.log"

first = 1
chunks = CHUNKS

if sys.argv[1:]:
    try:
        chunks = int(sys.argv[-1])
    except ValueError:
        pass
    else:
        del sys.argv[-1]


def timeit(parsefunc, src):
    global first
    if first:
        print "Document source contains", len(src), "bytes."
        first = 0
    modname = parsefunc.func_globals["__name__"]
    t1 = time.time()
    doc = parsefunc(src)
    t2 = time.time()
    doc.unlink()
    print ("using %s.parseString():" % modname), t2 - t1
    return t2 - t1


def usage(err=None, rc=0):
    program = os.path.basename(sys.argv[0])
    if rc:
        f = sys.stderr
    else:
        f = sys.stdout
    if err:
        print >>f, "%s: %s" % (program, err)
        print >>f
    print >>f, __doc__ % {"program": program}
    sys.exit(rc)


do_profile = 0
filename = None
opts, args = getopt.getopt(sys.argv[1:], "f:hp", ["file=", "help", "profile="])
for opt, arg in opts:
    if opt in ('-f', '--file'):
        if filename is not None:
            usage("`-f' argument may only be given once", rc=2)
        if args:
            usage("`-f' and additional file argument are not compatible", rc=2)
        filename = arg
    elif opt in ('-h', '--help'):
        usage()
    elif opt == '-p':
        do_profile = 1
    elif opt == '--profile':
        do_profile = 1
        LOGFILE = arg

if len(args) > 1:
    usage("at most on file argument can be used", rc=2)

if args:
    filename = args[0]

if filename is not None:
    src = open(filename, 'rb')
else:
    src = "<doc>%s</doc>" % (FRAGMENT * chunks)

timeit(minidom.parseString, src)
timeit(expatbuilder.parseString, src)

if sys.argv[1:] == ["-p"]:
    if os.path.exists(LOGFILE):
        os.unlink(LOGFILE)
    import hotshot
    import hotshot.stats

    def profile(*args, **kw):
        profiler = hotshot.Profile(LOGFILE)
        src = "<doc>%s</doc>" % (FRAGMENT * chunks)
        profiler.runcall(expatbuilder.parseString, src, *args, **kw)
        profiler.close()
        stats = hotshot.stats.load(LOGFILE)
        stats.strip_dirs()
        stats.sort_stats('calls', 'time')
        stats.print_stats(20)

    profile()
