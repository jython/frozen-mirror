"""Extended XML support for Python

The full PyXML package, available from http://pyxml.sf.net, is installed.

This package contains seven sub-packages:

dom -- The W3C Document Object Model.  This supports DOM Level 1 +
       Namespaces.

marshal -- Converts Python objects to XML and back again.

ns -- Contains namespace URIs for various standards.

parsers -- Python wrappers for XML parsers.

sax -- The Simple API for XML, developed by XML-Dev, led by David
       Megginson and ported to Python by Lars Marius Garshol.  This
       supports the SAX 2 API.

schema -- Support for XML schema languages.  Currently TREX is the only
          supported language.

utils -- Various small utility modules.

xpath -- XPath parsing and evaluation.  Implemented by Fourthought, Inc.
"""


# xml.unicode is not listed because it is for internal use and backwards
# compatibility only.
__all__ = ['dom', 'marshal', 'parsers', 'sax', 'schema', 'utils', 'xpath', 'xslt']

# Needs to synchronize with setup.py
# Never drop digits from the end.
version_info = (0,8,4)
__version__ = "0.8.4"
