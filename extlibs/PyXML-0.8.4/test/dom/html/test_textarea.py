from util import error
from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLTextAreaElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    t = doc.createElement('TEXTAREA')

    print 'testing get/set of attributes'
    testAttribute(t,'defaultValue');
    testAttribute(t,'accessKey');
    testIntAttribute(t,'cols');
    testIntAttribute(t,'disabled');
    testAttribute(t,'name');
    testIntAttribute(t,'readonly');
    testIntAttribute(t,'rows');
    testIntAttribute(t,'tabIndex');
    print 'get/set work'

    print 'testing clone node'
    t2 = t.cloneNode(1)
    if t2._get_defaultValue() != t._get_defaultValue():
        error('cloneNode did not set the default value');
    print 'cloneNode works'


if __name__ == '__main__':
    test()
