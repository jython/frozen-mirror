from xml.dom import Node, ext
from xml.dom.ext.reader import PyExpat

test_doc = """<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>LADIES</title></head>
<body>
<h1>LADIES</h1>
<h2><a name="A">Agathas</a></h2>
Four and forty lovers had Agathas in the old days,...
<h2><a name="B">Young Lady</a></h2>
I have fed your lar with poppies,...
<h2><a name="C">Lesbia Illa</a></h2>
Memnon, Memnon, that lady...
</body>
</html>
"""

def link_title_invert():
    #build a DOM tree from the file
    reader = PyExpat.Reader()
    doc = reader.fromString(test_doc)

    h2_elements = doc.getElementsByTagNameNS('http://www.w3.org/1999/xhtml', 'h2')
    for e in h2_elements:
        parent = e.parentNode
        a_list = filter(lambda x: (x.nodeType == Node.ELEMENT_NODE) and (x.localName == 'a'), e.childNodes)
        a = a_list[0]
        e.removeChild(a)
        for node in a.childNodes:
            #Automatically also removes the child from a
            e.appendChild(node)
        parent.replaceChild(a, e)
        a.appendChild(e)

    ext.Print(doc)

    #reclaim the object; not necessary with Python 2.0
    reader.releaseNode(doc)

if __name__ == '__main__':
    import sys
    link_title_invert()
