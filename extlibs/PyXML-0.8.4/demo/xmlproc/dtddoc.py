from xml.parsers.xmlproc import dtdparser,xmlapp,xmldtd,utils

import sys

# --- Utility functions

def print_cm(out,cm):
    if cm==None:
        out.write("ANY")
        return
    elif cm[1]==[]:
        out.write("EMPTY")
        return

    (sep,cont,mod)=cm
    out.write("(")
    for item in cont[:-1]:
        if len(item)==2:
            out.write('<A HREF="#%s">%s</A>%s %s ' % (item[0],item[0],item[1],
                                                      sep))
        else:
            print_cm(out,item)
            out.write(sep+" ")

    item=cont[-1]
    if len(item)==2:
        out.write('<A HREF="#%s">%s</A>%s' % (item[0],item[0],item[1]))
    else:
        print_cm(out,item)
        out.write(sep+" ")

    out.write(")%s " % mod)

# --- Main program

if len(sys.argv) != 2:
    print "Usage: dtddoc.py [file name of DTD file]"
    sys.exit(1)

# Parsing the DTD

print "Parsing DTD"
dp=dtdparser.DTDParser()
dp.set_error_handler(utils.ErrorPrinter(dp))
dtd=xmldtd.CompleteDTD(dp)
#dtd.compile_content_models(0)
dp.set_dtd_consumer(dtd)
dp.parse_resource(sys.argv[1])

# Processing the DTD

print "Processing DTD"

parents={}

def traverse_cm(cur,cm):
    if cm==None:
        return

    for item in cm[1]:
        if len(item)==2:
            try:
                parents[item[0]][cur]=1
            except KeyError:
                print "ERROR: Undeclared element '%s'" % item[0]
        else:
            traverse_cm(cur,item)

parents["#PCDATA"]={}
for elem_name in dtd.get_elements():
    parents[elem_name]={}

for elem_name in dtd.get_elements():
    elem=dtd.get_elem(elem_name)
    traverse_cm(elem_name,elem.get_content_model())

# Printing documentation

print "Printing documentation"

out=open("out.html","w")
out.write(
"""
<HTML>
<HEAD>
  <TITLE>DTD Documentation</TITLE>
  <LINK REL=stylesheet HREF="dtd.css" TYPE="text/css">
</HEAD>

<BODY>
<H1>DTD Documentation</H1>
""")

elems=dtd.get_elements()
elems.sort()
for elem_name in elems:
    out.write('<H2><A NAME="%s">%s</A></H2>' % (elem_name,elem_name))
    out.write("<H3>Parents<H3>")

    out.write("<P>")
    ps=parents[elem_name].keys()
    ps.sort()
    for p in ps:
        out.write('<A HREF="#%s">%s</A> ' % (p,p))

    out.write("</P>")

    elem=dtd.get_elem(elem_name)

    out.write("<H3>Content model</H3>")

    print_cm(out,elem.get_content_model())

    out.write("<H3>Attributes</H3>")
    out.write("<TABLE>")
    out.write("<TR><TH>Name <TH>Type <TH>Declaration <TH>Default")
    attrs=elem.get_attr_list()
    attrs.sort()
    for attr_name in attrs:
        attr=elem.get_attr(attr_name)
        out.write("  <TR><TD>%s <TD>%s <TD>%s <TD>" %
                  (attr_name,attr.get_type(),attr.get_decl()))
        if attr.get_default()!=None:
            out.write("'%s'" % attr.get_default())
    out.write("</TABLE>")


out.write(
"""
<HR>

<ADDRESS>
Produced by dtddoc.py, using xmlproc.
</ADDRESS>

</BODY>
</HTML>
""")

out.close()
