'''
Walk through a namespace-compliant XML file and print out the
the namespaces of all elements and attributes in document order
'''

from xml.dom.ext.reader import PyExpat
from xml.dom.NodeFilter import NodeFilter

def TraceNs(doc):
    snit = doc.createNodeIterator(doc, NodeFilter.SHOW_ELEMENT, None, 0)
    curr_elem = snit.nextNode()
    while curr_elem:
        print "Current Element", curr_elem.nodeName
        #FIXME: put a GetDefaultNs method into Ext
        #ns = Namespace.GetDefaultNs(curr_elem)
        #print "\tDefault NS\t", ns
        print "\t"+curr_elem.nodeName+"\t\t", curr_elem.namespaceURI

        header_printed = 0

        for k in curr_elem.attributes.keys():
            if curr_elem.attributes[k].namespaceURI:
                if not header_printed:
                    header_printed = 1
                    print "\tAttributes"
                print "\t\t"+curr_elem.attributes[k].nodeName+"\t", curr_elem.attributes[k].namespaceURI

        print
        curr_elem = snit.nextNode()


if __name__ == "__main__":
    import sys
    reader = PyExpat.Reader()
    doc = reader.fromUri(sys.argv[1])
    TraceNs(doc)
    reader.releaseNode(doc)
