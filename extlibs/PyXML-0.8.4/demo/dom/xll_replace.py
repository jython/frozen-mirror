"""
Demonstrates some advanced DOM manipulation.
This function looks for simple XLinks and replaces the node containing
such links with the contents of the referenced document.
"""

from xml.dom import Node
from xml.dom.NodeFilter import NodeFilter
from xml.dom import ext
from xml.dom.ext.reader import PyExpat

def XllReplace(start_node):
    reader = PyExpat.Reader()
    owner_doc = start_node.ownerDocument
    snit = owner_doc.createNodeIterator(start_node, NodeFilter.SHOW_ELEMENT, None, 0)
    curr_node = snit.nextNode()
    while curr_node:
        #Only empty nodes are allowed to have Links
        if not curr_node.childNodes.length and curr_node.attributes:
            is_link = 0
            href = None
            for k in curr_node.attributes.keys():
                if (curr_node.attributes[k].localName, curr_node.attributes[k].namespaceURI) == ("link", "http://www.w3.org/XML/XLink/0.9"):
                    is_link = 1
                elif (curr_node.attributes[k].localName, curr_node.attributes[k].namespaceURI) == ("href", "http://www.w3.org/XML/XLink/0.9"):
                    href = curr_node.attributes[k].value
            if is_link and href:
               #Then make a tree of the new file and insert it
                f = open(href, "r")
                st = f.read()
                new_df = reader.fromString(st, ownerDoc=start_node.ownerDocument)

                #Get the first element node and assume it's the document node
                for a_node in new_df.childNodes:
                    if a_node.nodeType == Node.ELEMENT_NODE:
                        doc_root = a_node
                        break
                curr_node.parentNode.replaceChild(doc_root, curr_node)
        curr_node = snit.nextNode()

    return start_node

if __name__ == "__main__":
    import sys
    reader = PyExpat.Reader()
    xml_dom_tree = reader.fromUri(sys.argv[1])
    XllReplace(xml_dom_tree)
    ext.PrettyPrint(xml_dom_tree)
    reader.releaseNode(xml_dom_tree)
