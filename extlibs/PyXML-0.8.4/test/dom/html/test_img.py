from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLImageElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    i = doc.createElement('IMG')

    print 'testing get/set'
    testAttribute(i,'lowSrc')
    testAttribute(i,'alt')
    testAttribute(i,'border')
    testAttribute(i,'height')
    testAttribute(i,'hspace')
    testIntAttribute(i,'isMap')
    testAttribute(i,'longDesc')
    testAttribute(i,'src')
    testAttribute(i,'useMap')
    testAttribute(i,'vspace')
    testAttribute(i,'width')

    i._set_align('left')
    rt = i._get_align()
    if rt != 'Left':
        error('get/set align failed')
    print 'get/set works'


if __name__ == '__main__':
    test()
