from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLModElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    m = doc.createElement('ins')

    print 'testing get/set'
    testAttribute(m,'cite')
    testAttribute(m,'dateTime')
    print 'get/set works'


if __name__ == '__main__':
    test()
