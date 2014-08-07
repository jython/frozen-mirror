import Cyclops,sys

from xml.dom.ext.reader import Sax2
from xml.dom import ext
def test():

    data = sys.stdin.read()

    doc = Sax2.FromXml(data)

    b1 = doc.createElementNS("http://foo.com","foo:branch")
    c1 = doc.createElementNS("http://foo.com","foo:child1")
    c2 = doc.createElementNS("http://foo.com","foo:child2")

    b1.setAttributeNS("http://foo.com","foo:a1","value-1")

    a1 = b1.getAttributeNodeNS("http://foo.com","a1")
    a1.value = "This shouldn't leak"

    b1.appendChild(c1)
    b1.appendChild(c2)

    doc.documentElement.appendChild(b1)

    r1 = doc.createElementNS("http://foo.com","foo:replace")
    doc.documentElement.replaceChild(r1,b1)

    b1.removeChild(c2)

    import cStringIO
    s = cStringIO.StringIO()
    import xml.dom.ext
    xml.dom.ext.Print(doc, stream = s)


    ext.ReleaseNode(doc)
    ext.ReleaseNode(b1)

    doc = Sax2.FromXml(data)
    ext.ReleaseNode(doc)



if __name__ == '__main__':
    cy = Cyclops.CycleFinder()
    cy.run(test)
    cy.find_cycles()
    cy.show_cycles()
