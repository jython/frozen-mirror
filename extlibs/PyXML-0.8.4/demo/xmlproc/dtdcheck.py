from xml.parsers.xmlproc import xmlproc

import sys

class DTDReporter(xmlproc.DTDConsumer):
    "A simple class that just prints out the events it receives."

    def __init__(self,parser,out=sys.stdout):
        xmlproc.DTDConsumer.__init__(self,parser)
        self.out=out

    def new_general_entity(self,name,val):
        self.out.write("ENTITY: %s [%s]\n" % (name,val))

    def new_external_entity(self,ent_name,pub_id,sys_id,ndata):
        self.out.write("EXTERNAL ENTITY: %s P: [%s] S: [%s] N: %s\n" %\
                       (ent_name,pub_id,sys_id,ndata))

    def new_parameter_entity(self,name,val):
        self.out.write("PE: %s [%s]\n" % (name,val))

    def new_external_pe(self,name,pubid,sysid):
        self.out.write("EXTERNAL PE: %s P: [%s] S: [%s]\n" % (name,pubid,sysid))

    def new_notation(self,name,pubid,sysid):
        self.out.write("NOTATION: %s P: [%s] S: [%s]\n" % (name,pubid,sysid))

    def new_attribute(self,elem,attr,a_type,a_decl,a_def):
        self.out.write("ATTLIST: %s %s %s %s [%s]\n" % (elem,attr,a_type,a_decl,a_def))

    def new_element_type(self,elem_name,elem_cont):
        self.out.write("ELEMENT: %s %s\n" % (elem_name,`elem_cont`))

    # --- Client methods

    def close(self):
        self.out.close()

# --- Main program

if __name__ == '__main__':
    t=xmlproc.DTDParser()
    t.set_dtd_consumer(DTDReporter(t))
    t.parse_resource(sys.argv[1])

    #t.parse_resource("c:\\minedo~1\\data\\sgml\\xml\\xbel-1.0.dtd")
    #t.parse_resource("c:\\minedo~1\\programmering\\python\\xml\\stddirs\\petest.dtd")
