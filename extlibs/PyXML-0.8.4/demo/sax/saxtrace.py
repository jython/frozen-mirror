"""
A minimal SAX application that just prints out the document-handler events
it receives.
"""

import sys
from xml.sax import saxexts

# --- SAXtracer

class SAXtracer:

    def __init__(self,objname):
        self.objname=objname
        self.met_name=""

    def __getattr__(self,name):
        self.met_name=name # UGLY! :)
        return self.trace

    def error(self,exception):
        print "err_handler.error(%s)" % str(exception)

    def fatalError(self,exception):
        print "err_handler.fatalError(%s)" % str(exception)

    def warning(self,exception):
        print "err_handler.warning(%s)" % str(exception)

    def characters(self,data,start,length):
        print "doc_handler.characters(%s,%d,%d)" % (`data[start:start+length]`,
                                                    start,length)

    def ignorableWhitespace(self,data,start,length):
        print "doc_handler.ignorableWhitespace(%s,%d,%d)" % \
              (`data[start:start+length]`,start,length)

    def startElement(self, name, attrs):
        attr_str="{"
        for attr in attrs:
            attr_str="%s '%s':'%s'," % (attr_str,attr,attrs[attr])

        if attr_str=="{":
            attr_str="{}"
        else:
            attr_str=attr_str[:-1]+" }"

        print "doc_handler.startElement('%s',%s)" % (name,attr_str)

    def trace(self,*rest):
        str="%s.%s(" % (self.objname,self.met_name)

        for param in rest[:-1]:
            str=str+`param`+", "

        if len(rest)>0:
            print str+`rest[-1]`+")"
        else:
            print str+")"

# --- Main prog

pf=saxexts.ParserFactory()
p=pf.make_parser("xml.sax.drivers.drv_xmlproc")

p.setDocumentHandler(SAXtracer("doc_handler"))
p.setDTDHandler(SAXtracer("dtd_handler"))
p.setErrorHandler(SAXtracer("err_handler"))
p.setEntityResolver(SAXtracer("ent_handler"))
p.parse(sys.argv[1])
