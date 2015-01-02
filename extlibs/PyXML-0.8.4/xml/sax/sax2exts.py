"""
Various extensions to the core SAX 2.0 API.

$Id: sax2exts.py,v 1.5 2001/12/30 22:17:03 loewis Exp $
"""

import saxexts,saxlib

# In SAX2, validation is turned-on through a property. Make sure
# that all parsers returned from this factory are validating
class ValidatingReaderFactory(saxexts.ParserFactory):
    def make_parser(self, parser_list = []):
        p = saxexts.ParserFactory.make_parser(self,parser_list)
        p.setFeature(saxlib.feature_validation, 1)
        return p


# --- XMLReader factory

XMLReaderFactory = saxexts.ParserFactory

# --- Creating parser factories

XMLParserFactory = XMLReaderFactory(["xml.sax.drivers2.drv_pyexpat",
                                     "xml.sax.drivers2.drv_xmlproc"])

XMLValParserFactory = ValidatingReaderFactory(["xml.sax.drivers2.drv_xmlproc"])

HTMLParserFactory=XMLReaderFactory(["xml.sax.drivers2.drv_htmllib",
                                    "xml.sax.drivers2.drv_sgmlop",
                                    "xml.sax.drivers2.drv_sgmllib"])

SGMLParserFactory=XMLReaderFactory(["xml.sax.drivers2.drv_sgmlop",
                                    "xml.sax.drivers2.drv_sgmllib"])

def make_parser(parser_list = []):
    return XMLParserFactory.make_parser(parser_list)
