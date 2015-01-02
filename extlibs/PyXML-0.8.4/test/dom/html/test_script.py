from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLScriptElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    s = doc.createElement('SCRIPT')

    print "testing get/set"

    testAttribute(s,'text')
    testAttribute(s,'charset')
    testAttribute(s,'src')
    testAttribute(s,'type')
    testIntAttribute(s,'defer')

    print "get/sets work"


if __name__ == '__main__':
    test();
