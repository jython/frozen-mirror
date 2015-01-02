from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLAnchorElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    a = doc.createElement('A')

    print 'testing get/set'
    testAttribute(a,'accessKey')
    testAttribute(a,'charset')
    testAttribute(a,'coords')
    testAttribute(a,'href')
    testAttribute(a,'hreflang')
    testAttribute(a,'rel')
    testAttribute(a,'rev')
    testIntAttribute(a,'tabIndex')
    testAttribute(a,'target')
    testAttribute(a,'type')
    a._set_shape('rect')
    rt = a._get_shape()
    if rt != 'Rect':
        error('get/set shape failed')
    print 'get/set works'

if __name__ == '__main__':
    test()
