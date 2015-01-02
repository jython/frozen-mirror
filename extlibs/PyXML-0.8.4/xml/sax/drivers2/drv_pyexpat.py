"""
SAX driver for the Pyexpat C module, based on xml.sax.expatdriver.

$Id: drv_pyexpat.py,v 1.6 2000/09/26 19:53:43 loewis Exp $
"""

# XXX: todo list of old drv_pyexpat.py, check whether any of these
# have been fixed.
# Todo on driver:
#  - make it support external entities (wait for pyexpat.c)
#  - enable configuration between reset() and feed() calls
#  - support lexical events?
#  - proper inputsource handling
#  - properties and features

# Todo on pyexpat.c:
#  - support XML_ExternalEntityParserCreate
#  - exceptions in callouts from pyexpat to python code lose position info

from xml.sax.expatreader import create_parser
