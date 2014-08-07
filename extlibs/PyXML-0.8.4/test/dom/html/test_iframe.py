from util import testAttribute, error
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLIFrameElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    f = doc.createElement('IFrame')

    print 'testing get/set'
    testAttribute(f,'height');
    testAttribute(f,'longDesc');
    testAttribute(f,'marginHeight');
    testAttribute(f,'marginWidth');
    testAttribute(f,'src');
    testAttribute(f,'width');
    f._set_align('left')
    rt = f._get_align()
    if rt != 'Left':
        error('get/set of align failed')
    f._set_frameBorder('left')
    rt = f._get_frameBorder()
    if rt != 'Left':
        error('get/set of frameBorder failed')
    f._set_scrolling('auto')
    rt = f._get_scrolling()
    if rt != 'Auto':
        error('get/set of scrolling failed')

    print 'get/set works'


if __name__ == '__main__':
    test()
