########################################################################
#
# File Name:            OtherXslElement.py
#
#
"""
Non-template instructions from the XSLT spec
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 FourThought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom import EMPTY_NAMESPACE
import xml.dom.ext
import xml.xslt
from xml.xslt import XsltElement, XsltException, Error, XSL_NAMESPACE


class DecimalFormatElement(XsltElement):
    legalAttrs = ('name', 'decimal-separator', 'grouping-separator', 'infinity', 'minus-sign', 'NaN', 'percent', 'per-mille', 'zero-digit', 'digit', 'pattern-separator')

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE, localName='decimal-format', prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        return

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         return base_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state)
        return


class IncludeElement(XsltElement):
    legalAttrs = ('href',)

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE, localName='include', prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        self.__dict__['_href'] = self.getAttributeNS(EMPTY_NAMESPACE, 'href')
        return

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         new_state = (base_state, self._href, )
         return new_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state[0])
        self._href = state[1]
        return


class FallbackElement(XsltElement):
    legalAttrs = ()

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE, localName='fallback', prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)
        self.__dict__['_nss'] = xml.dom.ext.GetAllNs(self)
        return

    def setup(self):
        return

    def instantiate(self, context, processor):
        origState = context.copy()
        context.setNamespaces(self._nss)
        for child in self.childNodes:
            context = child.instantiate(context, processor)[0]
        context.set(origState)
        return (context,)

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         return base_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state)
        return


class ImportElement(XsltElement):
    legalAttrs = ('href',)

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE, localName='import', prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)
        self.stylesheet = None

    def setup(self):
        self.href = self.getAttributeNS(EMPTY_NAMESPACE, 'href')

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         return base_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state)
        return


class KeyElement(XsltElement):
    legalAttrs = ('name', 'match', 'use')

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE, localName='key', prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        pass

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         return base_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state)
        return


class NamespaceAliasElement(XsltElement):
    legalAttrs = ('stylesheet-prefix', 'result-prefix')

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE, localName='namespace-alias', prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        pass

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         return base_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state)
        return


class OutputElement(XsltElement):
    legalAttrs = ('method', 'version', 'encoding', 'omit-xml-declaration', 'standalone', 'doctype-public', 'doctype-system', 'cdata-section-elements', 'indent', 'media-type')

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE, localName='output', prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        pass

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         return base_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state)
        return


class PreserveSpaceElement(XsltElement):
    legalAttrs = ('elements',)

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE, localName='preserve-space', prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        pass

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         return base_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state)
        return

    
class StripSpaceElement(XsltElement):
    legalAttrs = ('elements',)

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE, localName='strip-space', prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        pass

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         return base_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state)
        return

    
import urlparse
from xml.xslt import XsltException, Error
import xml.xslt.StylesheetReader
