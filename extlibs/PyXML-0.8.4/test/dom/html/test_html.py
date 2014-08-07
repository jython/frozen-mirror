def error(msg):
    raise 'ERROR: ' + msg

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLHtmlElement
    from xml.dom import implementation
    from util import testAttribute
    from util import testIntAttribute

    doc = implementation.createHTMLDocument('Title')
    h = doc.createElement('html')

    print 'testing get/set version'

    h._set_version('VERSION')
    if h._get_version() != 'VERSION':
        error('get/set of version failed')

    print 'get/set version works'


if __name__ == '__main__':

    test();
