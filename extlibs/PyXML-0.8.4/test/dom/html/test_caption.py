from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLTableCaptionElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    c = doc.createElement('Caption')

    print 'testing get/set'
    c._set_align('left')
    rt = c._get_align()
    if rt != 'Left':
        error('get/set align failed')
    print 'get/set works'


if __name__ == '__main__':

    test();
