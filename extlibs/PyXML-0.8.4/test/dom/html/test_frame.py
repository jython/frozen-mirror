from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLFrameElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    f = doc.createElement('Frame')

    print 'testing get/set'
    testAttribute(f,'longDesc')
    testAttribute(f,'marginHeight')
    testAttribute(f,'marginWidth')
    testIntAttribute(f,'noResize')
    testAttribute(f,'src')
    f._set_frameBorder('left')
    rt = f._get_frameBorder()
    if rt != 'Left':
        error('get/set frameBorder failed')
    f._set_scrolling('auto')
    rt = f._get_scrolling()
    if rt != 'Auto':
        error('get/set scrolling failed')
    print 'get/set works'

if __name__ == '__main__':
    test()
