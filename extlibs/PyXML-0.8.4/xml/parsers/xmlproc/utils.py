"""
Some utilities for use with xmlproc.

$Id: utils.py,v 1.7 2002/05/01 09:02:37 loewis Exp $
"""

import xmlapp, sys, string, types

replace = string.replace

if sys.platform[ : 4] == "java":
    from java.lang import Exception

try:
    from codecs import EncodedFile
except ImportError, e:
    # if we are on Python 1.5
    def EncodedFile(file, encoding):
        return file
    
# --- XMLParseException

class XMLParseException(Exception):
    pass


# --- ErrorPrinter

class ErrorPrinter(xmlapp.ErrorHandler):
    """An error handler that prints out warning messages."""

    def __init__(self, locator, level = 0, out = sys.stderr):
        xmlapp.ErrorHandler.__init__(self, locator)
        self.level = level
        self.out = out

    def warning(self,msg):
        if self.level < 1:
            self.out.write("WARNING: %s at %s\n" % (msg,self.__get_location()))

    def error(self,msg):
        if self.level < 2:
            self.out.write("ERROR: %s at %s\n" % (msg,self.__get_location()))

    def fatal(self,msg):
        self.out.write("ERROR: %s at %s\n" % (msg,self.__get_location()))

    def __get_location(self):
        return "%s:%d:%d" % (self.locator.get_current_sysid(),
                             self.locator.get_line(),
                             self.locator.get_column())
# --- ErrorRaiser

class ErrorRaiser(xmlapp.ErrorHandler):
    """An error handler that raises exceptions."""

    def __init__(self, locator = None, level = 0):
        xmlapp.ErrorHandler.__init__(self, locator)
        self.level = level

    def warning(self, msg):
        if self.level < 1:
            raise XMLParseException(msg)

    def error(self, msg):
        if self.level < 2:
            raise XMLParseException(msg)

    def fatal(self, msg):
        raise XMLParseException(msg)

# --- ErrorCounter

class ErrorCounter(xmlapp.ErrorHandler):
    """An error handler that counts errors."""

    def __init__(self, locator = None):
        xmlapp.ErrorHandler.__init__(self, locator)
        self.reset()

    def reset(self):
        self.warnings=0
        self.errors  =0
        self.fatals  =0

    def warning(self,msg):
        self.warnings=self.warnings+1

    def error(self,msg):
        self.errors=self.errors+1

    def fatal(self,msg):
        self.fatals=self.fatals+1

# --- ESIS document handler

class ESISDocHandler(xmlapp.Application):

    def __init__(self,writer=sys.stdout):
        self.writer=writer

    def handle_pi(self,target,data):
        self.writer.write("?"+target+" "+data+"\n")

    def handle_start_tag(self,name,amap):
        self.writer.write("("+name+"\n")
        for a_name in amap.keys():
            self.writer.write("A"+a_name+" "+amap[a_name]+"\n")

    def handle_end_tag(self,name):
        self.writer.write(")"+name+"\n")

    def handle_data(self,data,start_ix,end_ix):
        self.writer.write("-"+data[start_ix:end_ix]+"\n")

# --- XML canonizer

class Canonizer(xmlapp.Application):

    def __init__(self,writer=sys.stdout):
        self.elem_level=0
        self.writer=writer

    def handle_pi(self,target, remainder):
        if target!="xml":
            self.writer.write("<?"+target+" "+remainder+"?>")

    def handle_start_tag(self,name,amap):
        self.writer.write("<"+name)

        a_names=amap.keys()
        a_names.sort()

        for a_name in a_names:
            self.writer.write(" "+a_name+"=\"")
            self.write_data(amap[a_name])
            self.writer.write("\"")
        self.writer.write(">")
        self.elem_level=self.elem_level+1

    def handle_end_tag(self,name):
        self.writer.write("</"+name+">")
        self.elem_level=self.elem_level-1

    def handle_ignorable_data(self,data,start_ix,end_ix):
        self.write_data(data[start_ix:end_ix])

    def handle_data(self,data,start_ix,end_ix):
        if self.elem_level>0:
            self.write_data(data[start_ix:end_ix])

    def write_data(self,data):
        data=replace(data,"&","&amp;")
        data=replace(data,"<","&lt;")
        data=replace(data,"\"","&quot;")
        data=replace(data,">","&gt;")
        data=replace(data,chr(9),"&#9;")
        data=replace(data,chr(10),"&#10;")
        data=replace(data,chr(13),"&#13;")
        self.writer.write(data)

# --- DocGenerator

def escape_content(str):
    return replace(replace(str, "&", "&amp;"), "<", "&lt;")

def escape_attval(str):
    return replace(replace(replace(str, "&", "&amp;"), "<", "&lt;"), '"',
                   "&quot;")

class DocGenerator(xmlapp.Application):

    def __init__(self, out = None):
        if not out:
            self.out = EncodedFile(sys.stdout, "utf-8")
        else:
            self.out = out
    
    def handle_pi(self, target, remainder):
        self.out.write("<?%s %s?>" % (target, remainder))

    def handle_start_tag(self,name,amap):
        self.out.write("<"+name)
        for (name, value) in amap.items():
            self.out.write(' %s="%s"' % (name, escape_attval(value)))
        self.out.write(">")

    def handle_end_tag(self,name):
        self.out.write("</%s>" % name)

    def handle_ignorable_data(self,data,start_ix,end_ix):
        self.out.write(escape_content(data[start_ix:end_ix]))

    def handle_data(self,data,start_ix,end_ix):
        self.out.write(escape_content(data[start_ix:end_ix]))

# --- DictResolver

class DictResolver(xmlapp.PubIdResolver):

    def __init__(self, mapping = None):
        if mapping == None:
            mapping = {}

        self.mapping = mapping

    def resolve_pe_pubid(self, pubid, sysid):
        return self.mapping.get(pubid, sysid)

    def resolve_doctype_pubid(self, pubid, sysid):
        return self.mapping.get(pubid, sysid)

    def resolve_entity_pubid(self, pubid, sysid):
        return self.mapping.get(pubid, sysid)
    
# --- Location

class Location:

    def __init__(self, locator):
        self._sysid = locator.get_current_sysid()
        self._line = locator.get_line()
        self._column = locator.get_column()

    def get_sysid(self):
        return self._sysid

    def get_line(self):
        return self._line

    def get_column(self):
        return self._column

    def __str__(self):
        return "%s:%s:%s" % (self._sysid, self._line, self._column)
    
# --- Various DTD and validation tools

def load_dtd(sysid):
    import dtdparser,xmldtd

    dp=dtdparser.DTDParser()
    dtd=xmldtd.CompleteDTD(dp)
    dp.set_dtd_consumer(dtd)
    dp.parse_resource(sysid)

    return dtd

def validate_doc(dtd,sysid):
    import xmlval

    parser=xmlval.XMLValidator()
    parser.dtd=dtd # FIXME: what to do if there is a !DOCTYPE?
    parser.set_error_handler(ErrorPrinter(parser))
    parser.parse_resource(sysid)

    #dtd.rollback_changes()
