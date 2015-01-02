from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLFrameSetElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    f = doc.createElement('FrameSet')

    print 'testing get/set'
    testAttribute(f,'cols')
    testAttribute(f,'rows')
    print 'get/set works'


if __name__ == '__main__':
    test()
