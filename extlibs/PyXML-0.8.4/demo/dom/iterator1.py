"""Demonstrates basic walking using DOM level 2 iterators"""

from xml.dom.ext.reader import PyExpat
from xml.dom.NodeFilter import NodeFilter

def Iterate(xml_dom_object):
    print "Printing all nodes:"
    nit = xml_dom_object.ownerDocument.createNodeIterator(xml_dom_object, NodeFilter.SHOW_ALL, None, 0)

    curr_node =  nit.nextNode()
    while curr_node:
        print "%s node %s\n"%(curr_node.nodeType, curr_node.nodeName)
        curr_node =  nit.nextNode()

    print "\n\n\nPrinting only element nodes:"
    snit = xml_dom_object.ownerDocument.createNodeIterator(xml_dom_object, NodeFilter.SHOW_ELEMENT, None, 0)

    curr_node =  snit.nextNode()
    while curr_node:
        print "%s node %s\n"%(curr_node.nodeType, curr_node.nodeName)
        curr_node = snit.nextNode()


if __name__ == '__main__':
    import sys
    reader = PyExpat.Reader()
    xml_dom_object = reader.fromUri(sys.argv[1])
    Iterate(xml_dom_object)
    reader.releaseNode(xml_dom_object)
