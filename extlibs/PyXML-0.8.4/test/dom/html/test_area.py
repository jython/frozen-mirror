from util import error
from util import testAttribute
from util import testIntAttribute

def test():
    print "testing syntax"
    from xml.dom.html.HTMLAreaElement import HTMLAreaElement

    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')

    p = doc.createElement('Area')

    print "testing get/set"

    testAttribute(p,'accessKey')
    testAttribute(p,'alt')
    testAttribute(p,'coords')
    testAttribute(p,'href')
    testAttribute(p,'target')
    testIntAttribute(p,'noHref')
    testIntAttribute(p,'tabIndex')
    p._set_shape('circle')
    rt = p._get_shape()
    if rt != 'Circle':
        error('get/set shape failed')
    print "get/sets work"

if __name__ == '__main__':

    test();
