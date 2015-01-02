from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLFontElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    f = doc.createElement('Font');

    print 'testing get/set'
    testAttribute(f,'color');
    testAttribute(f,'face');
    testAttribute(f,'size');
    print 'get/set works'

if __name__ == '__main__':

    test();
