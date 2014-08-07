from util import error
from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLMapElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    m = doc.createElement('MAP')
    a = doc.createElement('AREA')

    print "testing get/set"
    m.appendChild(a);
    print "get Areas"
    as = m._get_areas()

    if as[0].nodeName != a.nodeName:
        error('getAreas failed')


if __name__ == '__main__':
    test()
