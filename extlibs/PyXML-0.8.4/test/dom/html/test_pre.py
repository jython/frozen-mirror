from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLPreElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    p = doc.createElement('PRE')

    print 'testing get/set'
    testIntAttribute(p,'width')
    print 'get/set works'


if __name__ == '__main__':
    test()
