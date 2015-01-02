"""
A basic example of using the DOM to create an XML document from scratch.
"""


from xml.dom import ext
from xml.dom import implementation

if __name__ == '__main__':

    #Create a doctype using document type name, sysid and pubid
    dt = implementation.createDocumentType('mydoc', '', '')

    #Create a document using document element namespace URI, doc element
    #name and doctype.  This automatically creates a document element
    #which is the single element child of the document
    doc = implementation.createHTMLDocument('', 'mydoc', dt)

    #Get the document element
    doc_elem = doc.documentElement

    #Create an element: the Document instanmce acts as a factory
    new_elem = doc.createElementNS('', 'spam')

    #Create an attribute on the new element
    new_elem.setAttributeNS('', 'eggs', 'sunnysideup')

    #Create a text node
    new_text = doc.createTextNode('some text here...')

    #Add the new text node to the new element
    new_elem.appendChild(new_text)

    #Add the new element to the document element
    doc_elem.appendChild(new_elem)

    #Print out the resulting document
    import xml.doc.ext
    xml.doc.ext.Print(doc)
