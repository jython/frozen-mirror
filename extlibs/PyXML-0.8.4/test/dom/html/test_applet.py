from util import error
from util import testAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html.HTMLAppletElement import HTMLAppletElement

    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')

    p = doc.createElement('Applet')

    print "testing get/set"
    testAttribute(p,'alt')
    testAttribute(p,'archive')
    testAttribute(p,'code')
    testAttribute(p,'codeBase')
    testAttribute(p,'height')
    testAttribute(p,'hspace')
    testAttribute(p,'object')
    testAttribute(p,'vspace')
    testAttribute(p,'width')
    p._set_align('left')
    rt = p._get_align()
    if rt != 'Left':
        error('get/set align failed')
    print "get/sets work"

if __name__ == '__main__':
    test()
