import os
import sys

from xml.parsers.xmlproc import xmlval
from xml.parsers.xmlproc.utils import validate_doc, load_dtd, ErrorPrinter

dtd = load_dtd("xmlval_illformed.dtd")

f = open("doc.xml", "w")
f.write("""<?xml version="1.0"?>
<!DOCTYPE configuration SYSTEM "xmlval_illformed.dtd">
<configuration><notallowed/></configuration>""")
f.close()

try:
    # validate_doc(dtd, "doc.xml")
    # validate_doc is not suitable since it prints to stderr

    parser = xmlval.XMLValidator()
    parser.dtd = dtd # FIXME: what to do if there is a !DOCTYPE?
    parser.set_error_handler(ErrorPrinter(parser, out=sys.stdout))
    parser.parse_resource("doc.xml")

finally:
    os.unlink("doc.xml")


DOC_TEXT ="""\
<?xml version='1.0' encoding='ISO-8859-1'?>
<!DOCTYPE root [
  <!ELEMENT root EMPTY>
  <!ENTITY % big-ent SYSTEM 'larger-than-16K.ent'>
  %big-ent;
]>
<root/>
"""

LINE = "<!-- This is a really long entity; it doesn't say much, though. -->\n"

f1 = open("doc.xml", "w")
f2 = open("larger-than-16K.ent", "w")

try:
    f1.write(DOC_TEXT)
    f1.close()
    for i in range(int(17*1024 / len(LINE))):
        f2.write(LINE)
    f2.close()
    parser = xmlval.XMLValidator()
    #parser.dtd = dtd # FIXME: what to do if there is a !DOCTYPE?
    parser.set_error_handler(ErrorPrinter(parser, out=sys.stdout))
    parser.parse_resource("doc.xml")

finally:
    os.unlink("doc.xml")
    os.unlink("larger-than-16K.ent")
