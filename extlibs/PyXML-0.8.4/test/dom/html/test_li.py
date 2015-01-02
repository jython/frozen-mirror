from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLLIElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    l = doc.createElement('LI')

    print 'testing get/set'

    testAttribute(l,'type')
    testIntAttribute(l,'value')

    print 'get/set works'


if __name__ == '__main__':
    test()
