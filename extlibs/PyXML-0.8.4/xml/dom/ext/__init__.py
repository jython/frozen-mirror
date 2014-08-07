########################################################################
#
# File Name:            __init__.py
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

"""Some Helper functions: 4DOM/PyXML-specific Extensions to the DOM,
and DOM-related utilities."""

import sys,string

from xml.dom import Node
from xml.dom.NodeFilter import NodeFilter
from xml.dom import XML_NAMESPACE, XMLNS_NAMESPACE, DOMException
from xml.dom.html import HTML_4_TRANSITIONAL_INLINE
from c14n import Canonicalize
import re


import types
if (sys.hexversion >> 8) > 0x10502:
    IsDOMString = lambda s: type(s) in [types.StringType, types.UnicodeType]
else:
    IsDOMString = lambda s: type(s) == types.StringType

class FtDomException(DOMException):
    def __init__(self, *args):
        apply(DOMException.__init__,(self,)+ args)
        return


NodeTypeDict = {
    Node.ELEMENT_NODE : "Element",
    Node.ATTRIBUTE_NODE : "Attr",
    Node.TEXT_NODE : "Text",
    Node.CDATA_SECTION_NODE : "CDATASection",
    Node.ENTITY_REFERENCE_NODE : "EntityReference",
    Node.ENTITY_NODE : "Entity",
    Node.PROCESSING_INSTRUCTION_NODE : "ProcessingInstruction",
    Node.COMMENT_NODE : "Comment",
    Node.DOCUMENT_NODE : "Document",
    Node.DOCUMENT_TYPE_NODE : "DocumentType",
    Node.DOCUMENT_FRAGMENT_NODE : "DocumentFragment",
    Node.NOTATION_NODE : "Notation"
    }


def NodeTypeToClassName(nodeType):
    return NodeTypeDict[nodeType]


def Print(root, stream=sys.stdout, encoding='UTF-8'):
    if not hasattr(root, "nodeType"):
        return
    from xml.dom.ext import Printer
    nss = SeekNss(root)
    visitor = Printer.PrintVisitor(stream, encoding, nsHints=nss)
    Printer.PrintWalker(visitor, root).run()
    return


def PrettyPrint(root, stream=sys.stdout, encoding='UTF-8', indent='  ',
                preserveElements=None):
    if not hasattr(root, "nodeType"):
        return
    from xml.dom.ext import Printer
    nss_hints = SeekNss(root)
    preserveElements = preserveElements or []
    owner_doc = root.ownerDocument or root
    if hasattr(owner_doc, 'getElementsByName'):
        #We don't want to insert any whitespace into HTML inline elements
        preserveElements = preserveElements + HTML_4_TRANSITIONAL_INLINE
    visitor = Printer.PrintVisitor(stream, encoding, indent,
                                   preserveElements, nss_hints)
    Printer.PrintWalker(visitor, root).run()
    stream.write('\n')
    return


def XHtmlPrettyPrint(root, stream=sys.stdout, encoding='UTF-8', indent='  '):
    if not hasattr(root, "nodeType"):
        return

    from xml.dom.ext import XHtmlPrinter
    visitor = XHtmlPrinter.XHtmlPrintVisitor(stream, encoding, indent)
    Printer.PrintWalker(visitor, root).run()
    stream.write('\n')
    return


def XHtmlPrint(root, stream=sys.stdout, encoding='UTF-8'):
    XHtmlPrettyPrint(root, stream, encoding, '')


def ReleaseNode(node):
    cn = node.childNodes[:]
    for child in cn:
        if child.nodeType == Node.ELEMENT_NODE:
            ReleaseNode(child)
        node.removeChild(child)

    if node.nodeType == Node.ELEMENT_NODE:
        for ctr in range(node.attributes.length):
            attr = node.attributes.item(0)
            node.removeAttributeNode(attr)
            ReleaseNode(attr)


def StripHtml(startNode, preserveElements=None):
    '''
    Remove all text nodes in a given tree that do not have at least one
    non-whitespace character, taking into account special HTML elements
    '''
    preserveElements = preserveElements or []
    preserveElements = preserveElements + HTML_4_TRANSITIONAL_INLINE
    remove_list = []
    owner_doc = startNode.ownerDocument or startNode
    snit = owner_doc.createNodeIterator(startNode, NodeFilter.SHOW_TEXT,
                                        None, 0)
    curr_node = snit.nextNode()
    while curr_node:
        #first of all make sure it is not inside one of the preserve_elements
        ancestor = curr_node
        while ancestor != startNode:
            if ancestor.nodeType == Node.ELEMENT_NODE:
                if ancestor.nodeName in preserveElements:
                    break
                ancestor = ancestor.parentNode
            else:
                if not string.strip(curr_node.data):
                    remove_list.append(curr_node)
                ancestor = ancestor.parentNode
        curr_node = snit.nextNode()
    for node_to_remove in remove_list:
        node_to_remove.parentNode.removeChild(node_to_remove)
    return startNode


def StripXml(startNode, preserveElements=None):
    '''
    Remove all text nodes in a given tree that do not have at least one
    non-whitespace character, taking into account xml:space
    '''
    preserveElements = preserveElements or []
    remove_list = []
    owner_doc = startNode.ownerDocument or startNode
    snit = owner_doc.createNodeIterator(startNode, NodeFilter.SHOW_TEXT,
                                        None, 0)
    curr_node = snit.nextNode()
    while curr_node:
        #first of all make sure it is not inside xml:space='preserve'
        if XmlSpaceState(curr_node) != 'preserve':
            if not string.strip(curr_node.data):
                #also make sure it is not inside one of the preserve elements
                ancestor = curr_node
                while ancestor != startNode:
                    if ancestor.nodeType == Node.ELEMENT_NODE:
                        if ancestor.localName in preserveElements or (ancestor.namespaceURI, ancestor.localName) in preserveElements:
                            break
                    ancestor = ancestor.parentNode
                else:
                    remove_list.append(curr_node)
                    ancestor = ancestor.parentNode
        curr_node = snit.nextNode()
    for node_to_remove in remove_list:
        node_to_remove.parentNode.removeChild(node_to_remove)
    return startNode

_id_key = ('', 'ID')

def GetElementById(startNode, targetId):
    '''
    Return the element in the given tree with an ID attribute of the given
    value
    '''
    owner_doc = startNode.ownerDocument or startNode
    snit = owner_doc.createNodeIterator(startNode, NodeFilter.SHOW_ELEMENT,
                                        None, 0)
    curr_node = snit.nextNode()
    while curr_node:
        attr = curr_node.attributes.get(_id_key, None)
        if attr and attr._get_nodeValue() == targetId:
            return curr_node
        curr_node = snit.nextNode()
    return None


def XmlSpaceState(node):
    '''
    Return the valid value of the xml:space attribute currently in effect
    '''
    valid_values = ['', 'preserve', 'default']
    xml_space_found = 0
    root_reached = 0
    xml_space_state = ''
    while not(xml_space_state or root_reached):
        if node.nodeType == Node.ELEMENT_NODE:
            xml_space_state = node.getAttributeNS(XML_NAMESPACE, 'space')
            if xml_space_state not in valid_values: xml_space_state = ''
        parent_node = node.parentNode
        if not (parent_node and parent_node.nodeType == Node.ELEMENT_NODE):
            root_reached = 1
        node = parent_node
    return xml_space_state


def GetAllNs(node):
    #The xml namespace is implicit
    nss = {'xml': XML_NAMESPACE}
    if node.nodeType == Node.ATTRIBUTE_NODE and node.ownerElement:
        return GetAllNs(node.ownerElement)
    if node.nodeType == Node.ELEMENT_NODE:
        if node.namespaceURI:
            nss[node.prefix] = node.namespaceURI
        for attr in node.attributes.values():
            if attr.namespaceURI == XMLNS_NAMESPACE:
                if attr.localName == 'xmlns':
                    nss[None] = attr.value
                else:
                    nss[attr.localName] = attr.value
            elif attr.namespaceURI:
                nss[attr.prefix] = attr.namespaceURI
    if node.parentNode:
        #Inner NS/Prefix mappings take precedence over outer ones
        parent_nss = GetAllNs(node.parentNode)
        parent_nss.update(nss)
        nss = parent_nss
    return nss


#FIXME: this dict is a small memory leak: a splay tree that rotates out
#out of the tree would be perfect.
#g_splitNames = {}
def SplitQName(qname):
    """
    Input a QName according to XML Namespaces 1.0
    http://www.w3.org/TR/REC-xml-names
    Return the name parts according to the spec
    In the case of namespace declarations the tuple returned
    is (prefix, 'xmlns')
    Note that this won't hurt users since prefixes and local parts starting
    with "xml" are reserved, but it makes ns-aware builders easier to write
    """
    #sName = g_splitNames.get(qname)
    sName = None
    if sName == None:
        fields = string.splitfields(qname, ':')
        if len(fields) == 1:
            #Note: we could gain a tad more performance by interning 'xmlns'
            if qname == 'xmlns':
                sName = (None, 'xmlns')
            else:
                sName = (None, qname)
        elif len(fields) == 2:
            if fields[0] == 'xmlns':
                sName = (fields[1], 'xmlns')
            else:
                sName = (fields[0], fields[1])
        else:
            sname = (None, None)
        #g_splitNames[qname] = sName
    return sName


def SeekNss(node, nss=None):
    '''traverses the tree to seek an approximate set of defined namespaces'''
    nss = nss or {}
    for child in node.childNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            if child.namespaceURI:
                nss[child.prefix] = child.namespaceURI
            for attr in child.attributes.values():
                if attr.namespaceURI == XMLNS_NAMESPACE:
                    if attr.localName == 'xmlns':
                        nss[None] = attr.value
                    else:
                        nss[attr.localName] = attr.value
                elif attr.namespaceURI:
                    nss[attr.prefix] = attr.namespaceURI
            SeekNss(child, nss)
    return nss
