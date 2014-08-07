from util import testAttribute, error
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLUListElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    u = doc.createElement('UL')

    print 'testing get/set'
    testIntAttribute(u,'compact')

    u._set_type('ordered')
    rt = u._get_type()
    if rt != 'Ordered':
        error('get/set of type failed')
    print 'get/set works'


if __name__ == '__main__':
    test()
