from util import testAttribute, error

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLLegendElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    l = doc.createElement('LEGEND')

    print 'testing get/set'
    testAttribute(l,'accessKey')

    l._set_align('left')
    rt = l._get_align()
    if rt != 'Left':
        error('get/set of align failed')
    print 'get/set works'


if __name__ == '__main__':
    test();
