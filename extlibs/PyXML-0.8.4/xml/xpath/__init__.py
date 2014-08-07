########################################################################
#
# File Name:            __init__.py
#
#
"""
WWW: http://4suite.org/4XPath         e-mail: support@4suite.org

Copyright (c) 2000-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""

NAMESPACE_NODE = 10000
FT_OLD_EXT_NAMESPACE = 'http://xmlns.4suite.org/xpath/extensions'
FT_EXT_NAMESPACE = 'http://xmlns.4suite.org/ext'

# Simple trick (thanks Tim Peters) to enable crippled IEEE 754 support
# until ANSI C (or Python) sorts it all out...
Inf = Inf = 1e300 * 1e300
NaN = Inf - Inf

from xml.dom import Node
from xml.FtCore import FtException

g_xpathRecognizedNodes = [
        Node.ELEMENT_NODE,
        Node.ATTRIBUTE_NODE,
        Node.TEXT_NODE,
        Node.CDATA_SECTION_NODE,
        Node.DOCUMENT_NODE,
        Node.PROCESSING_INSTRUCTION_NODE,
        Node.COMMENT_NODE
        ]

g_extFunctions = {}

class CompiletimeException(FtException):
    INTERNAL = 1
    SYNTAX = 2
    PROCESSING = 3

    def __init__(self, errorCode, *args):
        FtException.__init__(self, errorCode, MessageSource.COMPILETIME, args)

class RuntimeException(FtException):
    INTERNAL = 1
    NO_CONTEXT = 10
    UNDEFINED_VARIABLE = 100
    UNDEFINED_PREFIX = 101
    WRONG_ARGUMENTS = 200

    def __init__(self, errorCode, *args):
        FtException.__init__(self, errorCode, MessageSource.RUNTIME, args)

from XPathParserBase import SyntaxException

import MessageSource

def Evaluate(expr, contextNode=None, context=None):
    import os
    if os.environ.has_key('EXTMODULES'):
        RegisterExtensionModules(os.environ["EXTMODULES"].split(':'))

    if context:
        con = context
    elif contextNode:
        con = Context.Context(contextNode, 0, 0)
    else:
        raise RuntimeException(RuntimeException.NO_CONTEXT_ERROR)
    retval = parser.new().parse(expr).evaluate(con)
    return retval


def Compile(expr):
    try:
        return parser.new().parse(expr)
    except SyntaxError, error:
        raise CompiletimeException(CompiletimeException.SYNTAX, str(error))
    except:
        import traceback, cStringIO
        stream = cStringIO.StringIO()
        traceback.print_exc(None, stream)
        raise RuntimeException(RuntimeException.INTERNAL, stream.getvalue())


def CreateContext(contextNode):
    return Context.Context(contextNode, 0, 0)


def RegisterExtensionModules(moduleNames):
    mod_names = moduleNames[:]
    mods = []
    for mod_name in mod_names:
        if mod_name:
            mod = __import__(mod_name,{},{},['ExtFunctions'])
            if hasattr(mod,'ExtFunctions'):
                g_extFunctions.update(mod.ExtFunctions)
                mods.append(mod)
    return mods


#Allow access to the NormalizeNode function
from Util import NormalizeNode

import Context

try:
    import XPathParserc
except ImportError:
    #import XPathParser
    #parser = XPathParser
    from pyxpath import ExprParserFactory
    parser = ExprParserFactory
else:
    parser = XPathParserc


def Init():
    from xml.xpath import BuiltInExtFunctions
    g_extFunctions.update(BuiltInExtFunctions.ExtFunctions)


Init()
