########################################################################
#
# File Name:   CoreFunctions.py
#
#
"""
The implementation of all of the core functions for the XPath spec.
WWW: http://4suite.org/XPATH        e-mail: support@4suite.org

Copyright (c) 2000-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""

import string, cStringIO

from xml.dom import Node,EMPTY_NAMESPACE
from xml.xpath import ExpandedNameWrapper
from xml.xpath import NamespaceNode
from xml.xpath import NaN, Inf
from xml.xpath import Util, Conversions
from xml.xpath import NAMESPACE_NODE
from xml.xpath import CompiletimeException, RuntimeException
from xml.utils import boolean

from xml.FtCore import get_translator

_ = get_translator("xpath")


class Types:
    NumberType = 0
    StringType = 1
    BooleanType = 2
    NodeSetType = 3
    ObjectType = 4

import types
try:
    g_stringTypes = [types.StringType, types.UnicodeType]
except:
    g_stringTypes = [types.StringType]

### Node Set Functions ###

def Last(context):
    """Function: <number> last()"""
    return context.size


def Position(context):
    """Function: <number> position()"""
    return context.position


def Count(context, nodeSet):
    """Function: <number> count(<node-set>)"""
    if type(nodeSet) != type([]):
        raise RuntimeException(RuntimeException.WRONG_ARGUMENTS, 'count', _("expected node set argument"))
    return len(nodeSet)


def Id(context, object):
    """Function: <node-set> id(<object>)"""
    id_list = []
    if type(object) != type([]):
        st = Conversions.StringValue(object)
        id_list = string.split(st)
    else:
        for n in object:
            id_list.append(Conversions.StringValue(n))
    rt = []
    for id in id_list:
        doc = context.node.ownerDocument or context.node
        elements = Util.ElementsById(doc.documentElement, id)
        if len(elements) > 1:
            raise RuntimeException(RuntimeException.WRONG_ARGUMENTS, 'id', _("argument not unique"))
        elif elements:
            # Must be 1
            rt.append(elements[0])
    return rt


def LocalName(context, nodeSet=None):
    """Function: <string> local-name(<node-set>?)"""
    if nodeSet is None:
        node = context.node
    else:
        if type(nodeSet) != type([]):
            raise RuntimeException(RuntimeException.WRONG_ARGUMENTS, 'local-name', _("expected node set"))
        nodeSet = Util.SortDocOrder(nodeSet)
        if type(nodeSet) != type([]) or len(nodeSet) == 0:
            return ''
        node = nodeSet[0]
    en = ExpandedName(node)
    if en == None or en.localName == None:
        return ''
    return en.localName


def NamespaceUri(context, nodeSet=None):
    """Function: <string> namespace-uri(<node-set>?)"""
    if nodeSet is None:
        node = context.node
    else:
        if type(nodeSet) != type([]):
            raise RuntimeException(RuntimeException.WRONG_ARGUMENTS, 'namespace-uri', _("expected node set"))
        nodeSet = Util.SortDocOrder(nodeSet)
        if type(nodeSet) != type([]) or len(nodeSet) == 0:
            return ''
        node = nodeSet[0]
    en = ExpandedName(node)
    if en == None or en.namespaceURI == None:
        return ''
    return en.namespaceURI


def Name(context, nodeSet=None):
    """Function: <string> name(<node-set>?)"""
    if nodeSet is None:
        node = context.node
    else:
        if type(nodeSet) != type([]):
            raise RuntimeException(RuntimeException.WRONG_ARGUMENTS, 'name', _("expected node set"))
        nodeSet = Util.SortDocOrder(nodeSet)
        if type(nodeSet) != type([]) or len(nodeSet) == 0:
            return ''
        node = nodeSet[0]
    en = ExpandedName(node)
    if en == None:
        return ''
    return en.qName


### String Functions ###

def String(context, object=None):
    """Function: <string> string(<object>?)"""
    if type(object) in g_stringTypes:
        return object
    if object is None:
        object = [context.node]
    return Conversions.StringValue(object)


def Concat(context, *args):
    """Function: <string> concat(<string>, <string>, ...)"""
    if len(args) < 1:
        raise RuntimeException(RuntimeException.WRONG_ARGUMENTS, 'concat', _("at least 2 arguments expected"))
    return reduce(lambda a,b,c=context: a + Conversions.StringValue(b),
                  args, '')


def StartsWith(context, outer, inner):
    """Function: <string> starts-with(<string>, <string>)"""
    outer = Conversions.StringValue(outer)
    inner = Conversions.StringValue(inner)
    return outer[:len(inner)] == inner and boolean.true or boolean.false


def Contains(context, outer, inner):
    """Function: <string> contains(<string>, <string>)"""
    outer = Conversions.StringValue(outer)
    inner = Conversions.StringValue(inner)
    if len(inner) == 1:
        return inner in outer and boolean.true or boolean.false
    else:
        return string.find(outer, inner) != -1 and boolean.true or boolean.false


def SubstringBefore(context, outer, inner):
    """Function: <string> substring-before(<string>, <string>)"""
    outer = Conversions.StringValue(outer)
    inner = Conversions.StringValue(inner)
    index = string.find(outer, inner)
    if index == -1:
        return ''
    return outer[:index]


def SubstringAfter(context, outer, inner):
    """Function: <string> substring-after(<string>, <string>)"""
    outer = Conversions.StringValue(outer)
    inner = Conversions.StringValue(inner)
    index = string.find(outer, inner)
    if index == -1:
        return ''
    return outer[index+len(inner):]


def Substring(context, st, start, end=None):
    """Function: <string> substring(<string>, <number>, <number>?)"""
    st = Conversions.StringValue(st)
    start = Conversions.NumberValue(start)
    if start is NaN:
        return ''
    start = int(round(start))
    start = start > 1 and start - 1 or 0

    if end is None:
        return st[start:]
    end = Conversions.NumberValue(end)
    if start is NaN:
        return st[start:]
    end = int(round(end))
    return st[start:start+end]


def StringLength(context, st=None):
    """Function: <number> string-length(<string>?)"""
    if st is None:
        st = context.node
    return len(Conversions.StringValue(st))


def Normalize(context, st=None):
    """Function: <string> normalize-space(<string>?)"""
    if st is None:
        st = context.node
    st = Conversions.StringValue(st)
    return string.join(string.split(st))


def Translate(context, source, fromChars, toChars):
    """Function: <string> translate(<string>, <string>, <string>)"""
    source = Conversions.StringValue(source)
    fromChars = Conversions.StringValue(fromChars)
    toChars = Conversions.StringValue(toChars)

    # string.maketrans/translate do not handle unicode
    translate = {}
    for from_char, to_char in map(None, fromChars, toChars):
        translate[ord(from_char)] = to_char

    result = reduce(lambda a, b, t=translate:
                    a + (t.get(ord(b), b) or ''),
                    source, '')
    return result

### Boolean Functions ###

def _Boolean(context, object):
    """Function: <boolean> boolean(<object>)"""
    return Conversions.BooleanValue(object)


def Not(context, object):
    """Function: <boolean> not(<boolean>)"""
    return (not Conversions.BooleanValue(object) and boolean.true) or boolean.false


def True(context):
    """Function: <boolean> true()"""
    return boolean.true


def False(context):
    """Function: <boolean> false()"""
    return boolean.false


def Lang(context, lang):
    """Function: <boolean> lang(<string>)"""
    lang = string.upper(Conversions.StringValue(lang))
    node = context.node
    while node:
        lang_attr = filter(lambda x:x.name == 'xml:lang' and x.value, node.attributes.values())
        value = lang_attr and lang_attr[0].nodeValue or None
        if value:
            # See if there is a suffix
            index = string.find(value, '-')
            if index != -1:
                value = value[:index]
            value = string.upper(value)
            return value == lang and boolean.true or boolean.false
        node = node.nodeType == Node.ATTRIBUTE_NODE and node.ownerElement or node.parentNode
    return boolean.false

### Number Functions ###

def Number(context, object=None):
    """Function: <number> number(<object>?)"""
    if object is None:
        object = [context.node]
    return Conversions.NumberValue(object)


def Sum(context, nodeSet):
    """Function: <number> sum(<node-set>)"""
    nns = map(lambda x: Conversions.NumberValue(x), nodeSet)
    return reduce(lambda x,y: x+y, nns, 0)


def Floor(context, number):
    """Function: <number> floor(<number>)"""
    number = Conversions.NumberValue(number)
    #if type(number) in g_stringTypes:
    #    number = string.atof(number)        
    if int(number) == number:
        return number
    elif number < 0:
        return int(number) - 1
    else:
        return int(number)


def Ceiling(context, number):
    """Function: <number> ceiling(<number>)"""
    number = Conversions.NumberValue(number)
    #if type(number) in g_stringTypes:
    #    number = string.atof(number)
    if int(number) == number:
        return number
    elif number > 0:
        return int(number) + 1
    else:
        return int(number)


def Round(context, number):
    """Function: <number> round(<number>)"""
    number = Conversions.NumberValue(number)
    return round(number, 0)

### Helper Functions ###

def ExpandedName(node):
    """Get the expanded name of any object"""
    if hasattr(node, 'nodeType') and node.nodeType in [Node.ELEMENT_NODE, Node.PROCESSING_INSTRUCTION_NODE, Node.ATTRIBUTE_NODE, NAMESPACE_NODE]:
        return ExpandedNameWrapper.ExpandedNameWrapper(node)
    return None


### Function Mappings ###

CoreFunctions = {
    (EMPTY_NAMESPACE, 'last'): Last,
    (EMPTY_NAMESPACE, 'position'): Position,
    (EMPTY_NAMESPACE, 'count'): Count,
    (EMPTY_NAMESPACE, 'id'): Id,
    (EMPTY_NAMESPACE, 'local-name'): LocalName,
    (EMPTY_NAMESPACE, 'namespace-uri'): NamespaceUri,
    (EMPTY_NAMESPACE, 'name'): Name,
    (EMPTY_NAMESPACE, 'string'): String,
    (EMPTY_NAMESPACE, 'concat'): Concat,
    (EMPTY_NAMESPACE, 'starts-with'): StartsWith,
    (EMPTY_NAMESPACE, 'contains'): Contains,
    (EMPTY_NAMESPACE, 'substring-before'): SubstringBefore,
    (EMPTY_NAMESPACE, 'substring-after'): SubstringAfter,
    (EMPTY_NAMESPACE, 'substring'): Substring,
    (EMPTY_NAMESPACE, 'string-length'): StringLength,
    (EMPTY_NAMESPACE, 'normalize-space'): Normalize,
    (EMPTY_NAMESPACE, 'translate'): Translate,
    (EMPTY_NAMESPACE, 'boolean'): _Boolean,
    (EMPTY_NAMESPACE, 'not'): Not,
    (EMPTY_NAMESPACE, 'true'): True,
    (EMPTY_NAMESPACE, 'false'): False,
    (EMPTY_NAMESPACE, 'lang'): Lang,
    (EMPTY_NAMESPACE, 'number'): Number,
    (EMPTY_NAMESPACE, 'sum'): Sum,
    (EMPTY_NAMESPACE, 'floor'): Floor,
    (EMPTY_NAMESPACE, 'ceiling'): Ceiling,
    (EMPTY_NAMESPACE, 'round'): Round,
    (EMPTY_NAMESPACE, 'expanded-name'): ExpandedName
    }

Args = {
    Substring : (Types.StringType, [Types.StringType, Types.StringType]),
    }
