from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLMenuElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    m = doc.createElement('MENU')

    print 'testing get/set'
    testIntAttribute(m,'compact')
    print 'get/set works'


if __name__ == '__main__':
    test()
