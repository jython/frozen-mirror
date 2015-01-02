from util import error
from util import testAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLOptGroupElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    o = doc.createElement('OPTGROUP')

    print 'testing get/set disabled'

    if o._get_disabled() != 0:
        error('get disabled failed with nothing set')

    o._set_disabled(1)
    if o._get_disabled() != 1:
        error('get disabled failed when set to 1')

    o._set_disabled(0);
    if o._get_disabled() != 0:
        error('get/set disabled failed when set to 0')

    print 'get/set disabled works'
    print 'testing get/set label'
    testAttribute(o, 'label')
    print 'get/set label works'


if __name__ == '__main__':
    test()
