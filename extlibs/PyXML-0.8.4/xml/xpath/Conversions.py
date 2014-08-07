########################################################################
#
# File Name:   Conversions.py
#
#
"""
The implementation of all of the core functions for the XPath spec.
WWW: http://4suite.org/XPATH        e-mail: support@4suite.org

Copyright (c) 2000-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""

import string, cStringIO

from xml.dom import Node
from xml.xpath import ExpandedNameWrapper
from xml.xpath import NamespaceNode
from xml.xpath import NaN, Inf
from xml.xpath import Util
from xml.xpath import NAMESPACE_NODE
from xml.utils import boolean

import types
try:
    g_stringTypes= [types.StringType, types.UnicodeType]
except:
    g_stringTypes= [types.StringType]


def BooleanEvaluate(exp, context):
    rt = exp.evaluate(context)
    return BooleanValue(rt)


def StringValue(object):
#def StringValue(object, context=None):
    #print "StringValue context", context
    #if context:
    #    cache = context.stringValueCache
    #else:
    #    cache = None
    for func in g_stringConversions:
        #handled, result = func(object, cache)
        handled, result = func(object)
        if handled:
            break
    else:
        result = None
    return result


def BooleanValue(object):
    for func in g_booleanConversions:
        handled, result = func(object)
        if handled:
            break
    else:
        result = None
    return result


def NumberValue(object):
    for func in g_numberConversions:
        handled, result = func(object)
        if handled:
            break
    else:
        result = None
    return result


def NodeSetValue(object):
    for func in g_nodeSetConversions:
        handled, result = func(object)
        if handled:
            break
    else:
        result = None
    return result


def CoreStringValue(object):
    """Get the string value of any object"""
    # See bottom of file for conversion functions
    result = _strConversions.get(type(object), _strUnknown)(object)
    return result is not None, result


def CoreNumberValue(object):
    """Get the number value of any object"""
    if type(object) in [type(1), type(2.3), type(4L)]:
        return 1, object
    elif boolean.IsBooleanType(object):
        return 1, int(object)
    #FIXME: This can probably be optimized
    object = StringValue(object)
    try:
        object = float(object)
    except:
        #Many platforms seem to have a problem with strtod() and NaN: reported on Windows and FreeBSD
        #object = float('NaN')
        if object == '':
            object = 0
        else:
            object = NaN
    return 1, object


CoreBooleanValue = lambda obj: (1, boolean.BooleanValue(obj, StringValue))

g_stringConversions = [CoreStringValue]
g_numberConversions = [CoreNumberValue]
g_booleanConversions = [CoreBooleanValue]
#g_nodeSetConversions = [CoreNodeSetValue]


# Conversion functions for converting objects to strings

def _strUnknown(object):
    # Allow for non-instance DOM node objects
    if hasattr(object, 'nodeType'):
        # Add this type to the mapping for next time through
        _strConversions[type(object)] = _strInstance
        return _strInstance(object)
    return

def _strInstance(object):
    if hasattr(object, 'stringValue'):
        return object.stringValue
    if hasattr(object, 'nodeType'):
        node_type = object.nodeType
        if node_type == Node.ELEMENT_NODE:
            # The concatenation of all text descendants
            text_elem_children = filter(lambda x:
                                        x.nodeType in [Node.TEXT_NODE, Node.ELEMENT_NODE, Node.CDATA_SECTION_NODE],
                                        object.childNodes)
            return reduce(lambda x, y:
                          CoreStringValue(x)[1] + CoreStringValue(y)[1],
                          text_elem_children,
                          '')
        if node_type in [Node.ATTRIBUTE_NODE, NAMESPACE_NODE]:
            return object.value
        if node_type in [Node.PROCESSING_INSTRUCTION_NODE, Node.COMMENT_NODE, Node.TEXT_NODE, Node.CDATA_SECTION_NODE]:
            return object.data
        if node_type == Node.DOCUMENT_NODE:
            # Use the String value of the document root
            return CoreStringValue(object.documentElement)
    return None
        
_strConversions = {
    types.StringType : str,
    types.IntType : str,
    types.LongType : lambda l: repr(l)[:-1],
    types.FloatType : lambda f: f is NaN and 'NaN' or '%g' % f,
    boolean.BooleanType : str,
    types.InstanceType : _strInstance,
    types.ListType : lambda x: x and _strConversions.get(type(x[0]), _strUnknown)(x[0]) or '',
}

if hasattr(types, 'UnicodeType'):
    _strConversions[types.UnicodeType] = unicode

try:
    from Ft.Lib import cDomlettec

    def _strElementInstance(object):
        if hasattr(object, 'stringValue'):
            return object.stringValue
        if object.nodeType == Node.ELEMENT_NODE:
            # The concatenation of all text descendants
            text_elem_children = filter(
                lambda x: x.nodeType in [Node.TEXT_NODE, Node.ELEMENT_NODE, Node.CDATA_SECTION_NODE],
                object.childNodes
                )
            return reduce(lambda x, y:
                          CoreStringValue(x)[1] + CoreStringValue(y)[1],
                          text_elem_children,
                          '')

    _strConversions.update({
        cDomlettec.DocumentType : lambda x: _strElementInstance(x.documentElement),
        cDomlettec.ElementType : _strElementInstance,
        cDomlettec.TextType : lambda x: x.data,
        cDomlettec.CommentType : lambda x: x.data,
        cDomlettec.ProcessingInstructionType : lambda x: x.data,
        cDomlettec.AttrType : lambda x: x.value,
        })
except ImportError:
    pass
