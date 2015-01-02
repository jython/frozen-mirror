from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLFieldSetElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    f = doc.createElement('FieldSet');


if __name__ == '__main__':

    test();
