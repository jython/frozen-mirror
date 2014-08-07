"""
An XBEL to HTML converter useful for publishing XBEL bookmark lists on the
web.
"""

import doctree,sys

# --- Configuring

out=sys.stdout
inf=sys.argv[1]

if len(sys.argv)>2:
    stylesheet=sys.argv[2]
else:
    stylesheet=None

# --- Templates

top=\
"""
<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0 Transitional//EN\">
<HTML>
<HEAD>
  <TITLE>%s</TITLE>
  %s
</HEAD>

<BODY>
<H1>%s</H1>
"""

bottom=\
"""
<HR>

<ADDRESS>
Converted by xbel2html.py, using xmlproc.
</ADDRESS>

</BODY>
</HTML>
"""

# --- Conversion code

# Writing document top

root=doctree.build_tree(inf)

title=doctree.get_pcdata(doctree.get_element(root,"title"))
if stylesheet!=None:
    stylesheet='  <LINK HREF="%s" REL=stylesheet TYPE="text/css">\n' % \
                stylesheet
else:
    stylesheet=""

out.write(top % (title,stylesheet,title))

desc=doctree.get_element(root,"desc")
if desc!=None:
    out.write("<P>\n%s\n</P>\n\n" % doctree.get_pcdata(desc))

# Writing folder tree

def output(folder,level):
    title=doctree.get_pcdata(doctree.get_element(folder,"title"))
    desc=doctree.get_element(folder,"desc")
    if desc!=None:
        desc=doctree.get_pcdata(desc)

    if level<3:
        out.write("\n<H%d>%s</H%d>\n" % (level+1,title,level+1))
        if desc!=None:
            out.write("\n<P>%s</P>\n" % desc)
    else:
        a=2/0

    bookmarks=doctree.get_elements(folder,"bookmark")
    if bookmarks!=[]:
        out.write("\n<UL>\n")
        for bookmark in bookmarks:
            url=bookmark[1]["href"]
            title=doctree.get_pcdata(doctree.get_element(bookmark,"title"))
            desc=doctree.get_element(bookmark,"desc")
            if desc!=None:
                desc=doctree.get_pcdata(desc)
            else:
                desc=""

            out.write("  <LI><A HREF=\"%s\">%s</A>. %s\n" % (url,title,desc))

        out.write("</UL>\n")

    for child in doctree.get_elements(folder,"folder"):
        output(child,level+1)

folders=doctree.get_elements(root,"folder")
for folder in folders:
    output(folder,1)

# Writing document bottom

out.write(bottom)
