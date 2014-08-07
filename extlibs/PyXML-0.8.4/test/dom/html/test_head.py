def error(msg):
    raise 'ERROR: ' + msg

from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLHeadElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    h = doc.createElement('Head')

    print 'testing get/set profile'
    h._set_profile('PROFILE')
    if h._get_profile() != 'PROFILE':
        error('get/set profile failed')
    print 'get/set profile works'


if __name__ == '__main__':
    test()
