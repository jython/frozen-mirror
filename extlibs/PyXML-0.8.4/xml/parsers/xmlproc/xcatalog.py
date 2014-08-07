"""
Support for XCatalog catalog files.
$Id: xcatalog.py,v 1.9 2001/12/30 12:09:14 loewis Exp $
"""

import catalog,xmlapp,xmlproc

# --- An XCatalog parser factory

class XCatParserFactory:

    def __init__(self,error_lang=None):
        self.error_lang=error_lang

    def make_parser(self,sysid):
        return XCatalogParser(self.error_lang)

class FancyParserFactory:

    def __init__(self,error_lang=None):
        self.error_lang=error_lang

    def make_parser(self,sysid):
        if sysid[-4:]==".soc":
            return catalog.CatalogParser(self.error_lang)
        elif sysid[-4:]==".xml":
            return XCatalogParser(self.error_lang)
        else:
            return catalog.CatalogParser(self.error_lang)

# --- An XCatalog 0.1 parser

class XCatalogParser(catalog.AbstrCatalogParser,xmlapp.Application):

    def __init__(self,error_lang=None):
        catalog.AbstrCatalogParser.__init__(self)
        xmlapp.Application.__init__(self)
        self.error_lang=error_lang

    def parse_resource(self,sysid):
        parser=xmlproc.XMLProcessor()
        self.parser=parser
        parser.set_application(self)
        if self.error_lang!=None:
            parser.set_error_language(self.error_lang)
        parser.set_error_handler(self.err)
        parser.parse_resource(sysid)
        del self.parser

    def handle_start_tag(self,name,attrs):
        try:
            if name=="Base":
                self.app.handle_base(attrs["HRef"])
            elif name=="Map":
                self.app.handle_public(attrs["PublicID"],attrs["HRef"])
            elif name=="Delegate":
                self.app.handle_delegate(attrs["PublicID"],attrs["HRef"])
            elif name=="Extend":
                self.app.handle_catalog(attrs["HRef"])
            elif name!="XCatalog":
                self.parser.report_error(5000,(name,))
        except KeyError,e:
            if e.args[0] in ("HRef" , "PublicID"):
                self.parser.report_error(5001,(e.args[0],name))
            else:
                raise e # This came from the application, pass it on

    # implementing Locator methods

    def get_current_sysid(self):
        return self.parser.get_current_sysid()

    def get_line(self):
        return self.parser.get_line()

    def get_column(self):
        return self.parser.get_column()
