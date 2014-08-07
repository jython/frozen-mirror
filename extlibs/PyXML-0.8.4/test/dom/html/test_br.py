from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLBRElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    b = doc.createElement('BR');

    print 'testing get/set'
    b._set_clear('left')
    rt = b._get_clear()
    if rt != 'Left':
        error('get/set clear failed')

    print 'get/set works'


if __name__ == '__main__':

    test();
