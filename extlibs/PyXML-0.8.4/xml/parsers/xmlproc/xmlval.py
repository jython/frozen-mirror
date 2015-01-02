"""This is the parts of xmlproc that are specific to validation. They
are an application class that receive data from the parser and a
subclass of the parser object that sets this up.

$Id: xmlval.py,v 1.16 2002/07/17 17:43:14 mikeolson Exp $
"""

import urlparse,os,anydbm,string,cPickle,time

from xmlproc import *
from xmldtd import *
from xmlapp import *

# ==============================
# The validator class
# ==============================

class XMLValidator:
    """XML parser that validates a document and does some of what is required
    of a validating parser, like adding fixed and default attribute values
    etc."""

    def __init__(self):
        self.parser=XMLProcessor()
        self.app=Application()
        self.dtd=CompleteDTD(self.parser)
        self.val=ValidatingApp(self.dtd,self.parser)
        self.reset()

    def parse_resource(self,sysid):
        self.parser.parse_resource(sysid)

    def reset(self):
        self.dtd.reset()
        self.val.reset()

        self.parser.reset()
        self.parser.set_application(self.val)
        self.parser.dtd=self.dtd
        self.parser.ent=self.dtd
        self.parser.set_read_external_subset(1)

    def feed(self,data):
        self.parser.feed(data)

    def close(self):
        self.parser.close()

    def deref(self):
        self.parser.deref()

    def set_application(self,app):
        self.app=app
        self.val.set_real_app(self.app)
        app.set_locator(self.parser)

    def set_error_language(self,language):
        self.parser.set_error_language(language)

    def set_error_handler(self,err):
        self.parser.set_error_handler(err)

    def set_dtd_listener(self,dtd_listener):
        self.parser.set_dtd_listener(dtd_listener)

    def set_inputsource_factory(self,isf):
        self.parser.set_inputsource_factory(isf)

    def set_pubid_resolver(self,pubres):
        self.val.set_pubid_resolver(pubres)
        self.parser.set_pubid_resolver(pubres)

    def set_data_after_wf_error(self,stop_on_wf=0):
        self.parser.set_data_after_wf_error(stop_on_wf)

    def set_sysid(self, sysid):
        self.parser.set_sysid(sysid)

    def set_read_external_subset(self,read_it):
        pass # This parser always reads it

    def get_dtd(self):
        return self.dtd

    def get_current_sysid(self):
        return self.parser.get_current_sysid()

    def get_offset(self):
        return self.parser.get_offset()

    def get_line(self):
        return self.parser.get_line()

    def get_column(self):
        return self.parser.get_column()

    def parseStart(self):
        self.parser.parseStart()

    def parseEnd(self):
        self.parser.parseEnd()

    def read_from(self,file,bufsize=16384):
        self.parser.read_from(file,bufsize)

    def flush(self):
        self.parser.flush()

    def report_error(self,errno,args=None):
        self.parser.report_error(errno,args)

    # ===== The introspection methods =====

    def get_elem_stack(self):
        "Returns the internal element stack. Note: this is a live list!"
        return self.parser.stack

    def get_data_buffer(self):
        "Returns the current data buffer."
        return self.parser.data

    def get_construct_start(self):
        """Returns the start position of the current construct (tag, comment,
        etc)."""
        return self.parser.prepos

    def get_construct_end(self):
        """Returns the end position of the current construct (tag, comment,
        etc)."""
        return self.parser.pos

    def get_raw_construct(self):
        "Returns the raw form of the current construct."
        return self.parser.data[self.parser.prepos:self.parser.pos]

    def get_current_ent_stack(self):
        """Returns a snapshot of the entity stack. A list of the system
        identifier of the entity and its name, if any."""
        return map(lambda ent: (ent[0],ent[9]),self.parser.ent_stack)

# ==============================
# Application object that checks the document
# ==============================

class ValidatingApp(Application):
    "The object that uses the DTD to actually validate XML documents."

    def __init__(self,dtd,parser):
        self.dtd=dtd
        self.parser=parser
        self.realapp=Application()
        self.pubres=PubIdResolver()
        self.reset()

    def reset(self):
        self.cur_elem=None
        self.cur_state=0
        self.stack=[]
        self.ids={}
        self.idrefs=[]
        self._seen_root = 0

    def set_real_app(self,app):
        self.realapp=app

    def set_pubid_resolver(self,pubres):
        self.pubres=pubres

    def set_locator(self,locator):
        Application.set_locator(self,locator)
        self.realapp.set_locator(locator)

    def handle_start_tag(self,name,attrs):
	decl_root = self.dtd.get_root_elem()
	
	if self.cur_elem != None:
            if self.cur_state != -1:
                next = self.cur_elem.next_state(self.cur_state, name)
                if next == 0:
                    # try to infer missing element
                    skip = self.cur_elem.next_state_skip(self.cur_state, name)
                    if skip:
                        # success: give improved error message
                        self.parser.report_error(2025, (skip[1], name))
                        self.cur_state = skip[0]
                    else:
                        # failed; give generic error message
                        self.parser.report_error(2001, name)
                else:
                    self.cur_state = next

	    self.stack.append((self.cur_elem, self.cur_state))
            
	elif (not self._seen_root) and decl_root != None and name != decl_root:
	    self.parser.report_error(2002,name)

        self._seen_root = 1
	try:
	    self.cur_elem = self.dtd.get_elem(name)
            self.cur_state = self.cur_elem.get_start_state()
	    self.validate_attributes(self.dtd.get_elem(name), attrs)
	except KeyError:
	    self.parser.report_error(2003, name)
	    self.cur_state = -1

	self.realapp.handle_start_tag(name, attrs)
	
    def handle_end_tag(self,name):
	"Notifies the application of end tags (and empty element tags)."
	if self.cur_elem != None and \
	   not self.cur_elem.final_state(self.cur_state):

            valid = self.cur_elem.get_valid_elements(self.cur_state)
	    self.parser.report_error(2004, (name, string.join(valid, ", ")))
	
	self.realapp.handle_end_tag(name)

	if self.stack!=[]:
	    (self.cur_elem,self.cur_state)=self.stack[-1]
	    del self.stack[-1]



    def handle_data(self,data,start,end):
        "Notifies the application of character data."
        if self.cur_elem!=None and self.cur_state!=-1:
            next=self.cur_elem.next_state(self.cur_state,"#PCDATA")

            if next==0:
                self.realapp.handle_ignorable_data(data,start,end)
                for ch in data[start:end]:
                    if not ch in " \t\r\n":
                        self.parser.report_error(2005)
                        break

                return
            else:
                self.cur_state=next

        self.realapp.handle_data(data,start,end)

    def validate_attributes(self,element,attrs):
        """Validates the attributes against the element declaration and adds
        fixed and default attributes."""

	# Check the values of the present attributes
	for attr in attrs.keys():
	    try:
		decl = element.get_attr(attr)
	    except KeyError:
		self.parser.report_error(2006, attr)
                continue
        
            if decl.type!="CDATA":
                attrs[attr]=string.join(string.split(attrs[attr]))

            decl.validate(attrs[attr],self.parser)

            if decl.type=="ID":
                if self.ids.has_key(attrs[attr]):
                    self.parser.report_error(2007,attrs[attr])
                self.ids[attrs[attr]]=""
            elif decl.type=="IDREF":
                self.idrefs.append((self.locator.get_line(),
                                    self.locator.get_column(),
                                    attrs[attr]))
            elif decl.type=="IDREFS":
                for idref in string.split(attrs[attr]):
                    self.idrefs.append((self.locator.get_line(),
                                        self.locator.get_column(),
                                        idref))
            elif decl.type=="ENTITY":
                self.__validate_attr_entref(attrs[attr])
            elif decl.type=="ENTITIES":
                for ent_ref in string.split(attrs[attr]):
                    self.__validate_attr_entref(ent_ref)

        # Check for missing required attributes
        for attr in element.get_attr_list():
            decl=element.get_attr(attr)
            if decl.decl=="#REQUIRED" and not attrs.has_key(attr):
                self.parser.report_error(2010,attr)

    def __validate_attr_entref(self,name):
        try:
            ent=self.dtd.resolve_ge(name)
            if ent.notation=="":
                self.parser.report_error(2008)
            else:
                try:
                    self.dtd.get_notation(ent.notation)
                except KeyError:
                    self.parser.report_error(2009,ent.notation)
        except KeyError:
            self.parser.report_error(3021,name)

    def doc_end(self):
        for (line,col,id) in self.idrefs:
            if not self.ids.has_key(id):
                self.parser.report_error(2011,id)

        self.realapp.doc_end()

    def handle_doctype(self,rootname,pub_id,sys_id):
        self.realapp.handle_doctype(rootname,pub_id,sys_id)
        self.dtd.root_elem=rootname

    # --- These methods added only to make this hanger-on application
    #     invisible to external users.

    def doc_start(self):
        self.realapp.doc_start()

    def handle_comment(self,data):
        self.realapp.handle_comment(data)

    def handle_ignorable_data(self,data,start,end):
        self.realapp.handle_ignorable_data(data,start,end)

    def handle_pi(self,target,data):
        self.realapp.handle_pi(target,data)

    def set_entity_info(self,xmlver,enc,sddecl):
        self.realapp.set_entity_info(xmlver,enc,sddecl)
