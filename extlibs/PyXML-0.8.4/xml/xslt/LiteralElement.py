########################################################################
#
# File Name:            LiteralElement.py
#
#
"""
Implementation of the XSLT Spec import stylesheet element.
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import string
import xml.dom.Element
import xml.dom.ext
from xml.xslt import XsltElement, AttributeValueTemplate
from xml.xslt import XSL_NAMESPACE, XsltException, Error
from xml.xpath import Util
from xml.dom import XML_NAMESPACE

class LiteralElement(XsltElement):
    def __init__(self, doc, uri, localName, prefix, baseUri):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        self._useAttributeSets = string.splitfields(self.getAttributeNS(XSL_NAMESPACE, 'use-attribute-sets'))
        self._nss = xml.dom.ext.GetAllNs(self)
        self._outputNss = {}
        self.__attrs = []
        self.excludedNss = []
        sheet = self.ownerDocument.documentElement
        sheet._lres.append(self)
        excluded_prefixes = self.getAttributeNS(XSL_NAMESPACE, 'exclude-result-prefixes')
        if excluded_prefixes:
            excluded_prefixes = string.splitfields(excluded_prefixes)
            for prefix in excluded_prefixes:
                if prefix == '#default': prefix = ''
                self.excludedNss.append(self._nss[prefix])
        node = self.parentNode
        while node:
            if hasattr(node, 'excludedNss'):
                self.excludedNss = self.excludedNss + node.excludedNss
                break
            node = node.parentNode
        for attr in self.attributes.values():
            if attr.name == 'xmlns' or attr.name[:6] == 'xmlns:' or attr.namespaceURI == XSL_NAMESPACE:
                continue
            name = attr.name
            local_name = attr.localName
            prefix = attr.prefix
            uri = attr.namespaceURI
            if sheet.namespaceAliases[1].has_key(uri):
                name = sheet.namespaceAliases[0][prefix] + ':' + local_name
                uri = sheet.namespaceAliases[1][uri]
            self.__attrs.append((name, uri, AttributeValueTemplate.AttributeValueTemplate(attr.value)))
        self.fixupAliases()
        return

    def fixupAliases(self):
        sheet = self.ownerDocument.documentElement
        self._aliasUri = self.namespaceURI
        self._aliasNodeName = self.nodeName
        if sheet.namespaceAliases[1].has_key(self.namespaceURI):
            self._aliasNodeName = sheet.namespaceAliases[0][self.prefix] + ':' + self.localName
            self._aliasUri = sheet.namespaceAliases[1][self.namespaceURI]
        output_nss = self._nss.items()
        for ons in output_nss:
            prefix = ons[0]
            ns = ons[1]
            if ns in sheet.extensionNss + self.excludedNss + [XSL_NAMESPACE , XML_NAMESPACE]:
                continue
            if sheet.namespaceAliases[1].has_key(ns):
                if sheet.namespaceAliases[0].has_key(prefix):
                    prefix = sheet.namespaceAliases[0][prefix]
                ns = sheet.namespaceAliases[1][ns]
            self._outputNss[prefix] = ns
        return
    
    def instantiate(self, context, processor):
        origState = context.copy()
        context.setNamespaces(self._nss)
        
        processor.writers[-1].startElement(self._aliasNodeName, self._aliasUri, self._outputNss)
        for (name, uri, avt) in self.__attrs:
            value = avt.evaluate(context)
            processor.writers[-1].attribute(name, value, uri)
        for attr_set_name in self._useAttributeSets:
            split_name = Util.ExpandQName(attr_set_name, namespaces=context.processorNss)
            try:
                attr_set = processor.attributeSets[split_name]
            except KeyError:
                raise XsltException(Error.UNDEFINED_ATTRIBUTE_SET, attr_set_name)
            attr_set.use(context, processor)
        for child in self.childNodes:
            context = child.instantiate(context, processor)[0]
        processor.writers[-1].endElement(self._aliasNodeName)

        context.set(origState)
        return (context,)

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         new_state = (base_state, self._nss, self._useAttributeSets,
                      self._outputNss, self._aliasUri, self._aliasNodeName,
                      self.__attrs, self.excludedNss)
         return new_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state[0])
        self._nss = state[1]
        self._useAttributeSets = state[2]
        self._outputNss = state[3]
        self._aliasUri = state[4]
        self._aliasNodeName = state[5]
        self.__attrs = state[6]
        self.excludedNss = state[7]
        return

