from util import error
from util import testAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLStyleElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    s = doc.createElement('STYLE')

    print 'testing get/set of attributes'

    testAttribute(s,'media')
    testAttribute(s,'type')

    if s._get_disabled() != 0:
        error('getDisabled failed on false');

    s._set_disabled(1);
    if s._get_disabled() != 1:
        error('getDisabled failed on true');

    s._set_disabled(0);
    if s._get_disabled() != 0:
        error('getDisabled failed on false');

    print 'get/set works'


if __name__ == '__main__':
    test()
