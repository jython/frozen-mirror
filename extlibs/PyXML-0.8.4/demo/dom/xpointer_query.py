"""Demonstrates using the xptr.py tool to query DOM Nodes using the XPointer spec"""

from xml.dom import ext
from xml.dom.ext.reader import Sax2
import xptr


if __name__ == '__main__':
    import sys

    xpointer_expr = sys.argv[1]

    try:
        xml_dom_object = Sax2.FromXmlUrl(sys.argv[2], validate=0)
    except Sax.saxlib.SAXException, msg:
        print "SAXException caught:", msg
    except Sax.saxlib.SAXParseException, msg:
        print "SAXParseException caught:", msg

    result_node = xptr.LocateNode(xml_dom_object, xpointer_expr)
    ext.StripXml(result_node)
    ext.PrettyPrint(result_node)
    ext.ReleaseNode(result_node)
