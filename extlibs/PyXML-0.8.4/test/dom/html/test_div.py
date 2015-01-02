from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLDivElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    d = doc.createElement('Div')

    print 'testing get/set'
    d._set_align('left')
    rt = d._get_align()
    if rt != 'Left':
        error('get/set of align failed')
    print 'get/set works'


if __name__ == '__main__':

    test();
