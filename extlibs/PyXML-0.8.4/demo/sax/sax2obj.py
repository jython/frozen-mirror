"""
A general XML element -> Python object converter based on SAX.
"""

from xml.sax import saxexts,saxlib,saxutils
import re,string

reg_ws=re.compile("[%s]+" % string.whitespace)

class ConvSpec:
    """Contains the information needed to convert SAX events to Python
    objects."""

    def __init__(self):
        pass

class SAXObject:

    def __init__(self):
        self._fields={}

    def has_field(self,field):
        return self._fields.has_key(field)

    def get_fields(self):
        return self._fields.keys()

    def get_field(self,field):
        return self._fields[field]

    def set_field(self,field,value):
        self._fields[field]=value

    def display(self):
        for field in self._fields.keys():
            print "%s=%s" % (field,self._fields[field])

    def __getattr__(self,attr):
        try:
            return self._fields[attr]
        except KeyError,e:
            raise AttributeError(str(e))

    def __cmp__(self,obj):
        if id(obj)==id(self):
            return 0
        else:
            return 1

class DocHandler(saxlib.DocumentHandler):

    def __init__(self,target_elem,list_elems,ign_elems,rep_field):
        self.target_elem=target_elem
        self.list_elems=list_elems
        self.ign_elems=ign_elems
        self.rep_field=rep_field

        self.ignoring=0
        self.objects=[]
        self.current=None
        self.cur_data=""
        self.stack=[]

    def startElement(self,name,attrs):
        if self.ignoring:
            return

        if name==self.target_elem:
            self.current=SAXObject()
            for attr in attrs:
                self.current.set_field(attr,attrs[attr])
        elif self.list_elems.has_key(name):
            if not self.current.has_field(name):
                self.current.set_field(name,[])

            self.stack.append(self.current)
            self.current=SAXObject()
        elif self.rep_field.has_key(name) and not self.current.has_field(name):
            self.current.set_field(name,[])
        else:
            if self.ign_elems.has_key(name):
                self.ignoring=self.ignoring+1

        self.cur_data=""

    def characters(self,data,start,length):
        if self.ignoring or self.current==None:
            return

        data=data[start:start+length]
        mo=reg_ws.match(data)
        if mo!=None and mo.end(0)==len(data):
            return

        self.cur_data=self.cur_data+data

    def endElement(self,name):
        if self.ign_elems.has_key(name):
            self.ignoring=self.ignoring-1
            return

        if self.ignoring or self.current==None:
            return

        if name==self.target_elem:
            self.objects.append(self.current)
            self.current=None
        elif self.list_elems.has_key(name):
            obj=self.current
            self.current=self.stack[-1]
            del self.stack[-1]
            self.current.get_field(name).append(obj)
        elif self.rep_field.has_key(name):
            self.current.get_field(name).append(self.cur_data)
        else:
            self.current.set_field(name,self.cur_data)

    def get_objects(self):
        return self.objects

def make_objects(url,element,list_elems={},ign_elems={},rep_field={}):
    dh=DocHandler(element,list_elems,ign_elems,rep_field)
    eh=saxutils.ErrorPrinter()

    parser=saxexts.make_parser()
    parser.setDocumentHandler(dh)
    parser.setErrorHandler(eh)
    parser.parse(url)

    return dh.get_objects()

def make_xml(filename,root_elem,trgt_elem,list):
    out=open(filename,"w")
    out.write("<%s>\n" % root_elem)

    for obj in list:
        out.write("  <%s>\n" % trgt_elem)
        for field in obj.get_fields():
            out.write("    <%s>%s</%s>\n" % \
                      (field,escape_markup(obj.get_field(field)),field))
        out.write("  </%s>\n" % trgt_elem)

    out.write("\n</%s>" % root_elem)
    out.close()

def list2hash(lst,key_field):
    hash={}

    for obj in lst:
        hash[obj.get_field(key_field)]=obj

    return hash

def escape_markup(str):
    out=""

    for ch in str:
        if ch=="<":
            out=out+"&lt;"
        elif ch==">":
            out=out+"&gt;"
        else:
            out=out+ch

    return out
