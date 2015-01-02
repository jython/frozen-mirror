from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLBaseElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    b = doc.createElement('Base')

    print 'testing get/set attributes'
    testAttribute(b,'href')
    testAttribute(b,'target')
    print 'get/set works'

if __name__ == '__main__':
    test()
