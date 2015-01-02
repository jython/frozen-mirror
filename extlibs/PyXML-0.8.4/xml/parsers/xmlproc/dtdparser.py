"""
This module contains a DTD parser that reports DTD parse events to a listener.
Used by xmlproc to parse DTDs, but can be used for other purposes as well.

$Id: dtdparser.py,v 1.13 2002/04/13 19:10:40 larsga Exp $
"""

import string

string_find = string.find # optimization

from xmlutils import *
from xmldtd   import *

# ==============================
# A DTD parser
# ==============================

class DTDParser(XMLCommonParser):
    "A parser for XML DTDs, both internal and external."

    # --- LOW-LEVEL SCANNING METHODS
    # Redefined here with extra checking for parameter entity processing

    def find_reg(self,regexp,required=1):
        oldpos=self.pos
        mo=regexp.search(self.data,self.pos)
        if mo==None:
            if self.final and not required:
                self.pos=len(self.data)   # Just moved to the end
                return self.data[oldpos:]

            if self.in_peref:
                self.pop_entity()
                self.in_peref=0
                self._skip_ws()
                return self.find_reg(regexp,required)

            raise OutOfDataException()

        self.pos=mo.start(0)
        return self.data[oldpos:self.pos]

    def scan_to(self,target):
        new_pos=string_find(self.data,target,self.pos)
        if new_pos==-1:
            if self.in_peref:
                self.pop_entity()
                self.in_peref=0
                self._skip_ws()
                return self.scan_to(target)
            raise OutOfDataException()
        res=self.data[self.pos:new_pos]
        self.pos=new_pos+len(target)
        return res

    def get_index(self,target):
        new_pos=string_find(self.data,target,self.pos)
        if new_pos==-1:
            if self.in_peref:
                self.pop_entity()
                self.in_peref=0
                self._skip_ws()
                return self.get_index(target)
            raise OutOfDataException()
        return new_pos

    def test_str(self,str):
        if self.datasize-self.pos<len(str) and not self.final:
            if self.in_peref:
                self.pop_entity()
                self.in_peref=0
                self._skip_ws()
                return self.test_str(str)
            raise OutOfDataException()
        return self.data[self.pos:self.pos+len(str)]==str

    def now_at(self,test_str):
        if self.datasize-self.pos<len(test_str) and not self.final:
            if self.in_peref:
                self.pop_entity()
                self.in_peref=0
                self._skip_ws()
                return self.now_at(test_str)
            raise OutOfDataException()

        if self.data[self.pos:self.pos+len(test_str)]==test_str:
            self.pos=self.pos+len(test_str)
            return 1
        else:
            return 0

    def _skip_ws(self,necessary=0):
        start=self.pos

        try:
            while self.data[self.pos] in whitespace:
                self.pos=self.pos+1

            if necessary and self.pos==start and self.data[self.pos]!="%":
                self.report_error(3002)
        except IndexError:
            if self.in_peref:
                self.pop_entity()
                self.in_peref=0
                self._skip_ws()
                return

            if necessary and start==self.pos:
                if self.final:
                    self.report_error(3002)
                else:
                    raise OutOfDataException()

    def skip_ws(self,necessary=0):
        self._skip_ws(necessary)
        if not self.internal:
            try:
                if not self.now_at("%"):
                    return
            except OutOfDataException:
                return

            name=self._get_name()

            if not self.now_at(";"):
                self.report_error(3005,";")

            try:
                ent=self.dtd.resolve_pe(name)
            except KeyError:
                self.report_error(3038,name)
                return

            if ent.is_internal():
                self.in_peref=1
                self.push_entity(self.get_current_sysid(),ent.value)
                self.final=1  # Reset by pop_ent, needed for buffer handling
            else:
                self.report_error(4003)

            # At this point we need to try again, since the entity we just
            # tried may have contained only whitespace (or nothing at all).
            # Using self._skip_ws() makes us fail when an empty PE is followed
            # by a non-empty one. (DocBook has examples of this.)
            self.skip_ws()

    def test_reg(self,regexp):
        if self.pos>self.datasize-5 and not self.final:
            if self.in_peref:
                self.pop_entity()
                self.in_peref=0
                self._skip_ws()
                return self.test_reg(regexp)
            raise OutOfDataException()

        return regexp.match(self.data,self.pos)!=None

    def get_match(self,regexp):
        if self.pos>self.datasize-5 and not self.final:
            if self.in_peref:
                self.pop_entity()
                self.in_peref=0
                self._skip_ws()
                return self.get_match(regexp)
            raise OutOfDataException()

        ent=regexp.match(self.data,self.pos)
        if ent==None:
            self.report_error(reg2code[regexp.pattern])
            return ""

        end=ent.end(0) # Speeds us up slightly
        if end==self.datasize:
            if self.in_peref:
                self.pop_entity()
                self.in_peref=0
                #self._skip_ws()
                return ent.group(0)
            raise OutOfDataException()

        self.pos=end
        return ent.group(0)

    # --- DTD Parser proper

    def __init__(self):
        EntityParser.__init__(self)
        self.internal=0
        self.seen_xmldecl=0
        self.dtd=DTDConsumerPE()            # Keeps track of PE info
        self.dtd_consumer=self.dtd          # Where all events go
        self.in_peref=0
        self.ignores_entered=0
        self.includes_entered=0
        self.own_ent_stack=[]               # Keeps includes_entered

    def reset(self):
        EntityParser.reset(self)
        if hasattr(self,"dtd"):
            self.dtd.reset()

        self.internal=0
        self.seen_xmldecl=0
        self.in_peref=0
        self.ignores_entered=0
        self.includes_entered=0
        self.own_ent_stack=[]      # Keeps includes_entered
        self.dtd_start_called = 0  # Set to 1 if parsing external subset from
                                   # xmlproc.py (which has called dtd_start...)

    def parseStart(self):
        if not self.dtd_start_called:
            self.dtd_consumer.dtd_start()

    def parseEnd(self):
        self.dtd_consumer.dtd_end()

    def set_dtd_consumer(self,dtd):
        "Tells the parser where to send DTD information."
        self.dtd_consumer=dtd

    def set_dtd_object(self,dtd):
        """Tells the parser where to mirror PE information (in addition to
        what goes to the DTD consumer and where to get PE information."""
        self.dtd=dtd

    def set_internal(self,yesno):
        "Tells the parser whether the DTD is internal or external."
        self.internal=yesno

    def deref(self):
        "Removes circular references."
        self.ent = self.dtd_consumer = self.dtd = self.app = self.err = None

    def do_parse(self):
        "Does the actual parsing."

        try:
            prepos=self.pos

            if self.ignores_entered>0:
                self.parse_ignored_data()

            self._skip_ws()
            while self.pos<self.datasize:
                if self.now_at("<!ELEMENT"):
                    self.parse_elem_type()
                elif self.now_at("<!ENTITY"):
                    self.parse_entity()
                elif self.now_at("<!ATTLIST"):
                    self.parse_attlist()
                elif self.now_at("<!NOTATION"):
                    self.parse_notation()
                elif self.test_reg(reg_pe_ref):
                    self.parse_pe_ref()
                elif self.now_at("<?"):
                    self.parse_pi(self.dtd_consumer)
                elif self.now_at("<!--"):
                    self.parse_comment(self.dtd_consumer)
                elif self.now_at("<!["):
                    self.parse_conditional()
                elif self.now_at("]]>") and self.includes_entered>0:
                    self.includes_entered=self.includes_entered-1
                else:
                    self.report_error(3013)
                    self.scan_to(">")

                prepos=self.pos
                self._skip_ws()

            if self.final and self.includes_entered>0:
                self.report_error(3043)

        except OutOfDataException,e:
            if self.final:
                raise e
            else:
                self.pos=prepos
        except IndexError,e:
            if self.final:
                raise OutOfDataException()
            else:
                self.pos=prepos

    def parse_entity(self):
        "Parses an entity declaration."

        EntityParser.skip_ws(self,1) # No PE refs allowed here
        if self.now_at("%"):
            pedecl=1
            EntityParser.skip_ws(self,1) # No PE refs allowed here
        else:
            pedecl=0

        ent_name=self._get_name()
        self.skip_ws(1)

        (pub_id,sys_id)=self.parse_external_id(0)

        if sys_id == None:
            internal = 1
            ent_val = self.parse_ent_repltext()
        else:
            internal = 0
            if not self.get_current_sysid() and \
               urlparse.urlparse(sys_id)[0] == "":
                self.report_error(2024, sys_id)
            sys_id = join_sysids(self.get_current_sysid(), sys_id)

        if self.now_at("NDATA"):
            self.report_error(3002)
        else:
            self.skip_ws()

        if not internal and self.now_at("NDATA"):
            # Parsing the optional NDataDecl
            if pedecl:
                self.report_error(3035)
            self.skip_ws()

            ndata=self._get_name()
            self.skip_ws()
        else:
            ndata = None

        if not self.now_at(">"):
            self.report_error(3005,">")

        if pedecl:
            # These are echoed to self.dtd so we remember this stuff
            if internal:
                self.dtd_consumer.new_parameter_entity(ent_name,ent_val)
                if self.dtd!=self.dtd_consumer:
                    self.dtd.new_parameter_entity(ent_name,ent_val)
            else:
                self.dtd_consumer.new_external_pe(ent_name,pub_id,sys_id)
                if self.dtd!=self.dtd_consumer:
                    self.dtd.new_external_pe(ent_name,pub_id,sys_id)
        else:
            if internal:
                self.dtd_consumer.new_general_entity(ent_name,ent_val)
            else:
                self.dtd_consumer.new_external_entity(ent_name,pub_id,sys_id,ndata)

    def parse_ent_repltext(self):
        """Parses an entity replacement text and resolves all character
        entity and parameter entity references in it."""

        if self.now_at('"'):
            delim = '"'
        elif self.now_at("'"):
            delim = "'"
        else:
            self.report_error(3004,("'","\""))
            self.scan_to(">")
            return

        return self.parse_ent_litval(self.scan_to(delim))

    def parse_ent_litval(self,litval):
        pos=0
        val=""

        while 1:
            res=reg_litval_stop.search(litval,pos)

            if res==None:
                break

            val=val+litval[pos:res.start(0)]
            pos=res.start(0)

            if litval[pos:pos+2]=="&#":
                endpos=string_find(litval,";",pos)
                if endpos==-1:
                    self.report_error(3005,";")
                    break

                if litval[pos+2]=="x":
                    digs=unhex(litval[pos+3:endpos])
                else:
                    digs=int(litval[pos+2:endpos])

                if not (digs==9 or digs==10 or digs==13 or \
                        (digs>=32 and digs<=255)):
                    if digs>255:
                        if using_unicode and digs<65536:
                            val = val+xml_chr(digs)
                        else:
                            self.report_error(1005,digs)
                    else:
                        self.report_error(3018,digs)
                else:
                    val=val+xml_chr(digs)

                pos=endpos+1
            elif litval[pos]=="%":
                endpos=string_find(litval,";",pos)
                if endpos==-1:
                    self.report_error(3005,";")
                    break

                name=litval[pos+1:endpos]
                try:
                    ent=self.dtd.resolve_pe(name)
                    if ent.is_internal():
                        val=val+self.parse_ent_litval(ent.value)
                    else:
                        self.report_error(3037) # FIXME: Easily solved now...?
                except KeyError:
                    self.report_error(3038,name)

                pos=endpos+1
            else:
                self.report_error(4001)
                break

        return val+litval[pos:]

    def parse_notation(self):
        "Parses a notation declaration."
        self.skip_ws(1)
        name=self._get_name()
        self.skip_ws(1)

        (pubid,sysid)=self.parse_external_id(1,0)
        self.skip_ws()
        if not self.now_at(">"):
            self.report_error(3005,">")

        self.dtd_consumer.new_notation(name,pubid,sysid)

    def parse_pe_ref(self):
        "Parses a reference to a parameter entity."
        name=self.get_match(reg_pe_ref)[1:-1]

        try:
            ent=self.dtd.resolve_pe(name)
        except KeyError:
            self.report_error(3038,name)
            return

        if ent.is_internal():
            self.push_entity(self.get_current_sysid(),ent.value)
            self.do_parse()
            self.pop_entity()
        else:
            sysid=self.pubres.resolve_pe_pubid(ent.get_pubid(),
                                               ent.get_sysid())
            int=self.internal
            self.set_internal(0)
            try:
                self.open_entity(sysid) # Does parsing and popping
            finally:
                self.set_internal(int)

    def parse_attlist(self):
        "Parses an attribute list declaration."

        self.skip_ws(1)
        elem=self._get_name()
        self.skip_ws(1)

        while not self.test_str(">"):
            attr=self._get_name()
            self.skip_ws(1)

            if self.test_reg(reg_attr_type):
                a_type=self.get_match(reg_attr_type)
            elif self.now_at("NOTATION"):
                self.skip_ws(1)
                a_type=("NOTATION",self.__parse_list(reg_name,"|"))
            elif self.now_at("("):
                self.pos=self.pos-1 # Does not expect '(' to be skipped
                a_type=self.__parse_list(reg_nmtoken,"|")

                tokens={}
                for token in a_type:
                    if tokens.has_key(token):
                        self.report_error(3044,(token,))
                    else:
                        tokens[token]=1
            else:
                self.report_error(3039)
                self.scan_to(">")
                return

            self.skip_ws(1)

            if self.test_str("\"") or self.test_str("'"):
                a_decl="#DEFAULT"
                a_def=self.parse_ent_repltext()
            elif self.now_at("#IMPLIED"):
                a_decl="#IMPLIED"
                a_def=None
            elif self.now_at("#REQUIRED"):
                a_decl="#REQUIRED"
                a_def=None
	    elif self.now_at("#FIXED"):
		self.skip_ws(1)
		a_decl = "#FIXED"
		a_def = self.parse_ent_repltext()
	    else:
                self.report_error(3909)
                a_decl = None
                a_def = None

            self.skip_ws()
            self.dtd_consumer.new_attribute(elem,attr,a_type,a_decl,a_def)

        self.pos=self.pos+1 # Skipping the '>'

    def parse_elem_type(self):
        "Parses an element type declaration."

        self.skip_ws(1)
        #elem_name=self.get_match(reg_name)
        elem_name=self._get_name()
        self.skip_ws(1)

        # content-spec
        if self.now_at("EMPTY"):
            elem_cont="EMPTY"
        elif self.now_at("ANY"):
            elem_cont="ANY"
        elif self.now_at("("):
            elem_cont=self._parse_content_model()
        else:
            self.report_error(3004,("EMPTY, ANY","("))
            elem_cont="ANY" # Just so things don't fall apart downstream

        self.skip_ws()
        if not self.now_at(">"):
            self.report_error(3005,">")

        self.dtd_consumer.new_element_type(elem_name,elem_cont)

    def _parse_content_model(self,level=0):
        """Parses the content model of an element type declaration. Level
        tells the function if we are on the top level (=0) or not (=1).
        The '(' has just been passed over, we read past the ')'. Returns
        a tuple (separator, contents, modifier), where content consists
        of (cp, modifier) tuples and cp can be a new content model tuple."""

        self.skip_ws()

        # Creates a content list with separator first
        cont_list=[]
        sep=""

        if self.now_at("#PCDATA") and level==0:
            return self.parse_mixed_content_model()

        while 1:
            self.skip_ws()
            if self.now_at("("):
                cp=self._parse_content_model(1)
            else:
                cp=self._get_name()

            if self.test_str("?") or self.test_str("*") or self.test_str("+"):
                mod=self.data[self.pos]
                self.pos=self.pos+1
            else:
                mod=""

            if type(cp) in StringTypes:
                cont_list.append((cp,mod))
            else:
                cont_list.append(cp)

            self.skip_ws()
            if self.now_at(")"):
                break

            if sep=="":
                if self.test_str("|") or self.test_str(","):
                    sep=self.data[self.pos]
                else:
                    self.report_error(3004,("'|'",","))
                self.pos=self.pos+1
            else:
                if not self.now_at(sep):
                    self.report_error(3040)
                    self.scan_to(")")

        if self.test_str("+") or self.test_str("?") or self.test_str("*"):
            mod=self.data[self.pos]
            self.pos=self.pos+1
        else:
            mod=""

        return (sep,cont_list,mod)

    def parse_mixed_content_model(self):
        "Parses mixed content models. Ie: ones containing #PCDATA."

        cont_list=[("#PCDATA","")]
        sep=""
        mod=""

        while 1:
            try:
                self.skip_ws()
            except OutOfDataException,e:
                raise e

            if self.now_at("|"):
                sep="|"
            elif self.now_at(")"):
                break
            else:
                self.report_error(3005,"|")
                self.scan_to(">")

            self.skip_ws()
            cont_list.append((self.get_match(reg_name),""))

        if self.now_at("*"):
            mod="*"
        elif sep=="|":
            self.report_error(3005,"*")

        return (sep,cont_list,mod)

    def parse_conditional(self):
        "Parses a conditional section."
        if self.internal:
            self.report_error(3041)
            self.scan_to("]]>")
        else:
            self.skip_ws()

            if self.now_at("IGNORE"):
                self.ignores_entered=1
                self.skip_ws()
                if not self.now_at("["):
                    self.report_error(3005,"[")
                self.parse_ignored_data()
                return

            if not self.now_at("INCLUDE"):
                self.report_error(3004,("'IGNORE'","INCLUDE"))
                self.scan_to("[")
                self.includes_entered=self.includes_entered+1

            self.skip_ws()
            if not self.now_at("["):
                self.report_error(3005,"[")

            # Doing an extra skip_ws and waiting until we get here
            # before increasing the include count, to avoid increasing
            # the count inside a PE, where it would be forgotten after pop.
            self.skip_ws()
            self.includes_entered=self.includes_entered+1

    def parse_ignored_data(self):
        try:
            counter=self.ignores_entered
            while counter:
                self.find_reg(reg_cond_sect)
                if self.now_at("]]>"):
                    counter=counter-1
                else:
                    counter=counter+1
                    self.pos=self.pos+3

        except OutOfDataException,e:
            if self.final:
                self.report_error(3043)

            self.ignores_entered=counter
            self.data=""
            self.pos=0
            self.datasize=0
            raise e

        self.ignores_entered=0

    def __parse_list(self, elem_regexp, separator):
        "Parses a '(' S? elem_regexp S? separator ... ')' list. (Internal.)"

        list=[]
        self.skip_ws()
        if not self.now_at("("):
            self.report_error(3005,"(")

        while 1:
            self.skip_ws()
            list.append(self.get_match(elem_regexp))
            self.skip_ws()
            if self.now_at(")"):
                break
            elif not self.now_at(separator):
                self.report_error(3004,("')'",separator))
                break

        return list

    def is_external(self):
        return not self.internal

    # --- Internal methods

    def _push_ent_stack(self,name="None"):
        EntityParser._push_ent_stack(self,name)
        self.own_ent_stack.append(self.includes_entered)
        self.includes_entered=0

    def _pop_ent_stack(self):
        EntityParser._pop_ent_stack(self)
        self.includes_entered=self.own_ent_stack[-1]
        del self.own_ent_stack[-1]

# --- Minimal DTD consumer

class DTDConsumerPE(DTDConsumer):

    def __init__(self):
        DTDConsumer.__init__(self,None)
        self.param_ents={}
        self.used_notations = {}

    def new_parameter_entity(self,name,val):
        if not self.param_ents.has_key(name):     #Keep first decl
            self.param_ents[name]=InternalEntity(name,val)

    def new_external_pe(self,name,pubid,sysid):
        if not self.param_ents.has_key(name):     # Keep first decl
            self.param_ents[name]=ExternalEntity(name,pubid,sysid,"")

    def resolve_pe(self,name):
        return self.param_ents[name]

    def reset(self):
        self.param_ents={}
