#!/usr/bin/env python
#
# lynx_parse.py :
# Read a list of Lynx bookmark files, specified on the command line,
# and outputs the corresponding XBEL document.
#
# Sample usage: ./lynx_parse.py ~/bookmarks/
#    (The script requires the path to the directory where your bookmark files
#     are stored.)
#

import bookmark
import re

def parse_lynx_file(bms, input):
    """Convert a Lynx 2.8 bookmark file to XBEL, reading from the
    input file object, and write to the output file object."""

    # Read the whole file into memory
    data = input.read()

    # Get the title
    m = re.search("<title>(.*?)</title>", data, re.IGNORECASE)
    if m is None: title = "Untitled"
    else: title = m.group(1)

    bms.add_folder( title )

    hrefpat = re.compile( r"""^ \s* <li> \s*
<a \s+ href \s* = \s* "(?P<url> [^"]* )" \s*>
(?P<name> .*? ) </a>""",
    re.IGNORECASE| re.DOTALL | re.VERBOSE | re.MULTILINE)
    pos = 0
    while 1:
        m = hrefpat.search(data, pos)
        if m is None: break
        pos = m.end()
        url, name = m.group(1,2)
        bms.add_bookmark( name, href = url)

    bms.leave_folder()

if __name__ == '__main__':
    import sys, glob

    if len(sys.argv)<2 or len(sys.argv)>3:
        print
        print "A simple utility to convert Lynx bookmarks to XBEL."
        print
        print "Usage: "
        print "  lynx_parse.py <lynx-directory> [<xbel-file>]"
        sys.exit(1)

    bms = bookmark.Bookmarks()

    # Determine the owner on Unix platforms
    import os, pwd
    uid = os.getuid()
    t = pwd.getpwuid( uid )
    bms.owner = t[4]

    glob_pattern = os.path.join(sys.argv[1], '*.html')
    file_list = glob.glob( glob_pattern )
    for file in file_list:
        input = open(file)
        parse_lynx_file(bms, input)

    if len(sys.argv)==3:
        out=open(sys.argv[2],"w")
        bms.dump_xbel(out)
        out.close()
    else:
        bms.dump_xbel()

    # Done
