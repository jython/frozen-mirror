"""
A SAX 2.0 driver for htmllib.

$Id: drv_htmllib.py,v 1.2 2001/12/30 12:13:45 loewis Exp $
"""

import types, string

from xml.sax import SAXNotSupportedException, SAXNotRecognizedException
from xml.sax.xmlreader import IncrementalParser
from drv_sgmllib import SgmllibDriver

class HtmllibDriver(SgmllibDriver):

    from htmlentitydefs import entitydefs

# ---

def create_parser():
    return HtmllibDriver()
