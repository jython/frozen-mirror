"""
A basic example of using the DOM to create an HTML document from scratch.
Also demonstrates creation of HTML forms
"""

from xml.dom import ext
from xml.dom import implementation

if __name__ == '__main__':

    #create a concrete HTMLDocument instance.
    doc = implementation.createHTMLDocument('A Basic HTML Document')

    #add in body
    doc.body = doc.createElement('Body')

    #Create a form
    form = doc.createElement('Form')

    #Create some text.  Note: every character is represented in some
    #DOM object.  All text (even between tags) is in a text node
    t = doc.createTextNode('Employee Name:')

    #Create an input tag
    i = doc.createElement('Input')

    #All elements can have attributes directly set
    i.setAttribute('TYPE','TEXT')

    #Some have helper functions defined.
    #This one sets the SIZE attribute to 20
    #Note that the argument must be a string.  4DOM closely
    #follows the DOM spec for the type of the arguments, even
    #when the spec is inconsistent or counter-intuitive
    i.size = '20'

    #This sets the NAME attribute
    i.name = 'EmployeeName'

    #Set the form's ACTION attribute
    form.action = '/cgi-local/test.py'

    #this inserts i as the last child in the form
    form.appendChild(i)

    #Insert t before i in form's child list
    form.insertBefore(t,i)

    #add the form to the document's body.  Note that you can't
    #add child elements directly to the document.
    doc.body.appendChild(form)

    #This prints out the text representation of the HTML document
    ext.PrettyPrint(doc)
