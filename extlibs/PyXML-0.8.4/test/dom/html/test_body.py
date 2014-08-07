from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLBodyElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')

    b = doc.createElement('Body');

    print 'testing get/set '
    testAttribute(b,'aLink');
    testAttribute(b,'background');
    testAttribute(b,'bgColor');
    testAttribute(b,'link');
    testAttribute(b,'text');
    testAttribute(b,'vLink');
    print 'get/set works'


if __name__ == '__main__':
    test();
