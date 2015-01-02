########################################################################
#
# File Name:            Util.py
#
#
"""
General Utilities for XPath apps.
WWW: http://4suite.org/4XSLT        e-mail: support@4suite.org

Copyright (c) 2000-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""

import os, glob, string
import xml.dom.ext
from xml.dom import XML_NAMESPACE,EMPTY_NAMESPACE
from xml.dom import Node
from xml.dom.NodeFilter import NodeFilter
from xml.xpath import g_xpathRecognizedNodes, Compile

g_documentOrderIndex = {}

g_xmlSpaceDescendant = g_xmlSpaceAncestor = None


def ElementsById(element, name):
    elements = []
    attrs = element.attributes
    idattr = attrs.get((EMPTY_NAMESPACE, 'id')) or attrs.get((EMPTY_NAMESPACE, 'ID'))
    idattr and idattr.value == name and elements.append(idattr.ownerElement)
    for element in filter(lambda node: node.nodeType == Node.ELEMENT_NODE,
                          element.childNodes):
        elements.extend(ElementsById(element, name))
    return elements


def IndexDocument(doc):
    global g_documentOrderIndex
    if g_documentOrderIndex.has_key(id(doc)):
        return
    mapping = {}
    count = __IndexNode(doc, 0, mapping)
    g_documentOrderIndex[id(doc)] = mapping


def FreeDocumentIndex(doc):
    global g_documentOrderIndex
    if g_documentOrderIndex.has_key(id(doc)):
        del g_documentOrderIndex[id(doc)]


def SortDocOrder(nList):
    if len(nList) in [0, 1]:
        return nList
    if hasattr(nList[0], 'docIndex'):
        nList.sort(lambda a, b: cmp(a.docIndex, b.docIndex))
        return nList
    doc = nList[0].ownerDocument or nList[0]
    IndexDocument(doc)
    global g_documentOrderIndex
    if g_documentOrderIndex.has_key(id(doc)):
        rt = nList[:]
        rt.sort(IndexSort)
    else:
        rt = __recurseSort([doc], nList)
    return rt


def ExpandQName(qname, refNode=None, namespaces=None):
    '''
    Expand the given QName in the context of the given node,
    or in the given namespace dictionary
    '''
    nss = {}
    if refNode:
        nss = xml.dom.ext.GetAllNs(refNode)
    elif namespaces:
        nss = namespaces
    (prefix, local) = xml.dom.ext.SplitQName(qname)
    #We're not to use the default namespace
    if prefix != '':
        split_name = (nss[prefix], local)
    else:
        split_name = (EMPTY_NAMESPACE, local)
    return split_name


def __IndexNode(node, curIndex, mapping):
    if node.nodeType in g_xpathRecognizedNodes:
        #Add this node
        mapping[id(node)] = curIndex
        curIndex = curIndex + 1
        if node.nodeType == Node.ELEMENT_NODE:
            #FIXME how do we get attributes in doc order???
            for attr in node.attributes.values():
                mapping[id(attr)] = curIndex
                curIndex = curIndex + 1

        for childNode in node.childNodes:
            curIndex = __IndexNode(childNode, curIndex, mapping)

    return curIndex


def IndexSort(left, right):
    ldocId = id(left.ownerDocument or left)
    rdocId = id(right.ownerDocument or right)
    if ldocId == rdocId:
        lid = id(left)
        rid = id(right)
        return cmp(g_documentOrderIndex[ldocId][lid], g_documentOrderIndex[rdocId][rid])
    else:
        return cmp(ldocId, rdocId)


def __recurseSort(test, toSort):
    """Check whether any of the nodes in toSort are in the list test, and if so, sort them into the result list"""
    result = []
    for node in test:
        toSort = filter(lambda x, n=node: x != n, toSort)
        if node in toSort:
            result.append(node)
        #See if node has attributes
        if node.nodeType == Node.ELEMENT_NODE:
            attrList = node.attributes.values()
            #FIXME: Optimize by unrolling this level of recursion
            result = result + __recurseSort(attrList, toSort)
            if not toSort:
                #Exit early
                break
        #See if any of t's children are in toSort
        result = result + __recurseSort(node.childNodes, toSort)
        if not toSort:
            #Exit early
            break
    return result


def NormalizeNode(node):
    """NormalizeNode is used to prepare a DOM for XPath evaluation.

    1.  Convert CDATA Sections to Text Nodes.
    2.  Normalize all text nodes
    """
    node = node.firstChild
    while node:
        if node.nodeType == Node.CDATA_SECTION_NODE:
            # If followed by a text node, add this data to it
            if node.nextSibling and node.nextSibling.nodeType == Node.TEXT_NODE:
                node.nextSibling.insertData(0, node.data)
            elif node.data:
                # Replace this node with a new text node
                text = node.ownerDocument.createTextNode(node.data)
                node.parentNode.replaceChild(text, node)
                node = text
            else:
                # It is empty, get rid of it
                next = node.nextSibling
                node.parentNode.removeChild(node)
                node = next
                # Just in case it is None
                continue
        elif node.nodeType == Node.TEXT_NODE:
            next = node.nextSibling
            while next and next.nodeType in [Node.TEXT_NODE,
                                             Node.CDATA_SECTION_NODE]:
                node.appendData(next.data)
                node.parentNode.removeChild(next)
                next = node.nextSibling
            if not node.data:
                # Remove any empty text nodes
                next = node.nextSibling
                node.parentNode.removeChild(node)
                node = next
                # Just in case it is None
                continue
        elif node.nodeType == Node.ELEMENT_NODE:
            for attr in node.attributes.values():
                if len(attr.childNodes) > 1:
                    NormalizeNode(attr)
            NormalizeNode(node)
        node = node.nextSibling
    return

