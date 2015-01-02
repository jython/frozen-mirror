#!/usr/bin/env python

"""
Small utility to parse Opera bookmark files.
Written by Lars Marius Garshol
"""

import string,bookmark,time

# --- Constants

short_months={"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05",
              "Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10",
              "Nov":"11","Dec":"12"}

# --- Parsing exception

class OperaParseException(Exception):
    pass

# --- Methods

def readfield(infile, fieldname, required = 1):
    line = infile.readline()
    linelength = len(line)
    pos = string.find(line,fieldname+"=")
    if pos == -1 and required:
        raise OperaParseException("Field '%s' missing" % fieldname)

    if pos == -1 and required == 0:
        infile.seek(-linelength, 1)

    return string.rstrip(line[pos+len(fieldname)+1:])

def swallow_rest(infile):
    "Reads input until first blank line."
    while 1:
        line=infile.readline()
        if line=="" or line=="\n" or line=="\015\012": break

def parse_date(date):
    # CREATED=904923783 (Fri Sep 04 17:43:03 1998)
    # VISITED=0 (?)

    if date=="":
        return None

    lp=string.find(date,"(")
    rp=string.find(date,")")
    if lp==-1 or rp==-1:
        if string.find(date," ")!=-1:
            raise OperaParseException("Can't handle this date: %s" % `date`)

        t=time.localtime(string.atoi(date))
        return "%s%s%s" % (t[0],string.zfill(t[1],2),string.zfill(t[2],2))

    if date[lp:rp+1]=="(?)":
        return None

    month=short_months[date[lp+5:lp+8]]
    day=date[lp+9:lp+11]
    year=date[rp-4:rp]

    return "%s%s%s" % (year,month,day)

def parse_adr(filename):
    bms=bookmark.Bookmarks()

    infile=open(filename)
    version=infile.readline()

    while 1:
        line=infile.readline()
        if line=="": break
        line=string.rstrip(line)

        if line=="#FOLDER":
            name=readfield(infile,"NAME")
            created=parse_date(readfield(infile,"CREATED"))
            parse_date(readfield(infile, "VISITED", 0)) # just throw this away
            order = readfield(infile, "ORDER", 0)
            swallow_rest(infile)

            bms.add_folder(name,created)
        elif line=="#URL":
            name=readfield(infile,"NAME")
            url=readfield(infile,"URL")
            created=parse_date(readfield(infile,"CREATED"))
            visited=parse_date(readfield(infile, "VISITED", 0))
            order = readfield(infile, "ORDER", 0)
            swallow_rest(infile)

            bms.add_bookmark(name,created,visited,None,url)
        elif line=="-":
            bms.leave_folder()

    return bms

# --- Test-program

if __name__ == '__main__':
    import sys

    if len(sys.argv)<2 or len(sys.argv)>3:
        print
        print "A simple utility to convert Opera bookmarks to XBEL."
        print
        print "Usage: "
        print "  adr_parse.py <adr-file> [<xbel-file>]"
        sys.exit(1)

    bms=parse_adr(sys.argv[1])

    if len(sys.argv)==3:
        out=open(sys.argv[2],"w")
        bms.dump_xbel(out)
        out.close()
    else:
        bms.dump_xbel()

    # Done
