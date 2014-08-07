########################################################################
#
# File Name:            __init__.py
#
#
"""
WWW: http://4suite.org/4XSLT         e-mail: support@4suite.org

Copyright (c) 2000, 2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

XSL_NAMESPACE='http://www.w3.org/1999/XSL/Transform'

import xml.dom
from xml import xpath
from xml.xpath import g_xpathRecognizedNodes

SyntaxException = xpath.SyntaxException
InternalException = SyntaxException # not used

g_extElements = {}
g_xsltRecognizedNodes = g_xpathRecognizedNodes + [xml.dom.Node.DOCUMENT_FRAGMENT_NODE]

# Define ReleaseNode in a DOM-independent way
import xml.dom.ext
import xml.dom.minidom
def _releasenode(n):
    if isinstance(n, xml.dom.minidom.Node):
        n.unlink()
    else:
        xml.dom.ext.ReleaseNode(n)

try:
    from Ft.Lib import pDomlette
    def ReleaseNode(n):
        if isinstance(n, pDomlette.Node):
            pDomlette.ReleaseNode(n)
        else:
            _releasenode(n)
    _XsltElementBase = pDomlette.Element
except ImportError:
    ReleaseNode = _releasenode
    from minisupport import _XsltElementBase

def RegisterExtensionModules(moduleNames, moduleList=g_extElements):
    mod_names = moduleNames[:]
    mods = []
    for mod_name in mod_names:
        module_used = 0
        if mod_name:
            mod = __import__(mod_name, {}, {}, ['ExtElements', 'ExtFunctions'])
            if hasattr(mod, 'ExtFunctions'):
                xpath.g_extFunctions.update(mod.ExtFunctions)
                module_used = 1
            if hasattr(mod, 'ExtElements'):
                moduleList.update(mod.ExtElements)
                module_used = 1
            module_used and mods.append(mod)
    return mods


class XsltException(Exception):
    def __init__(self, errorCode, *args):
        self.args = args
        self.errorCode = errorCode
        Exception.__init__(self, MessageSource.g_errorMessages[errorCode]%args)


class XsltElement(_XsltElementBase):
    def __init__(self, doc, uri, localName, prefix, baseUri):
        _XsltElementBase.__init__(self, doc, uri, localName, prefix)
        self.baseUri = baseUri

    def setup(self):
        self._nss = xml.dom.ext.GetAllNs(self)
        return

    def instantiate(self, context, processor):
        for child in self.childNodes:
            if (child.namespaceURI, child.localName) == (XSL_NAMESPACE, 'fallback'):
                child.instantiate(context, processor)
        return (context,)

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix, self.baseUri)

    def __getstate__(self):
         base_state = _XsltElementBase.__getstate__(self)
         new_state = (base_state, self.baseUri,)
         return new_state

         return base_state

    def __setstate__(self, state):
        _XsltElementBase.__setstate__(self, state[0])
        self.baseUri = state[1]
        return


class Error:
    INTERNAL_ERROR = 1
    PATTERN_SYNTAX = 2
    PATTERN_SEMANTIC = 3
    NO_STYLESHEET = 4
    AVT_SYNTAX = 5
    STYLESHEET_MISSING_VERSION = 6
    STYLESHEET_MISSING_VERSION_NOTE1 = 7
    STYLESHEET_PARSE_ERROR = 8
    SOURCE_PARSE_ERROR = 9

    TOP_LEVEL_ELEM_WITH_NULL_NS = 10
    XSLT_ILLEGAL_ATTR = 11
    XSLT_ILLEGAL_ELEMENT = 12
    STYLESHEET_ILLEGAL_ROOT = 13
    CIRCULAR_VAR = 14

    WHEN_AFTER_OTHERWISE = 111
    MULTIPLE_OTHERWISE = 112

    APPLYIMPORTS_WITH_NULL_CURR_TPL = 120

    #xsl:import
    ILLEGAL_IMPORT = 130

    #xsl:choose
    ILLEGAL_CHOOSE_CHILD = 140
    CHOOSE_REQUIRES_WHEN_CHILD = 141
    CHOOSE_WHEN_AFTER_OTHERWISE = 142
    CHOOSE_MULTIPLE_OTHERWISE = 143

    #xsl:call-template
    ILLEGAL_CALLTEMPLATE_CHILD = 150

    #xsl:template
    ILLEGAL_TEMPLATE_PRIORITY = 160

    #xsl:attribute
    ATTRIBUTE_ADDED_AFTER_ELEMENT = 170
    ATTRIBUTE_MISSING_NAME = 171

    #xsl:element
    UNDEFINED_ATTRIBUTE_SET = 180

    #xsl:for-each
    INVALID_FOREACH_SELECT = 190

    #xsl:value-of
    VALUEOF_MISSING_SELECT = 200

    #xsl:copy-of
    COPYOF_MISSING_SELECT = 210

    #xsl:text
    ILLEGAL_TEXT_CHILD = 220

    #xsl:apply-template
    ILLEGAL_APPLYTEMPLATE_CHILD = 230

    #xsl:when
    WHEN_MISSING_TEST = 240

    #xsl:attribute-set
    ILLEGAL_ATTRIBUTESET_CHILD = 250
    ATTRIBUTESET_REQUIRES_NAME = 251


    INVALID_PATTERN = 1000
    INVALID_OPERAND_IN_PATTERN = 1001
    INVALID_OPERAND_ID = 1002
    INVALID_OPERAND_SREL = 1003
    INVALID_OPERAND_REL = 1004
    INVALID_OPERAND_IDREL = 1005
    INVALID_LEFT_OR_RIGHT_OPERAND_S = 1006
    INVALID_LEFT_OR_RIGHT_OPERAND_RELP = 1007
    INVALID_AXIS_SPEC = 1008
    INVALID_NODE_TEST = 1009
    INVALID_PREDICATE_LIST = 1010

    ILLEGAL_SORT_DATA_TYPE_VALUE = 2010
    ILLEGAL_SORT_CASE_ORDER_VALUE = 2011
    ILLEGAL_SORT_ORDER_VALUE = 2012
    
    ILLEGAL_NUMBER_GROUPING_SIZE_VALUE = 2020
    ILLEGAL_NUMBER_LEVEL_VALUE = 2021
    ILLEGAL_NUMBER_LETTER_VALUE_VALUE = 2022
    ILLEGAL_NUMBER_FORMAT_VALUE = 2023

    INVALID_NAMESPACE_ALIAS = 2030

    WRONG_NUMBER_OF_ARGUMENTS = 5000
    WRONG_ARGUMENT_TYPE = 5001

    RESTRICTED_OUTPUT_VIOLATION = 7000

    FEATURE_NOT_SUPPORTED = 9999

    STYLESHEET_REQUESTED_TERMINATION = 10000


class OutputParameters:
    def __init__(self):
        #Initialize with defaults according to spec
        self.method = None
        self.version = "1.0"
        self.encoding = ""
        self.omitXmlDeclaration = 'no'
        self.standalone = None
        self.doctypeSystem = ''
        self.doctypePublic = ''
        self.mediaType = None
        self.cdataSectionElements = []
        self.indent = None


g_registered = 0

def Register():
    import os,string
    from xml.xslt import XsltFunctions, BuiltInExtElements
    xpath.g_extFunctions.update(XsltFunctions.ExtFunctions)
    if os.environ.has_key('EXTMODULES'):
        RegisterExtensionModules(
            string.split(os.environ["EXTMODULES"], ':')
            )
    g_extElements.update(BuiltInExtElements.ExtElements)
    global g_registered
    g_registered = 1

def Init():
    pass

Init()

import MessageSource

