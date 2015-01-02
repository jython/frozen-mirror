from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLLabelElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    l = doc.createElement('LABEL')

    print 'testing get/set attributes'

    testAttribute(l,'accessKey')
    testAttribute(l,'htmlFor')
    print 'get/set works'


if __name__ == '__main__':
    test()
