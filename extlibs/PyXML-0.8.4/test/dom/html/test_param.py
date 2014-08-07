from util import error
from util import testAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLParamElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    p = doc.createElement('PARAM')

    print "testing get/set"

    testAttribute(p,'type')
    testAttribute(p,'value')
    p._set_valueType('object')
    rt = p._get_valueType()
    if rt != 'Object':
        error('get/set valueType failed')
    print "get/sets work"


if __name__ == '__main__':
    test()
