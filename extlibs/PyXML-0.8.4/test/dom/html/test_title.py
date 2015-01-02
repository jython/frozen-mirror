from util import error

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLTitleElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    t = doc.createElement('TITLE')

    print 'test get/set text'

    t._set_text('TEST');
    if t._get_text() != 'TEST':
        error('get/set text failed');
    print 'text works'


if __name__ == '__main__':
    test();
