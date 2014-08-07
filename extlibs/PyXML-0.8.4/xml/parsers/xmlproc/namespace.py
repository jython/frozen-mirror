"""
A parser filter for namespace support. Placed externally to the parser
for efficiency reasons.

$Id: namespace.py,v 1.5 2001/12/30 12:09:14 loewis Exp $
"""

import string
import xmlapp

# --- ParserFilter

class ParserFilter(xmlapp.Application):
    "A generic parser filter class."

    def __init__(self):
        xmlapp.Application.__init__(self)
        self.app=xmlapp.Application()

    def set_application(self,app):
        "Sets the application to report events to."
        self.app=app

    # --- Methods inherited from xmlapp.Application

    def set_locator(self,locator):
        xmlapp.Application.set_locator(self,locator)
        self.app.set_locator(locator)

    def doc_start(self):
        self.app.doc_start()

    def doc_end(self):
        self.app.doc_end()

    def handle_comment(self,data):
        self.app.handle_comment(data)

    def handle_start_tag(self,name,attrs):
        self.app.handle_start_tag(name,attrs)

    def handle_end_tag(self,name):
        self.app.handle_end_tag(name)

    def handle_data(self,data,start,end):
        self.app.handle_data(data,start,end)

    def handle_ignorable_data(self,data,start,end):
        self.app.handle_ignorable_data(data,start,end)

    def handle_pi(self,target,data):
        self.app.handle_pi(target,data)

    def handle_doctype(self,root,pubID,sysID):
        self.app.handle_doctype(root,pubID,sysID)

    def set_entity_info(self,xmlver,enc,sddecl):
        self.app.set_entity_info(xmlver,enc,sddecl)

# --- NamespaceFilter

class NamespaceFilter(ParserFilter):
    """An xmlproc application that processes qualified names and reports them
    as 'URI local-part' names. It reports errors through the error reporting
    mechanisms of the parser."""

    def __init__(self,parser):
        ParserFilter.__init__(self)
        self.ns_map={}       # Current prefix -> URI map
        self.ns_stack=[]     # Pushed for each element, used to maint ns_map
        self.rep_ns_attrs=0  # Report xmlns-attributes?
        self.parser=parser

    def set_report_ns_attributes(self,action):
        "Tells the filter whether to report or delete xmlns-attributes."
        self.rep_ns_attrs=action

    # --- Overridden event methods

    def handle_start_tag(self,name,attrs):
        old_ns={} # Reset ns_map to these values when we leave this element
        del_ns=[] # Delete these prefixes from ns_map when we leave element

        # attrs=attrs.copy()   Will have to do this if more filters are made

        # Find declarations, update self.ns_map and self.ns_stack
        for (a,v) in attrs.items():
            if a[:6]=="xmlns:":
                prefix=a[6:]
                if string.find(prefix,":")!=-1:
                    self.parser.report_error(1900)

                if v=="":
                    self.parser.report_error(1901)
            elif a=="xmlns":
                prefix=""
            else:
                continue

            if self.ns_map.has_key(prefix):
                old_ns[prefix]=self.ns_map[prefix]
            else:
                del_ns.append(prefix)

            if prefix=="" and v=="":
                del self.ns_map[prefix]
            else:
                self.ns_map[prefix]=v

            if not self.rep_ns_attrs:
                del attrs[a]

        self.ns_stack.append((old_ns,del_ns))

        # Process elem and attr names
        name=self.__process_name(name)

        parts=string.split(name)
        if len(parts)>1:
            ns=parts[0]
        else:
            ns=None

        for (a,v) in attrs.items():
            del attrs[a]
            aname=self.__process_name(a,ns)
            if attrs.has_key(aname):
                self.parser.report_error(1903)
            attrs[aname]=v

        # Report event
        self.app.handle_start_tag(name,attrs)

    def handle_end_tag(self,name):
        name=self.__process_name(name)

        # Clean up self.ns_map and self.ns_stack
        (old_ns,del_ns)=self.ns_stack[-1]
        del self.ns_stack[-1]

        self.ns_map.update(old_ns)
        for prefix in del_ns:
            del self.ns_map[prefix]

        self.app.handle_end_tag(name)

    # --- Internal methods

    def __process_name(self,name,default_to=None):
        n=string.split(name,":")
        if len(n)>2:
            self.parser.report_error(1900)
            return name
        elif len(n)==2:
            if n[0]=="xmlns":
                return name

            try:
                return "%s %s" % (self.ns_map[n[0]],n[1])
            except KeyError:
                self.parser.report_error(1902)
                return name
        elif default_to!=None:
            return "%s %s" % (default_to,name)
        elif self.ns_map.has_key("") and name!="xmlns":
            return "%s %s" % (self.ns_map[""],name)
        else:
            return name
