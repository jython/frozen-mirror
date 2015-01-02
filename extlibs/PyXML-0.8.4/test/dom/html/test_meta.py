from util import error
from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLMetaElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    m = doc.createElement('META')

    print 'testing get/set of attributes'

    testAttribute(m,'content')
    testAttribute(m,'httpEquiv')
    testAttribute(m,'scheme')

    print 'get/set works'


if __name__ == '__main__':
    test()
