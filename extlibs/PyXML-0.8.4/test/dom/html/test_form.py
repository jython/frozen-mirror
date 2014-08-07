from util import testAttribute, error

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLFormElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    f = doc.createElement('Form')

    print 'testing get/set'

    testAttribute(f,'name')
    testAttribute(f,'acceptCharset')
    testAttribute(f,'action')
    testAttribute(f,'encType')
    testAttribute(f,'target')
    f._set_method("TEST")
    rt = f._get_method()
    if rt != "Test":
        error('get/set of method failed')

    print 'get/sets work'
    print 'test getElements'
    i = doc.createElement('IsIndex')
    f.appendChild(i)
    hc = f._get_elements()
    if hc.length != 1:
        error('getElements failed')
    if f._get_length() != 1:
        error('getLength failed')
    print 'getElements works'


if __name__ == '__main__':
    test()
