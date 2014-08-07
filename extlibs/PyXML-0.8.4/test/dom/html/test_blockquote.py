from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLQuoteElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    b = doc.createElement('BlockQuote');

    print 'testing get/set'
    testAttribute(b,'cite');
    print 'get/set works'


if __name__ == '__main__':

    test();
