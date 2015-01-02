"""
The main module of the parser. All other modules will be imported into this
one, so this module is the only one one needs to import. For validating
parsing, import xmlval instead.
"""

# $Id: xmlproc.py,v 1.25 2002/08/13 09:28:51 afayolle Exp $

import re,string,sys,urlparse

string_translate=string.translate # optimization. made 10% difference!
string_find     =string.find

from dtdparser import *
from xmlutils import *
from xmlapp import *
from xmldtd import *

version="0.70"
revision="$Revision: 1.25 $"

# ==============================
# A full well-formedness parser
# ==============================

class XMLProcessor(XMLCommonParser):
    "A parser that performs a complete well-formedness check."

    def __init__(self):
        EntityParser.__init__(self)

        # Various handlers
        self.app=Application()
        self.dtd=WFCDTD(self)
        self.ent=self.dtd
        self.dtd_listener=None
        self.stop_on_wf=1

    def set_application(self,app):
        "Sets the object to send data events to."
        self.app=app
        app.set_locator(self)

    def set_dtd_listener(self,listener):
        "Registers an object that listens for DTD parse events."
        self.dtd_listener=listener

    def set_data_after_wf_error(self,stop_on_wf=0):
        """Sets the parser policy on well-formedness errors. If this is set to
        0 data events are still delivered, even after well-formedness errors.
        Otherwise no more data events reach the application after such erors.
        """
        self.stop_on_wf=stop_on_wf

    def set_read_external_subset(self,read_it):
        """Tells the parser whether to read the external subset of documents
        or not."""
        self.read_external_subset=read_it

    def report_error(self,number,args=None):
        if self.stop_on_wf and number>2999:
            self.app=Application() # No more data events reported
        EntityParser.report_error(self,number,args)

    def reset(self):
        EntityParser.reset(self)
        if hasattr(self,"dtd"):
            self.dtd.reset()

        # State vars
        self.stack=[]
        self.seen_root=0
        self.seen_doctype=0
        self.seen_xmldecl=0
        self.stop_on_wf=1
        self.read_external_subset=0

    def deref(self):
        "Deletes circular references."
        self.dtd = self.ent = self.err = self.app = self.pubres = None

    def do_parse(self):
        "Does the actual parsing."
        try:
            while self.pos<self.datasize:
                self.prepos=self.pos

                if self.data[self.pos]=="<":
                    t=self.data[self.pos+1] # Optimization
                    if t=="/":
                        self.parse_end_tag()
                    elif t!="!" and t!="?":
                        self.parse_start_tag()
                    elif self.now_at("<!--"):
                        self.parse_comment(self.app)
                    elif self.now_at("<?"): # FIXME: use t and modify self.pos?
                        self.parse_pi(self.app,1)
                    elif self.now_at("<![CDATA["):
                        self.parse_cdata()
                    elif self.now_at("<!DOCTYPE"):
                        self.parse_doctype()
                    else:
                        self.report_error(3013)
                        self.scan_to(">") # Avoid endless loops
                elif self.data[self.pos]=="&":
                    if self.now_at("&#"):
                        self.parse_charref()
                    else:
                        self.pos=self.pos+1  # Skipping the '&'
                        self.parse_ent_ref()
                else:
                    self.parse_data()

        except IndexError, e:
            # Means self.pos was outside the buffer when we did a raw
            # compare.  This is both a little ugly and fragile to
            # changes, but this loop is rather time-critical, so we do
            # raw compares anyway.
            # Should try to lose this since it gets very hard to find
            # problems if the user throws an IndexError...

            if self.final:
                raise OutOfDataException()
            else:
                self.pos=self.prepos  # Didn't complete the construct
        except OutOfDataException, e:
            if self.final:
                raise e
            else:
                self.pos=self.prepos  # Didn't complete the construct

    def parseStart(self):
        "Must be called before parsing starts. (Notifies application.)"
        self.app.doc_start()

    def parseEnd(self):
        """Must be called when parsing is finished. (Does some checks and "
        "notifies the application.)"""
        if self.stack!=[] and self.ent_stack==[]:
            self.report_error(3014,self.stack[-1])
        elif not self.seen_root:
            self.report_error(3015)

        self.app.doc_end()

    def parse_start_tag(self):
        "Parses the start tag."
        self.pos=self.pos+1 # Skips the '<'
        name=self._get_name()
        self.skip_ws()

        try:
            (attrs,fixeds)=self.dtd.attrinfo[name]
            attrs=attrs.copy()
        except KeyError:
            attrs={}
            fixeds={}

        if self.data[self.pos]!=">" and self.data[self.pos]!="/":
            seen={}
            while not self.test_str(">") and not self.test_str("/>"):
                a_name=self._get_name()
                self.skip_ws()
                if not self.now_at("="):
                    self.report_error(3005,"=")
                    self.scan_to(">") ## Panic! Get out of the tag!
                    a_val=""
                    break
                self.skip_ws()

                a_val=self.parse_att_val()
                if a_val==-1:
                    # WF error, we've skipped the rest of the tag
                    self.pos=self.pos-1      # Lets us find the '>'
                    if self.data[self.pos-1]=="/":
                        self.pos=self.pos-1  # Gets the '/>' cases right
                    break

                if seen.has_key(a_name):
                    self.report_error(3016,a_name)
                else:
                    seen[a_name]=1

                attrs[a_name]=a_val
                if fixeds.has_key(a_name) and fixeds[a_name]!=a_val:
                    self.report_error(2000,a_name)
                self.skip_ws()

        # --- Take care of the tag

        if self.stack==[] and self.seen_root:
            self.report_error(3017)

        self.seen_root=1

        if self.now_at(">"):
            self.app.handle_start_tag(name,attrs)
            self.stack.append(name)
        elif self.now_at("/>"):
            self.app.handle_start_tag(name,attrs)
            self.app.handle_end_tag(name)
        else:
            self.report_error(3004,("'>'","/>"))

    def parse_att_val(self):
        "Parses an attribute value and resolves all entity references in it."

        val=""
        if self.now_at('"'):
            delim='"'
            reg_attval_stop=reg_attval_stop_quote
        elif self.now_at("'"):
            delim="'"
            reg_attval_stop=reg_attval_stop_sing
        else:
            self.report_error(3004,("'","\""))
            self.scan_to(">")
            return -1 # FIXME: Ugly. Should throw an exception instead

        while 1:
            piece=self.find_reg(reg_attval_stop)
            val=val+ws_trans(piece)

            if self.now_at(delim):
                break

            if self.now_at("&#"):
                val=val+self._read_char_ref()
            elif self.now_at("&"):
                name=self._get_name()

                if name in self.open_ents:
                    self.report_error(3019)
                    return
                else:
                    self.open_ents.append(name)

                try:
                    ent=self.ent.resolve_ge(name)
                    if ent.is_internal():
                        # Doing all this here sucks a bit, but...
                        self.push_entity(self.get_current_sysid(),\
                                         ent.value,name)

                        self.final=1 # Only one block

                        val=val+self.parse_literal_entval()
                        if not self.pos==self.datasize:
                            self.report_error(3001) # Thing started, not compl

                        self.pop_entity()
                    else:
                        self.report_error(3020)
                except KeyError:
                    self.report_error(3021,name) ## FIXME: Check standalone dcl

                del self.open_ents[-1]

            elif self.now_at("<"):
                self.report_error(3022)
                continue
            else:
                self.report_error(4001)
                self.pos=self.pos+1    # Avoid endless loop
                continue

            if not self.now_at(";"):
                self.report_error(3005,";")

        return val

    def parse_literal_entval(self):
        "Parses a literal entity value for insertion in an attribute value."

        val=""
        reg_stop=re.compile("&")

        while 1:
            try:
                piece=self.find_reg(reg_stop)
            except OutOfDataException:
                # Only character data left
                val=val+ws_trans(self.data[self.pos:])
                self.pos=self.datasize
                break

            val=val+ws_trans(piece)

            if self.now_at("&#"):
                val=val+self._read_char_ref()
            elif self.now_at("&"):
                name=self._get_name()

                if name in self.open_ents:
                    self.report_error(3019)
                    return ""
                else:
                    self.open_ents.append(name)

                try:
                    ent=self.ent.resolve_ge(name)
                    if ent.is_internal():
                        # Doing all this here sucks a bit, but...
                        self.push_entity(self.get_current_sysid(),\
                                         ent.value,name)

                        self.final=1 # Only one block

                        val=val+self.parse_literal_entval()
                        if not self.pos==self.datasize:
                            self.report_error(3001)

                        self.pop_entity()
                    else:
                        self.report_error(3020)
                except KeyError:
                    self.report_error(3021,name)

                del self.open_ents[-1]

            else:
                self.report_error(4001)

            if not self.now_at(";"):
                self.report_error(3005,";")
                self.scan_to(">")

        return val

    def parse_end_tag(self):
        "Parses the end tag from after the '</' and beyond '>'."
        self.pos=self.pos+2 # Skips the '</'
        name=self._get_name()

        if self.data[self.pos]!=">":
            self.skip_ws() # Probably rare to find whitespace here
            if not self.now_at(">"): self.report_error(3005,">")
        else:
            self.pos=self.pos+1

	try:
            elem = self.stack[-1]
            if name != elem:
		self.report_error(3023,(name,elem))

                # Let's do some guessing in case we continue
                if len(self.stack)>0 and self.stack[-1]==name:
                    del self.stack[-1]
                else:
                    self.stack.append(elem) # Put it back
            else:
                del self.stack[-1]

        except IndexError:
            self.report_error(3024,name)

        self.app.handle_end_tag(name)

    def parse_data(self):
        "Parses character data."
        start=self.pos
        end=string_find(self.data,"<",self.pos)
        if end==-1:
            end=string_find(self.data,"&",self.pos)

            if end==-1:
                if not self.final:
                    raise OutOfDataException()

                end=self.datasize
        else:
            ampend=string_find(self.data,"&",self.pos,end)
            if ampend!=-1:
                end=ampend

        self.pos=end

        if string_find(self.data,"]]>",start,end)!=-1:
            self.pos=string_find(self.data,"]]>",start,end)
            self.report_error(3025)
            self.pos=self.pos+3 # Skipping over it

        if self.stack==[]:
            res=reg_ws.match(self.data,start)
            if res==None or res.end(0)!=end:
                self.report_error(3029)
        else:
            self.app.handle_data(self.data,start,end)

    def parse_charref(self):
        "Parses a character reference."
        if self.now_at("x"):
            digs=unhex(self.get_match(reg_hex_digits))
        else:
            try:
                digs=int(self.get_match(reg_digits))
            except ValueError:
                self.report_error(3027)
                digs=None

        if not self.now_at(";"): self.report_error(3005,";")
        if digs==None: return

        if not (digs==9 or digs==10 or digs==13 or \
                (digs>=32 and digs<=255)):
            if digs>255:
                if using_unicode and digs<65536:
                    self.app.handle_data(xml_chr(digs),0,1)
                else:
                    self.report_error(1005,digs)
            else:
                self.report_error(3018,digs)
        else:
            if self.stack==[]:
                self.report_error(3028)
            self.app.handle_data(xml_chr(digs),0,1)

    def parse_cdata(self):
        "Parses a CDATA marked section from after the '<![CDATA['."
        new_pos=self.get_index("]]>")
        if self.stack==[]:
            self.report_error(3029)
        self.app.handle_data(self.data,self.pos,new_pos)
        self.pos=new_pos+3

    def parse_ent_ref(self):
        "Parses a general entity reference from after the '&'."
        name=self._get_name()
        if not self.now_at(";"): self.report_error(3005,";")

        try:
            ent=self.ent.resolve_ge(name)
        except KeyError:
            self.report_error(3021,name)
            return

        if ent.name in self.open_ents:
            self.report_error(3019)
            return

        self.open_ents.append(ent.name)

        if self.stack==[]:
            self.report_error(3030)

        # Storing size of current element stack
        stack_size=len(self.stack)

        if ent.is_internal():
            self.push_entity(self.get_current_sysid(),ent.value,name)
            try:
                self.do_parse()
            except OutOfDataException: # Ran out of data before done
                self.report_error(3001)

            self.flush()
            self.pop_entity()
        else:
            if ent.notation != None:
                self.report_error(3031)
            else:
                self.seen_root = 0    # Haven't seen root in the new entity yet
                self.open_entity(self.pubres.resolve_entity_pubid(ent.get_pubid(),
                                                                  ent.get_sysid()),
                                 name)
                self.seen_root = 1

        # Did any elements cross the entity boundary?
        if stack_size != len(self.stack):
            self.report_error(3042)

        del self.open_ents[-1]

    def parse_doctype(self):
        "Parses the document type declaration."

        if self.seen_doctype:
            self.report_error(3032)
        if self.seen_root:
            self.report_error(3033)

        self.skip_ws(1)
        rootname = self._get_name()
        self.skip_ws(1)

        (pub_id, sys_id) = self.parse_external_id()
        self.skip_ws()

        self.app.handle_doctype(rootname, pub_id, sys_id)
        self.dtd.dtd_start()

        if self.now_at("["):
            self.parse_internal_dtd()
        elif not self.now_at(">"):
            self.report_error(3005, ">")

        # External subset must be parsed _after_ the internal one
        if pub_id != None or sys_id != None: # Was there an external id at all?
            if not self.get_current_sysid() and \
               urlparse.urlparse(sys_id)[0] == "":
                self.report_error(2024, sys_id)

            if self.read_external_subset:
                p = self._setup_dtd_parser(0)
                try:
                    sys_id = self.pubres.resolve_doctype_pubid(pub_id, sys_id)
                    p.dtd_start_called = 1
                    p.parse_resource(join_sysids(self.get_current_sysid(),
                                                 sys_id))
                finally:
                    p.deref()
                    self.err.set_locator(self)

        if (pub_id == None and sys_id == None) or \
           not self.read_external_subset:
            # If we parse the external subset dtd_end is called for us by
            # the dtd parser. If we don't we must call it ourselves.
            self.dtd.dtd_end()

        self.seen_doctype=1 # Has to be at the end to avoid block trouble

    def parse_internal_dtd(self):
        "Parse the internal DTD beyond the '['."

        self.set_start_point() # Record start of int_subset, preserve data
        self.update_pos()
        line=self.line
        lb=self.last_break
        last_part_size=0

        while 1:
            self.find_reg(reg_int_dtd)

            if self.now_at("\""): self.scan_to("\"")
            elif self.now_at("'"): self.scan_to("'")
            elif self.now_at("<?"): self.scan_to("?>")
            elif self.now_at("<!--"): self.scan_to("-->")
            elif self.now_at("<!["): self.scan_to("]]>")
            elif self.now_at("]"):
                p=self.pos
                self.skip_ws()
                if self.now_at(">"):
                    last_part_size=(self.pos-p)+1
                    break

        # [:lps] cuts off the "]\s+>" at the end
        self.handle_internal_dtd(line,lb,self.get_region()[:-last_part_size])

    def handle_internal_dtd(self,doctype_line,doctype_lb,int_dtd):
        "Handles the internal DTD."
        try:
            p=self._setup_dtd_parser(1)
            try:
                p.line=doctype_line
                p.last_break=doctype_lb

                p.set_sysid(self.get_current_sysid())
                p.final=1
                p.feed(int_dtd, decoded = 1)
            except OutOfDataException:
                self.report_error(3034)
        finally:
            p.deref()
            self.err.set_locator(self)

    def _setup_dtd_parser(self, internal_subset):
        p=DTDParser()
        p.set_error_handler(self.err)
        p.set_dtd_consumer(self.dtd)
        p.set_error_language(self.err_lang)
        p.set_inputsource_factory(self.isf)
        p.set_pubid_resolver(self.pubres)
        p.set_dtd_object(self.dtd)
        if self.dtd_listener!=None:
            self.dtd.set_dtd_listener(self.dtd_listener)
        p.set_internal(internal_subset)
        self.err.set_locator(p)
        return p

    # ===== The introspection methods =====

    def get_elem_stack(self):
        "Returns the internal element stack. Note: this is a live list!"
        return self.stack

    def get_data_buffer(self):
        "Returns the current data buffer."
        return self.data

    def get_construct_start(self):
        """Returns the start position of the current construct (tag, comment,
        etc)."""
        return self.prepos

    def get_construct_end(self):
        """Returns the end position of the current construct (tag, comment,
        etc)."""
        return self.pos

    def get_raw_construct(self):
        "Returns the raw form of the current construct."
        return self.data[self.prepos:self.pos]

    def get_current_ent_stack(self):
        """Returns a snapshot of the entity stack. A list of the system
        identifier of the entity and its name, if any."""
        return map(lambda ent: (ent[0],ent[9]),self.ent_stack)
