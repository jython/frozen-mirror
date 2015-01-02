"""
This file contains the default classes that are used to receive events
from the XML parser. All these classes are meant to be subclassed (or
imitated) by clients that want to handle these functions themselves.
Application is the class that receives document data from the parser,
and is probably the one most people want.

$Id: xmlapp.py,v 1.12 2002/08/13 09:28:51 afayolle Exp $
"""

import sys,urllib2,urlparse

from xmlutils import *

# ==============================
# The default application class
# ==============================

class Application:
    """This is the class that represents the application that receives
    parsed data from the parser. It is meant to be subclassed by users."""

    def __init__(self):
        self.locator=None

    def set_locator(self,locator):
        """Gives the application an object to ask for the current location.
        Called automagically by the parser."""
        self.locator=locator

    def doc_start(self):
        "Notifies the application of the start of the document."
        pass

    def doc_end(self):
        "Notifies the application of the end of the document."
        pass

    def handle_comment(self,data):
        "Notifies the application of comments."
        pass

    def handle_start_tag(self,name,attrs):
        "Notifies the application of start tags (and empty element tags)."
        pass

    def handle_end_tag(self,name):
        "Notifies the application of end tags (and empty element tags)."
        pass

    def handle_data(self,data,start,end):
        "Notifies the application of character data."
        pass

    def handle_ignorable_data(self,data,start,end):
        "Notifies the application of character data that can be ignored."
        pass

    def handle_pi(self,target,data):
        "Notifies the application of processing instructions."
        pass

    def handle_doctype(self,root,pubID,sysID):
        "Notifies the application of the document type declaration."
        pass

    def set_entity_info(self,xmlver,enc,sddecl):
        """Notifies the application of information about the current entity
        supplied by an XML or text declaration. All three parameters will be
        None, if they weren't present."""
        pass

# ==============================
# The public identifier resolver
# ==============================

class PubIdResolver:
    """An application class that resolves public identifiers to system
    identifiers."""

    def resolve_pe_pubid(self,pubid,sysid):
        """Maps the public identifier of a parameter entity to a system
        identifier. The default implementation just returns the system
        identifier."""
        return sysid

    def resolve_doctype_pubid(self,pubid,sysid):
        """Maps the public identifier of the DOCTYPE declaration to a system
        identifier. The default implementation just returns the system
        identifier."""
        return sysid

    def resolve_entity_pubid(self,pubid,sysid):
        """Maps the public identifier of an external entity to a system
        identifier. The default implementation just returns the system
        identifier."""
        return sysid

# ==============================
# The default error handler
# ==============================

class ErrorHandler:
    """An error handler for the parser. This class can be subclassed by clients
    that want to use their own error handlers."""

    def __init__(self,locator):
        self.locator=locator

    def set_locator(self,loc):
        self.locator=loc

    def get_locator(self):
        return self.locator

    def warning(self,msg):
        "Handles a non-fatal error message."
        pass

    def error(self,msg):
        self.fatal(msg)

    # "The reports of the error's fatality are much exaggerated"
    # --Paul Prescod

    def fatal(self,msg):
        "Handles a fatal error message."
        if self.locator==None:
            print "ERROR: "+msg
        else:
            print "ERROR: "+msg+" at %s:%d:%d" % (self.locator.get_current_sysid(),\
                                                  self.locator.get_line(),\
                                                  self.locator.get_column())
            print "TEXT: '%s'" % (self.locator.data[self.locator.pos:\
                                                    self.locator.pos+10])
        sys.exit(1)

# ==============================
# The default entity handler
# ==============================

class EntityHandler:
    "An entity handler for the parser."

    def __init__(self,parser):
        self.parser=parser

    def resolve_ent_ref(self,entname):
        """Resolves a general entity reference and returns its contents. The
        default method only resolves the predefined entities. Returns a
        2-tuple (n,m) where n is true if the entity is internal. For internal
        entities m is the value, for external ones it is the system id."""

        try:
            return (1,predef_ents[entname])
        except KeyError:
            self.parser.report_error(3021,entname)
            return (1,"")

# ==============================
# A DTD event handler
# ==============================

class DTDConsumer:
    """Represents an XML DTD. This class can be subclassed by applications
    which want to handle the DTD information themselves."""

    def __init__(self,parser):
        self.parser=parser

    def dtd_start(self):
        "Called when DTD parsing starts."
        pass

    def dtd_end(self):
        "Called when the DTD is completely parsed."
        pass

    def new_general_entity(self,name,val):
        "Receives internal general entity declarations."
        pass

    def new_external_entity(self,ent_name,pub_id,sys_id,ndata):
        """Receives external general entity declarations. 'ndata' is the
        empty string if the entity is parsed."""
        pass

    def new_parameter_entity(self,name,val):
        "Receives internal parameter entity declarations."
        pass

    def new_external_pe(self,name,pubid,sysid):
        "Receives external parameter entity declarations."
        pass

    def new_notation(self,name,pubid,sysid):
        "Receives notation declarations."
        pass

    def new_element_type(self,elem_name,elem_cont):
        "Receives the declaration of an element type."
        pass

    def new_attribute(self,elem,attr,a_type,a_decl,a_def):
        "Receives the declaration of a new attribute."
        pass

    def handle_comment(self,contents):
        "Receives the contents of a comment."
        pass

    def handle_pi(self,target,data):
        "Receives the target and data of processing instructions."
        pass

# ==============================
# An inputsource factory
# ==============================

class InputSourceFactory:
    "A class that creates file-like objects from system identifiers."

    def create_input_source(self,sysid):
        if sysid[1:3]==":\\" or urlparse.urlparse(sysid)[0] == '':
            return open(sysid)
        else:
            return urllib2.urlopen(sysid)
