from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLButtonElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    b = doc.createElement('Button');

    print 'testing get/set attributes'

    testAttribute(b,'accessKey');
    testIntAttribute(b,'disabled');
    testAttribute(b,'name');
    testIntAttribute(b,'tabIndex');
    testAttribute(b,'value');
    print 'get/sets works'

if __name__ == '__main__':

    test();
