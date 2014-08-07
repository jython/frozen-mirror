def error(msg):
    raise 'ERROR: ' + msg


def test():
    print 'Testing Syntax'
    from util import testAttribute
    from util import testIntAttribute
    from xml.dom import implementation
    from xml.dom.html.HTMLElement import HTMLElement

    #Test with an HTML Element
    doc = implementation.createHTMLDocument('Title')

    e = doc.createElement('HTML');

    print 'Testing get/set of attributes'

    e._set_id('1');
    if e._get_id() != '1':
        error('get/set of ID failed');

    e._set_title('TEST');
    if e._get_title() != 'TEST':
        error('get/set of Title failed');

    e._set_lang('EN');
    if e._get_lang() != 'EN':
        error('get/set of lang failed');

    e._set_dir('/src/');
    if e._get_dir() != '/src/':
        error('get/set of dir failed');

    e._set_className('class');
    if e._get_className() != 'class':
        error('get/set of className failed');

    print 'get/set of attributes works'

    print 'test cloneNode'

    e2 = e.cloneNode(0);

    print 'cloneNode works'


if __name__ == '__main__':

    test();
