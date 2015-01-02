from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLHRElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    h = doc.createElement('HR')

    print 'testing get/set'
    h._set_align('left')
    rt = h._get_align()
    if rt != 'Left':
        error('get/set align failed')
    testIntAttribute(h,'noShade')
    testAttribute(h,'size')
    testAttribute(h,'width')
    print 'get/set works'

if __name__ == '__main__':

    test();
