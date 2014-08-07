from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLObjectElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    o = doc.createElement('OBJECT')

    print 'testing get/set'
    testAttribute(o,'code');
    testAttribute(o,'archive');
    testAttribute(o,'border');
    testAttribute(o,'codeBase');
    testAttribute(o,'codeType');
    testAttribute(o,'data');
    testIntAttribute(o,'declare');
    testAttribute(o,'height');
    testAttribute(o,'hspace');
    testAttribute(o,'standby');
    testIntAttribute(o,'tabIndex');
    testAttribute(o,'type');
    testAttribute(o,'useMap');
    testAttribute(o,'vspace');
    testAttribute(o,'width');
    o._set_align('left')
    rt = o._get_align()
    if rt != 'Left':
        error('get/set align failed')
    print 'get/set works'


if __name__ == '__main__':
    test()
