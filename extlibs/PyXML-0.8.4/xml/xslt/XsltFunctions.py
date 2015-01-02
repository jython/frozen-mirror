########################################################################
#
# File Name:   XsltFunctions.py
#
#

"""
WWW: http://4suite.org/XSLT        e-mail: support@4suite.org

Copyright (c) 1999-2000 FourThought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""

import cStringIO, os, re, urlparse, urllib
from xml.dom import EMPTY_NAMESPACE
import xml.dom.ext
from xml.dom import Node
from xml.dom.DocumentFragment import DocumentFragment
from xml.xpath import CoreFunctions, Conversions, Util, g_extFunctions
from xml.xslt import XsltException, Error, XSL_NAMESPACE
from xml.xslt import g_extElements
# from Ft.Lib import Uri


#  import os
#  BETA_DOMLETTE = os.environ.get("BETA_DOMLETTE")
#  if BETA_DOMLETTE:
#      from Ft.Lib import cDomlette
#      g_readerClass = cDomlette.RawExpatReader
#      g_domModule = cDomlette
#  else:
#      from Ft.Lib import pDomlette
#      g_readerClass = pDomlette.PyExpatReader
#      g_domModule = pDomlette


def Document(context, object, nodeSet=None):
    result = []

    baseUri = getattr(context.stylesheet, 'baseUri', '')
    #if baseUri: baseUri= baseUri + '/'
    if nodeSet:
        baseUri = getattr(nodeSet[0], 'baseUri', baseUri)

    if nodeSet is None:
        if type(object) == type([]):
            for curr_node in object:
                result = result + Document(
                    context, Conversions.StringValue(curr_node),
                    [curr_node]
                    )
        elif object == '':
            result = [context.stylesheet.ownerDocument]
            context.stylesheet.newSource(context.stylesheet.ownerDocument,
                                         context.processor)
            #Util.IndexDocument(context.stylesheet.ownerDocument)
        else:
            try:
                #FIXME: Discard fragments before checking for dupes
                uri = Conversions.StringValue(object)
                if context.documents.has_key(uri):
                    result = context.documents[uri]
                else:
                    try:
                        doc = context.stylesheet._docReader.fromUri(uri, baseUri=baseUri)
                    except:
                        raise
                    #Util.IndexDocument(doc)
                    context.stylesheet.newSource(doc, context.processor)
                    result = [doc]
            except IOError:
                pass
    elif type(nodeSet) == type([]):
        if type(object) == type([]):
            for curr_node in object:
                result = result + Document(
                    context,
                    Conversions.StringValue(curr_node),
                    nodeSet
                    )
        else:
            try:
                uri = Conversions.StringValue(object)
                #FIXME: Discard fragments before checking for dupes
                if context.documents.has_key(uri):
                    result = context.documents[uri]
                else:
                    doc = context.stylesheet._docReader.fromUri(uri, baseUri=baseUri)
                    #Util.IndexDocument(doc)
                    context.stylesheet.newSource(doc, context.processor)
                    result = [doc]
            except IOError:
                pass
    return result


def Key(context, qname, keyList):
    result = []
    name = Util.ExpandQName(Conversions.StringValue(qname),
                            namespaces=context.processorNss)
    if context.stylesheet.keys.has_key(name):
        a_dict = context.stylesheet.keys[name]
        if type(keyList) != type([]):
            keyList = [keyList]
        for key in keyList:
            key = Conversions.StringValue(key)
            result = result + a_dict.get(key, [])
    return result


def Current(context):
    return [context.currentNode]


def UnparsedEntityUri(context, name):
    if hasattr(context.node.ownerDoc, '_unparsedEntities') and context.node.ownerDoc._unparsedEntities.has_key(name):
        return context.node.ownerDoc._unparsedEntities[name]
    return ''


def GenerateId(context, nodeSet=None):
    if nodeSet is not None and type(nodeSet) != type([]):
        raise XsltException(Error.WRONG_ARGUMENT_TYPE)
    if not nodeSet:
        return 'id' + `id(context.node)`
    else:
        node = Util.SortDocOrder(nodeSet)[0]
        return 'id' + `id(node)`
        

def SystemProperty(context, qname):
    uri, lname = Util.ExpandQName(Conversions.StringValue(qname),
                                  namespaces=context.processorNss)
    if uri == XSL_NAMESPACE:
        if lname == 'version':
            return 1.0
        if lname == 'vendor':
            return "Fourthought Inc."
        if lname == 'vendor-url':
            return "http://4Suite.org"
    elif uri == 'http://xmlns.4suite.org/xslt/env-system-property':
        return os.environ.get(lname, '')
    elif uri == 'http://xmlns.4suite.org':
        if lname == 'version':
            return __version__
    return ''


def FunctionAvailable(context, qname):
    split_name = Util.ExpandQName(Conversions.StringValue(qname),
                                  namespaces=context.processorNss)
    if g_extFunctions.has_key(split_name) or CoreFunctions.CoreFunctions.has_key(split_name):
        return CoreFunctions.True(context)
    else:
        return CoreFunctions.False(context)


def ElementAvailable(context, qname):
    split_name = Util.ExpandQName(Conversions.StringValue(qname),
                                  namespaces=context.processorNss)
    if g_extElements.has_key(split_name) or CoreFunctions.CoreFunctions.has_key(split_name):
        return CoreFunctions.True(context)
    else:
        return CoreFunctions.False(context)


def XsltStringValue(object):
#def XsltStringValue(object, cache=None):
    #print "XsltStringValue cache", cache
    #if cache and cache.has_key(object):
        #print "found:", cache[object]
        #return cache[object]
    if hasattr(object, 'stringValue'):
        return 1, object.stringValue
    if hasattr(object, 'nodeType') and object.nodeType == Node.DOCUMENT_FRAGMENT_NODE:
        result = ''
        for node in object.childNodes:
            result = result + Conversions.CoreStringValue(node)[1]
        #if cache is not None: cache[object] = result
        return 1, result
    return 0, None

def XsltNumberValue(object):
    handled, value = XsltStringValue(object)
    if handled:
        return 1, Conversions.NumberValue(value)
    return 0, None

def XsltBooleanValue(object):
    handled, value = XsltStringValue(object)
    if handled:
        return 1, Conversions.BooleanValue(value)
    return 0, None

##0 decimal-separator
##1 grouping-separator
##2 infinity
##3 minus-sign
##4 NaN
##5 percent
##6 per-mille
##7 zero-digit
##8 digit
##9 pattern-separator

def FormatNumber(context, number, formatString, decimalFormatName=None):
    decimal_format = ''
    num = Conversions.NumberValue(number)
    format_string = Conversions.StringValue(formatString)
    if decimalFormatName is not None:
        split_name = Util.ExpandQName(decimalFormatName,
                                      namespaces=context.processorNss)
        decimal_format = context.stylesheet.decimalFormats[split_name]
    else:
        decimal_format = context.stylesheet.decimalFormats['']
    from Ft.Lib import routines
    result = routines.FormatNumber(num, format_string)
    return result


Conversions.g_stringConversions.insert(0, XsltStringValue)
Conversions.g_numberConversions.insert(0, XsltNumberValue)
Conversions.g_booleanConversions.insert(0, XsltBooleanValue)

ExtFunctions = {
    (EMPTY_NAMESPACE, 'document'): Document,
    (EMPTY_NAMESPACE, 'key'): Key,
    (EMPTY_NAMESPACE, 'current'): Current,
    (EMPTY_NAMESPACE, 'generate-id'): GenerateId,
    (EMPTY_NAMESPACE, 'system-property'): SystemProperty,
    (EMPTY_NAMESPACE, 'function-available'): FunctionAvailable,
    (EMPTY_NAMESPACE, 'element-available'): ElementAvailable,
    (EMPTY_NAMESPACE, 'string-value'): XsltStringValue,
    (EMPTY_NAMESPACE, 'format-number'): FormatNumber,
    (EMPTY_NAMESPACE, 'unparsed-entity-uri'): UnparsedEntityUri
    }

