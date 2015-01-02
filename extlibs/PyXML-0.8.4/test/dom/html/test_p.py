from util import testAttribute, error

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLParagraphElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    p = doc.createElement('P')

    print 'testing get/set'
    p._set_align('left')
    rt = p._get_align()
    if rt != 'Left':
        error('get/set align failed')
    print 'get/set works'


if __name__ == '__main__':
    test()
