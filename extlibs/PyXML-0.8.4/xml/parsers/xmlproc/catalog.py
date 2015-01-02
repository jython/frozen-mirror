"""
An SGML Open catalog file parser.
$Id: catalog.py,v 1.14 2001/12/30 12:09:14 loewis Exp $
"""

import string,sys

import xmlutils,xmlapp

# --- Parser factory class

class CatParserFactory:
    """This class is used by the CatalogManager to create new parsers as they
    are needed."""

    def __init__(self,error_lang=None):
        self.error_lang=error_lang

    def make_parser(self,sysid):
        return CatalogParser(self.error_lang)

# --- Empty catalog application class

class CatalogApp:

    def handle_public(self,pubid,sysid):
        pass

    def handle_delegate(self,prefix,sysid):
        pass

    def handle_document(self,sysid):
        pass

    def handle_system(self,sysid1,sysid2):
        pass

    def handle_base(self,sysid):
        pass

    def handle_catalog(self,sysid):
        pass

    def handle_override(self,yesno):
        pass

    def handle_doctype(self, docelem, sysid):
        pass

    def handle_sgmldecl(self, sysid):
        '''Called for SGMLDECL catalog entries. These are only used by
        SGML systems and tell the application where to find the SGML
        declaration file.'''

# --- Abstract catalog parser with common functionality

class AbstrCatalogParser:
    "Abstract catalog parser with functionality needed in all such parsers."

    def __init__(self,error_lang=None):
        self.app=CatalogApp()
        self.err=xmlapp.ErrorHandler(None)
        self.error_lang=error_lang

    def set_application(self,app):
        self.app=app

    def set_error_handler(self,err):
        self.err=err

# --- The catalog file parser (SGML Open Catalogs)

class CatalogParser(AbstrCatalogParser,xmlutils.EntityParser):
    "A parser for SGML Open catalog files."

    def __init__(self,error_lang=None):
        AbstrCatalogParser.__init__(self,error_lang)
        xmlutils.EntityParser.__init__(self)

        # p=pubid (or prefix)
        # s=sysid (to be resolved)
        # o=other
        self.entry_hash={ "PUBLIC": ("p","s"), "DELEGATE": ("p","s"),
                          "CATALOG": ("s"), "DOCUMENT": ("s"),
                          "BASE": ("o"), "SYSTEM": ("o","s"),
                          "OVERRIDE": ("o"), "DOCTYPE" : ("o", "s"),
                          "SGMLDECL" : ("s")}

    def parseStart(self):
        if self.error_lang:
            self.set_error_language(self.error_lang)

    def do_parse(self):
        try:
            while self.pos+1<self.datasize:
                prepos=self.pos

                self.skip_stuff()
                if self.pos+1>=self.datasize:
                    break

                entryname=self.find_reg(xmlutils.reg_ws)
                if not self.entry_hash.has_key(entryname):
                    self.report_error(5100,(entryname,))
                else:
                    self.parse_entry(entryname,self.entry_hash[entryname])

        except xmlutils.OutOfDataException:
            if self.final:
                raise
            else:
                self.pos=prepos  # Didn't complete the construct

    def parse_arg(self):
        if self.now_at('"'):
            delim='"'
        elif self.now_at("'"):
            delim="'"
        else:
            return self.find_reg(xmlutils.reg_ws,0)

        return self.scan_to(delim)

    def skip_stuff(self):
        "Skips whitespace and comments between items."
        while 1:
            self.skip_ws()
            if self.now_at("--"):
                self.scan_to("--")
            else:
                break

    def parse_entry(self,name,args):
        arglist=[]
        for arg in args:
            self.skip_stuff()
            arglist.append(self.parse_arg())

        if name == "PUBLIC":
            self.app.handle_public(arglist[0],arglist[1])
        elif name == "CATALOG":
            self.app.handle_catalog(arglist[0])
        elif name == "DELEGATE":
            self.app.handle_delegate(arglist[0],arglist[1])
        elif name == "BASE":
            self.app.handle_base(arglist[0])
        elif name == "DOCUMENT":
            self.app.handle_document(arglist[0])
        elif name == "SYSTEM":
            self.app.handle_system(arglist[0],arglist[1])
        elif name == "OVERRIDE":
            self.app.handle_override(arglist[0])
        elif name == "DOCTYPE":
            self.app.handle_doctype(arglist[0], arglist[1])
        elif name == "SGMLDECL":
            self.app.handle_sgmldecl(arglist[0])

# --- A catalog file manager

class CatalogManager(CatalogApp):

    def __init__(self, error_handler = None):
        self.__public = {}
        self.__system = {}
        self.__delegations = []
        self.__document = None
        self.__doctypes = {} # docelem -> sysid
        self.__base = None
        self.__sgmldecl = None

        # Keeps track of sysid base even if we recurse into other catalogs
        self.__catalog_stack=[]

        self.err = error_handler or xmlapp.ErrorHandler(None)
        self.parser_fact = CatParserFactory()
        self.parser = None

    # --- application interface

    def set_error_handler(self,err):
        self.err=err

    def set_parser_factory(self,parser_fact):
        self.parser_fact=parser_fact

    def parse_catalog(self,sysid):
        self.__catalog_stack.append((self.__base,))
        self.__base=sysid

        self.parser=self.parser_fact.make_parser(sysid)
        old_locator = self.err.get_locator()
        self.err.set_locator(self.parser)
        self.parser.set_error_handler(self.err)
        self.parser.set_application(self)
        self.parser.parse_resource(sysid)

        self.err.set_locator(old_locator)
        self.__base=self.__catalog_stack[-1][0]
        del self.__catalog_stack[-1]

    def report(self,out=sys.stdout):
        out.write("Document sysid: %s\n" % self.__document)

        out.write("FPI mappings:\n")
        for it in self.__public.items():
            out.write("  %s -> %s\n" % it)

        out.write("Sysid mappings:\n")
        for it in self.__system.items():
            out.write("  %s -> %s\n" % it)

        out.write("Delegates:\n")
        for (prefix,cat_man) in self.__delegations:
            out.write("---PREFIX MAPPER: %s\n" % prefix)
            cat_man.report(out)
            out.write("---EOPM\n")

    # --- parse events

    def handle_base(self,newbase):
        self.__base=newbase

    def handle_catalog(self,sysid):
        self.parse_catalog(self.__resolve_sysid(sysid))

    def handle_public(self,pubid,sysid):
        self.__public[pubid]=self.__resolve_sysid(sysid)

    def handle_system(self,sysid1,sysid2):
        self.__system[self.__resolve_sysid(sysid1)]=\
                                                self.__resolve_sysid(sysid2)

    def handle_delegate(self,prefix,sysid):
        catalog_manager=CatalogManager()
        catalog_manager.set_parser_factory(self.parser_fact)
        catalog_manager.parse_catalog(self.__resolve_sysid(sysid))
        self.__delegations.append((prefix,catalog_manager))

    def handle_document(self, sysid):
        self.__document = self.__resolve_sysid(sysid)

    def handle_sgmldecl(self, sysid):
        self.__sgmldecl = self.__resolve_sysid(sysid)

    def handle_doctype(self, docelem, sysid):
        self.__doctypes[docelem] = self.__resolve_sysid(sysid)

    # --- client services

    def get_public_ids(self):
        """Returns a list of all declared public indentifiers in this catalog
        and delegates."""
        list=self.__public.keys()
        for delegate in self.__delegations:
            list=list+delegate.get_public_ids()

        return list

    def get_document_sysid(self):
        return self.__document

    def get_sgmldecl(self):
        return self.__sgmldecl

    def remap_sysid(self,sysid):
        try:
            return self.__system[sysid]
        except KeyError:
            return sysid

    def resolve_sysid(self,pubid,sysid):
        if pubid!=None:
            resolved=0
            for (prefix,catalog) in self.__delegations:
                if prefix==pubid[:len(prefix)]:
                    sysid=catalog.resolve_sysid(pubid,sysid)
                    resolved=1
                    break

            if not resolved:
                try:
                    sysid=self.__public[pubid]
                except KeyError:
                    self.err.error("Unknown public identifier '%s'" % pubid)

            return self.remap_sysid(sysid)
        else:
            self.remap_sysid(sysid)

    def get_doctype_sysid(self, docelem):
        """Returns the system identifier of the DTD with the given document
        element. Raises KeyError if no such document element is known."""
        return self.remap_sysid(self.__doctypes[docelem])

    # --- internal methods

    def __resolve_sysid(self,sysid):
        return xmlutils.join_sysids(self.__base,sysid)

# --- An xmlproc catalog client

class xmlproc_catalog:

    def __init__(self,sysid,pf,error_handler=None):
        self.catalog=CatalogManager(error_handler)
        self.catalog.set_parser_factory(pf)
        self.catalog.parse_catalog(sysid)

    def get_document_sysid(self):
        return self.catalog.get_document_sysid()

    def get_sgmldecl(self):
        return self.catalog.get_sgmldecl()

    def resolve_pe_pubid(self,pubid,sysid):
        if pubid==None:
            return self.catalog.remap_sysid(sysid)
        else:
            return self.catalog.resolve_sysid(pubid,sysid)

    def resolve_doctype_pubid(self,pubid,sysid):
        if pubid==None:
            return self.catalog.remap_sysid(sysid)
        else:
            return self.catalog.resolve_sysid(pubid,sysid)

    def resolve_entity_pubid(self,pubid,sysid):
        if pubid==None:
            return self.catalog.remap_sysid(sysid)
        else:
            return self.catalog.resolve_sysid(pubid,sysid)

# --- A SAX catalog client

class SAX_catalog:

    def __init__(self,sysid,pf):
        self.catalog=CatalogManager()
        self.catalog.set_parser_factory(pf)
        self.catalog.parse_catalog(sysid)

    def resolveEntity(self,pubid,sysid):
        return self.catalog.resolve_sysid(pubid,sysid)
