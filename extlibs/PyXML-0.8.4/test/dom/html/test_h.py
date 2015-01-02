from util import testAttribute, error
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLHeadingElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    h = doc.createElement('H1')

    print 'testing get/set'
    h._set_align('left')
    rt = h._get_align()
    if rt != 'Left':
        error('get/set align failed')
    print 'get/set works'

if __name__ == '__main__':
    test()
