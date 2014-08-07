"""
This is an experimental implementation of the XPointer locator language.

Version 0.20 - 23.Aug.98
   Lars Marius Garshol - larsga@ifi.uio.no
   http://www.stud.ifi.uio.no/~larsga/download/python/xml/xptr.html

Changes since version 0.10:
 - 'id' locator term implemented
 - 'attr' locator term implemented
 - node type qualifiers implemented
 - 'origin' locator term implemented

Modified by Uche Ogbuji 25.Jan.99 to work with 4DOM.
Modified by Uche Ogbuji 18.Nov.99 to work with the emerging Python/DOM binding 4DOM.  Distributed with permission.
"""

import re,string,sys
from xml.dom import Node
from xml.dom import ext

# Spec deviations:
# - html keyword not supported
# - negative instance numbers not supported
# - #cdata node type selector not supported
# - * for attribute values/names not supported
# - preceding keyword not supported
# - span keyword unsupported
# - support 'string' location terms

# Spec questions
# - what if locator fails?
# - what to do with "span(...).child(1)"?
# - how to continue from a set of selected nodes?
# - attr: error if does not use element as source?
# - should distinguish between semantic errors and failures?
# - can string terms locate inside attr vals?
# - are the string loc semantics a bit extreme? perhaps restrict to one node?
# - how to represent span and string results in terms of the DOM?

# Global variables

version="0.20"
specver="WD-xptr-19980303"

# Useful regular expressions

reg_sym=re.compile("[a-z]+|\\(|\\)|\\.|[-+]?[1-9][0-9]*|[A-Za-z_:][\-A-Za-z_:.0-9]*|,|#[a-z]+|\\*|\"[^\"]*\"|'[^']*'")
reg_sym_param=re.compile(",|\)|\"|'")
reg_name=re.compile("[A-Za-z_:][\-A-Za-z_:.0-9]*")

# Some exceptions

class XPointerException(Exception):
    "Means something went wrong when attempting to follow an XPointer."
    pass

class XPointerParseException(XPointerException):
    "Means the XPointer was syntactically invalid."

    def __init__(self,msg,pos):
        self.__msg=msg
        self.__pos=pos

    def get_pos(self):
        return self.__pos

    def __str__(self):
        return self.__msg % self.__pos

class XPointerFailedException(XPointerException):
    "Means the XPointer was logically invalid."
    pass

class XPointerUnsupportedException(XPointerException):
    "Means the XPointer used unsupported constructs."
    pass

# Simple XPointer lexical analyzer

class SymbolGenerator:
    "Chops XPointers up into distinct symbols."

    def __init__(self,xpointer):
        self.__data=xpointer
        self.__pos=0
        self.__last_was_param=0
        self.__next_is=""

    def get_pos(self):
        "Returns the current position in the string."
        return self.__pos

    def more_symbols(self):
        "True if there are more symbols in the XPointer."
        return self.__pos<len(self.__data) or self.__next_is!=""

    def next_symbol(self):
        "Returns the next XPointer symbol."
        if self.__next_is!="":
            tmp=self.__next_is
            self.__next_is=""
            return tmp

        if self.__last_was_param:
            self.__last_was_param=0
            sym=""
            count=0

            while self.more_symbols():
                n=self.next_symbol()
                if n=='"' or n=="'":
                    pos=string.find(self.__data,n,self.__pos)
                    if pos==-1:
                        raise XPointerParseException("Unmatched %s at %d" % \
                                                     n,self.__pos)
                    sym=self.__data[self.__pos-1:pos+1]
                    self.__pos=pos+1
                elif n=="(":
                    count=count+1
                elif n==")":
                    count=count-1
                    if count<0:
                        if sym=="":
                            return ")"
                        else:
                            self.__next_is=")"
                            return sym
                elif n=="," and count==0:
                    self.__last_was_param=1
                    self.__next_is=","
                    return sym

                sym=sym+n

        mo=reg_sym.match(self.__data,self.__pos)
        if mo==None:
            raise XPointerParseException("Invalid symbol at position %d",
                                         self.__pos)

        self.__pos=self.__pos+len(mo.group(0))

        self.__last_was_param= mo.group(0)=="("
        return mo.group(0)

# Simple XPointer parser

class XPointerParser:
    """Simple XPointer parser that parses XPointers firing events that receive
    terms and parameters."""

    def __init__(self,xpointer):
        self.__sgen=SymbolGenerator(xpointer)
        self.__first_term=1
        self.__prev=None

    def __skip_over(self,symbol):
        if self.__sgen.next_symbol()!=symbol:
            raise XPointerParseException("Expected '"+symbol+"' at %s",
                                         self.__sgen.get_pos())

    def __is_valid(self,symbol,regexp):
        mo=regexp.match(symbol)
        return mo!=None and len(mo.group(0))==len(symbol)

    def __parse_instance_or_all(self,iora):
        if iora!="all":
            try:
                return int(iora)
            except ValueError,e:
                raise XPointerParseException("Expected number or 'all' at %s",
                                             self.__sgen.get_pos())
        else:
            return "all"

    def parse(self):
        "Runs through the entire XPointer, firing events."
        sym="."
        while sym==".":
            name=self.__sgen.next_symbol()

            if name=="(":
                name=""   # Names can be defaulted
            else:
                self.__skip_over("(")

            sym=self.__sgen.next_symbol()
            if sym!=")":
                params=[sym]
                sym=self.__sgen.next_symbol()
            else:
                params=[]

            while sym==",":
                params.append(self.__sgen.next_symbol())
                sym=self.__sgen.next_symbol()

            if sym!=")":
                raise XPointerParseException("Expected ')' at %s",
                                             self.__sgen.get_pos())

            self.dispatch_term(name,params)

            if self.__sgen.more_symbols():
                sym=self.__sgen.next_symbol()
            else:
                return

        # If the XPointer ends correctly, we'll return from the if above
        raise XPointerParseException("Expected '.' at %s",
                                     self.__sgen.get_pos())

    def dispatch_term(self,name,params):
        """Called when a term is encountered to analyze it and fire more
        detailed events."""
        if self.__first_term:
            if name=="root" or name=="origin" or name=="id" or name=="html":
                if name=="root" or name=="origin":
                    if len(params)!=0:
                        raise XPointerParseException(name+" terms have no "
                                                     "parameters (at %s)",
                                                     self.__sgen.get_pos())
                    else:
                        param=None
                elif name=="id" or name=="html":
                    if len(params)!=1:
                        raise XPointerParseException(name+" terms require one "
                                                     "parameter (at %s)",
                                                     self.__sgen.get_pos())
                    else:
                        param=params[0]
                        # XXX Validate parameter

                self.__first_term=0
                self.handle_abs_term(name,param)
                return
            else:
                self.handle_abs_term("root",None)
        else:
            if name=="" and self.__prev!=None:
                name=self.__prev

        if name=="child" or name=="ancestor" or name=="psibling" or \
           name=="fsibling" or name=="descendant" or name=="following" or \
           name=="preceding":
            self.parse_rel_term(name,params)
        elif name=="span":
            self.parse_span_term(params)
        elif name=="attr":
            self.parse_attr_term(params)
        elif name=="string":
            self.parse_string_term(params)
        else:
            raise XPointerParseException("Illegal term type "+name+\
                                         " at %s",self.__sgen.get_pos())

        self.__prev=name

    def parse_rel_term(self,name,params):
        "Parses the arguments of relative location terms and fires the event."
        no=self.__parse_instance_or_all(params[0])

        if len(params)>1:
            type=params[1]
            if not (type=="#element" or type=="#pi" or type=="#comment" or \
                    type=="#text" or type=="#cdata" or type=="#all" or \
                    self.__is_valid(type,reg_name)):
                raise XPointerParseException("Invalid type at %s",
                                             self.__sgen.get_pos())
        else:
            type="#element"

        attrs=[]
        ix=2
        while ix+1<len(params):
            if not self.__is_valid(params[ix],reg_name):
                raise XPointerParseException("Not a valid name at %s",
                                             self.__sgen.get_pos())

            attrs.append((params[ix],params[ix+1]))
            ix=ix+2

        self.handle_rel_term(name,no,type,attrs)

    def parse_span_term(self,params):
        "Parses the arguments of the span term and fires the event."
        raise XPointerUnsupportedException("'span' keyword unsupported.")

    def parse_attr_term(self,params):
        "Parses the argument of the attr term and fires the event."
        if len(params)!=1:
            raise XPointerParseException("'attr' location terms must have "
                                         "exactly one parameter (at %s)",
                                         self.__sgen.get_pos())

        if not self.__is_valid(params[0],reg_name):
            raise XPointerParseException("'%s' is not a valid attribute "
                                         "name at %s" % name,
                                         self.__sgen.get_pos())

        self.handle_attr_term(params[0])

    def parse_string_term(self,params):
        "Parses the argument of the string term and fires the event."
        no=self.__parse_instance_or_all(params[0])

        if len(params)>1:
            skiplit=params[1]
        else:
            skiplit=None

        if len(params)>2:
            if params[2]=="end":
                pos="end"
            else:
                try:
                    pos=int(params[2])
                except ValueError,e:
                    raise XPointerParseException("Expected number at %s",
                                                 self.__sgen.get_pos())

                if pos==0:
                    raise XPointerParseException("0 is not an acceptable "
                                                 "value at %s",
                                                 self.__sgen.get_pos())
        else:
            pos=None

        if len(params)>3:
            try:
                length=int(params[3])
            except ValueError,e:
                raise XPointerParseException("Expected number at %s",
                                             self.__sgen.get_pos())
        else:
            length=0

        self.handle_string_term(no,skiplit,pos,length)

    # Event methods to be overridden

    def handle_abs_term(self,name,param):
        "Called to handle absolute location terms."
        pass

    def handle_rel_term(self,name,no,type,attrs):
        "Called to handle relative location terms."
        pass

    def handle_attr_term(self,attr_name):
        "Called to handle 'attr' location terms."
        pass

    def handle_span_term(self,frm,to):
        "Called to handle 'span' location terms."
        pass

    def handle_string_term(self,no,skiplit,pos,length):
        "Called to handle 'string' location terms."
        pass

# ----- XPointer implementation that navigates a DOM tree

# Iterator classes

class DescendantIterator:

    def __init__(self):
        self.stack=[]

    def __call__(self,node):
        next=node.firstChild
        if next==None:
            next=node.nextSibling

        while next==None:
            if self.stack==[]:
                raise XPointerFailedException("No matching node")
            next=self.stack[-1].nextSibling
            del self.stack[-1]

        self.stack.append(next)
        return next

class FollowingIterator:

    def __init__(self):
        self.seen_hash={}
        self.skip_child=0

    def __call__(self,node):
        if not self.skip_child:
            next=node.firstChild
        else:
            self.skip_child=0
            next=None

        if next==None:
            next=node.getNextSibling()
        if next==None:
            next=node.parentNode
            self.skip_child=1   # Don't go down, we've been there :-)

            if next.GI=="#DOCUMENT":
                raise XPointerFailedException("No matching node")

            if self.seen_hash.has_key(next.id()):
                next=node.nextSibling
                prev=node

                while next==None:
                    next=prev.parentNode
                    self.skip_child=1   # Don't go down, we've been there :-)
                    prev=next
                    if next.nodeName=="#DOCUMENT":
                        raise XPointerFailedException("No matching node")
                    if self.seen_hash.has_key(next.id()):
                        next=prev.nextSibling
                        if next!=None:
                            self.skip_child=0
            else:
                # We're above all the nodes we've looked at. Throw out the
                # hashed objects.
                self.seen_hash.clear()

        self.seen_hash[next.id()]=1
        return next

# The implementation itself

class XDOMLocator(XPointerParser):
    def __init__(self, xpointer, document):
        XPointerParser.__init__(self, xpointer)
        self.__node=document
        self.__first=1
        self.__prev=None

    def __node_matches(self,node,type,attrs):
        "Checks whether a DOM node matches a foo(2,SECTION,ID,I5) selector."
        if type==node.nodeName or \
           (type=="#element" and node.nodeType == Node.ELEMENT_NODE) or \
           (type=="#pi"      and node.nodeType == Node.PROCESSING_INSTRUCTION_NODE) or \
           (type=="#comment" and node.nodeType == Node.COMMENT_NODE) or \
           (type=="#text"    and node.nodeType == Node.TEXT_NODE) or \
           (type=="#cdata"   and node.nodeType == Node.CDATA_SECTION_NODE) or \
           type=="#all":
            if attrs!=None:
                for (a,v) in attrs:
                    try:
                        if v!=node.getAttribute(a):
                            return 0
                    except KeyError,e:
                        return 0

            return 1
        else:
            return 0

    def __get_node(self,no,type,attrs,iterator):
        """General method that iterates through the tree calling the iterator
        on the current node for each step to get the next node."""
        count=0
        current=iterator(self.__node)

        while current!=None:
            if self.__node_matches(current,type,attrs):
                count=count+1
                if count==no:
                    return current

            current=iterator(current)

        raise XPointerFailedException("No matching node")

    def __get_child(self,no,type,attrs):
        if type==None:
            candidates = self.__node.childNodes
        else:
            candidates = []

            for obj in self.__node.childNodes:
                if self.__node_matches(obj,type,attrs):
                    candidates.append(obj)
        try:
            return candidates[no-1]
        except IndexError,e:
            raise XPointerFailedException("No matching node")

    def get_node(self):
        "Returns the located node."
        return self.__node

    def handle_abs_term(self,name,param):
        "Called to handle absolute location terms."
        if name=="root":
            if self.__node.nodeType != Node.DOCUMENT_NODE:
                raise XPointerFailedException("Expected document node")
            self.__node=self.__node.documentElement
        elif name=="origin":
            pass # Just work from current node
        elif name=="id":
            self.__node=ext.GetElementById(self.__node, param)
        elif name=="html":
            raise XPointerUnsupportedException("Term type 'html' unsupported.")

    def handle_rel_term(self,name,no,type,attrs):
        "Called to handle relative location terms."
        if name=="child":
            next=self.__get_child(no,type,attrs)
        elif name=="ancestor":
            next=self.__get_node(no,type,attrs,DOM.Node._get_parentNode)
        elif name=="psibling":
            next=self.__get_node(no,type,attrs,DOM.Node._get_previousSibling)
        elif name=="fsibling":
            next=self.__get_node(no,type,attrs,DOM.Node._get_nextSibling)
        elif name=="descendant":
            next=self.__get_node(no,type,attrs,DescendantIterator())
        elif name=="following":
            next=self.__get_node(no,type,attrs,FollowingIterator())

        self.__node=next
        self.__prev=name

    def handle_attr_term(self, attr_name):
        if __node.nodeType != Node.ELEMENT_NODE:
            raise XPointerFailedException("'attr' location term used from "
                                          "non-element node")

        if not self.__node.attributes.has_key(attr_name):
            raise XPointerFailedException("Non-existent attribute '%s' located"
                                          " by 'attr' term" % attr_name)

        self.__node=self.__node.attributes.getNamedItem(attr_name)

    def handle_string_term(self,no,skiplit,pos,length):
        raise XPointerUnsupportedException("'string' location terms not "
                                           "supported")


def LocateNode(node, xpointer):
    try:
        xp=XDOMLocator(xpointer, node)
        xp.parse()
        return xp.get_node()
    except XPointerParseException,e:
        print "ERROR: "+str(e)
