from util import testAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLQuoteElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    q = doc.createElement('Q')

    print 'testing get/set'
    testAttribute(q,'cite')
    print 'get/set works'


if __name__ == '__main__':
    test();
