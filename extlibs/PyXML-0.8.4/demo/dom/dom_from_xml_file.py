from xml.dom import ext
from xml.dom.ext.reader import PyExpat

def read_xml_from_file(fileName):
    #build a DOM tree from the file
    reader = PyExpat.Reader()
    xml_dom_object = reader.fromUri(fileName)

    ext.Print(xml_dom_object)

    #reclaim the object
    reader.releaseNode(xml_dom_object)

if __name__ == '__main__':
    import sys
    read_xml_from_file(sys.argv[1])
