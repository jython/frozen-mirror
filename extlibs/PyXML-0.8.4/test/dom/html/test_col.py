from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLTableColElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    c = doc.createElement('COL');

    print 'testing get/set'
    testAttribute(c,'ch');
    testAttribute(c,'chOff');
    testIntAttribute(c,'span');
    testAttribute(c,'width');

    c._set_align('left')
    rt = c._get_align()
    if rt != 'Left':
        error('get/set align failed')

    c._set_vAlign('top')
    rt = c._get_vAlign()
    if rt != 'Top':
        error('get/set vAlign failed')

    print 'get/set works'


if __name__ == '__main__':

    test();
