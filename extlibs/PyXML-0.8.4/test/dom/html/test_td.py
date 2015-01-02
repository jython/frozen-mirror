from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLTableCellElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    c = doc.createElement('TD')

    print 'testing get/set'
    testAttribute(c,'abbr');
    testAttribute(c,'axis');
    testAttribute(c,'bgColor');
    testAttribute(c,'ch');
    testAttribute(c,'chOff');
    testIntAttribute(c,'colSpan');
    testAttribute(c,'headers');
    testAttribute(c,'height');
    testIntAttribute(c,'noWrap');
    testIntAttribute(c,'rowSpan');
    testAttribute(c,'width');
    print 'get/set works'
    c._set_align('left')
    rt = c._get_align()
    if rt != 'Left':
        error('get/set align failed')
    c._set_vAlign('top')
    rt = c._get_vAlign()
    if rt != 'Top':
        error('get/set align failed')
    c._set_scope('colgroup')
    rt = c._get_scope()
    if rt != 'Colgroup':
        error('get/set align failed')

    #getCells is tested in the TR test file


if __name__ == '__main__':
    test();
