########################################################################
#
# File Name:            FtElements.py
#
#
"""
FourThought proprietary extension elements
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

from xml.dom import EMPTY_NAMESPACE
import xml.dom.ext
from xml.xslt import XsltElement, XsltException, Error
from xml.xslt import XSL_NAMESPACE
from xml.xslt import AttributeValueTemplate, OutputParameters, TextWriter
from xml.xpath import Util, FT_EXT_NAMESPACE, XPathParser
from xml.xslt import ApplyTemplatesElement

class FtApplyTemplates(ApplyTemplatesElement.ApplyTemplatesElement):
    def setup(self):
        ApplyTemplatesElement.ApplyTemplatesElement.setup(self)

        #Overwrite the mode
        mode_attr = self.getAttributeNS(EMPTY_NAMESPACE, 'mode')
        if mode_attr != '':
            parser = XPathParser.XPathParser()
            self.__dict__['_mode'] = parser.parseExpression(mode_attr)

    def _instantiateMode(self,context):
        rt = self._mode.evaluate(context)

        split_name = Util.ExpandQName(
            rt,
            namespaces=self._nss
            )
        return split_name
            

class WriteFileElement(XsltElement):
    def __init__(self, doc, uri=FT_EXT_NAMESPACE, localName='write-file', prefix='ft', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        self.__dict__['_nss'] = xml.dom.ext.GetAllNs(self)
        self.__dict__['_name'] = AttributeValueTemplate.AttributeValueTemplate(self.getAttributeNS(EMPTY_NAMESPACE, 'name'))
        self.__dict__['_overwrite'] = AttributeValueTemplate.AttributeValueTemplate(self.getAttributeNS(EMPTY_NAMESPACE, 'overwrite'))
        out = OutputParameters()
        for child in self.childNodes:
            if (child.namespaceURI, child.localName) == (FT_EXT_NAMESPACE, 'output'):
                method = child.getAttributeNS(EMPTY_NAMESPACE, 'method')
                if method: out.method = method
                version = child.getAttributeNS(EMPTY_NAMESPACE, 'version')
                if version: out.version = version
                encoding = child.getAttributeNS(EMPTY_NAMESPACE, 'encoding')
                if encoding: out.encoding = encoding
                omit_xml_decl = child.getAttributeNS(EMPTY_NAMESPACE, 'omit-xml-declaration')
                if omit_xml_decl: out.omitXmlDeclaration = omit_xml_decl
                standalone = child.getAttributeNS(EMPTY_NAMESPACE, 'standalone')
                if standalone: out.standalone = standalone
                doctype_system = child.getAttributeNS(EMPTY_NAMESPACE, 'doctype-system')
                if doctype_system: out.doctypeSystem = doctype_system
                doctype_public = child.getAttributeNS(EMPTY_NAMESPACE, 'doctype-public')
                if doctype_public: out.doctypePublic = doctype_public
                media_type = child.getAttributeNS(EMPTY_NAMESPACE, 'media-type')
                if media_type: out.mediaType = media_type
                cdata_sec_elem = child.getAttributeNS(EMPTY_NAMESPACE, 'cdata-section-elements')
                if cdata_sec_elem: out.cdataSectionElements = cdata_sec_elem
                indent = child.getAttributeNS(EMPTY_NAMESPACE, 'indent')
                if indent: out.indent = indent
            self.__dict__['_outputParams'] = out
        return

    def instantiate(self, context, processor):

        origState = context.copy()
        context.processorNss = self._nss
        
        name = self._name.evaluate(context)
        overwrite = self._overwrite.evaluate(context)
        if overwrite == 'yes':
            f = open(name, 'w')
        else:
            f = open(name, 'a')
        processor.addHandler(self._outputParams, f)
        for child in self.childNodes:
            context = child.instantiate(context, processor)[0]
        processor.removeHandler()
        f.close()

        context.set(origState)
        return (context,)

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         new_state = (base_state, self._nss, self._name,self._overwrite,self._outputParams)
         return new_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state[0])
        self._nss = state[1]
        self._name = state[2]
        self._overwrite = state[3]
        self._outputParams = state[4]
        return


class FtOutputElement(XsltElement):
    def __init__(self, doc, uri=FT_EXT_NAMESPACE, localName='output', prefix='ft', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        return

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)


class MessageOutputElement(XsltElement):
    def __init__(self, doc, uri=FT_EXT_NAMESPACE, localName='message-output', prefix='ft', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        #FIXME: disable -> silent
        self.__dict__['_nss'] = xml.dom.ext.GetAllNs(self)
        if self.getAttributeNS(EMPTY_NAMESPACE, 'file'):
            self.__dict__['_file'] = AttributeValueTemplate.AttributeValueTemplate(self.getAttributeNS(EMPTY_NAMESPACE, 'file'))
        else:
            self.__dict__['_file'] = None
        if self.getAttributeNS(EMPTY_NAMESPACE, 'disable'):
            self.__dict__['_disable'] = AttributeValueTemplate.AttributeValueTemplate(self.getAttributeNS(EMPTY_NAMESPACE, 'disable'))
        else:
            self.__dict__['_disable'] = None
        if self.getAttributeNS(EMPTY_NAMESPACE, 'overwrite'):
            self.__dict__['_overwrite'] = AttributeValueTemplate.AttributeValueTemplate(self.getAttributeNS(EMPTY_NAMESPACE, 'overwrite'))
        else:
            self.__dict__['_overwrite'] = None
        return

    def instantiate(self, context, processor):
        if self._file:
            processor.setMessageFile(self._file.evaluate(context))
        if self._disabled:
            processor._messagesEnabled = self._disabled.evaluate(context) == yes
        if self._overwrite == 'yes':
            f = open(name, 'w')
        else:
            f = open(name, 'a')
        return (context,)

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         new_state = (base_state, self._nss, self._name,self._overwrite,self._outputParams)
         return new_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state[0])
        self._nss = state[1]
        self._file = state[2]
        self._silent = state[3]
        return

    
ExtElements = {
    (FT_EXT_NAMESPACE, 'apply-templates'): FtApplyTemplates,
    (FT_EXT_NAMESPACE, 'output'): FtOutputElement,
    (FT_EXT_NAMESPACE, 'write-file'): WriteFileElement,
    (FT_EXT_NAMESPACE, 'message-output'): MessageOutputElement,
    }

