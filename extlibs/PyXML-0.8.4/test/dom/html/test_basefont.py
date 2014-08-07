from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLBaseFontElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    b = doc.createElement('BaseFont')

    print 'testing get/set'
    testAttribute(b,'color');
    testAttribute(b,'face');
    testAttribute(b,'size');
    print 'get/set works'

if __name__ == '__main__':

    test();
