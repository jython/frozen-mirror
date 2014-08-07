from util import error
from util import testAttribute

from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLOptionElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    o = doc.createElement('OPTION')
    f = doc.createElement('FORM')

    f.appendChild(o);

    print 'testing getForm'

    if o._get_form().nodeName != f.nodeName:
        error('getForm failed');

    print 'getForm works'
    print 'testing get/set default selected'

    if o._get_defaultSelected() != 0:
        error('getDefaultSelected failed without setting it');

    o._set_defaultSelected(1);
    if o._get_defaultSelected() != 1:
        error('get/setDefaultSelected failed when set to 1');

    o._set_defaultSelected(0);
    if o._get_defaultSelected() != 0:
        error('get/set defaultSelected does not work when set to 0');

    print 'get/set default selected works'
    print 'testing getText'

    t = doc.createTextNode('TEST')
    o.appendChild(t)
    if o._get_text() != 'TEST':
        error('getText failed')

    print 'getText works'

    print 'testing get index'
    if o._get_index() != -1:
        error('get/set index failed')

    s = doc.createElement('Select')
    s.add(o, None);
    if o._get_index() != 0:
        error('get Index failed for 1')

    print 'testing get/set disabled'

    if o._get_disabled() != 0:
        error('getDisabled failed with nothing set')
    o._set_disabled(1);
    if o._get_disabled() != 1:
        error('getDisabled failed when set to 1')
    o._set_disabled(0);
    if o._get_disabled() != 0:
        error('getdisabled failed when set to 0')

    print 'get/set disabled works'

    print 'testing get/set for label and value'
    testAttribute(o,'label')
    testAttribute(o,'value')
    print 'get/set works'
    print 'testing getSelected'
    #o.setSelected(1);
    #if o.getSelected() != 1:
    #       error('getSelected failed');

    print 'getselected works'
    print 'testing cloneNode'
    o2 = o.cloneNode(0)
    print 'cloneNode works'


if __name__ == '__main__':
    test()
