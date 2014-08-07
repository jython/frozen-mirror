from util import error
from util import testAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLSelectElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    s = doc.createElement('SELECT')
    o = doc.createElement('OPTION')
    o1 = doc.createElement('OPTION')

    print 'getType works'

    print 'testing get/set SelectedIndex'

    if s._get_selectedIndex() != -1:
        error('With none selected getSelectedIndex failed');

    s.add(o,None)
    s.add(o1,o)

    s._set_selectedIndex(1)
    if s._get_selectedIndex() != 1:
        error('get/setSelected index fails when one is set');

    print 'get/set selected index works'

    print 'testing getLength'
    if s._get_length() != 2:
        error('getLength fails');
    print 'getLength works'

    print 'testing getOptions'
    os = s._get_options();

    if os.item(0).nodeName != o1.nodeName:
        error('getOptions returns the wrong stuff')

    if os.item(1).nodeName != o.nodeName:
        error('getOptions does not return the correct stuff');

    print 'getOptions works'

    print 'testing get/set disabled'

    if s._get_disabled() != 0:
        error('getDisabled failed when not set');

    s._set_disabled(1)
    if s._get_disabled() != 1:
        error('get/set disabled failed when set');

    s._set_disabled(0)
    if s._get_disabled() != 0:
        error('get/set disabled failed when not set');

    print 'get/set disabled works'

    print 'testing get type'

    if s._get_type() != 'select-one':
        error('getType failed');

    print 'testing get/set multiple'

    if s._get_multiple() != 0:
        error('getMultiple fails with nothing set');

    s._set_multiple(1)
    if s._get_multiple() != 1:
        error('get/set multiple fails when set to 1');

    s._set_multiple(0);
    if s._get_multiple() != 0:
        error('get/set multiple fails when set to 0');

    print 'get/set multiple works'

    print 'test get/set name'
    testAttribute(s,'name');
    print 'get/setName works'

    print 'testing get/set size'
    s._set_size(3)
    if s._get_size() != 3:
        error('get/setSize does not work');

    print 'get/setSize works'
    print 'testing get/setTabIndex'
    s._set_tabIndex(3)
    if s._get_tabIndex() != 3:
        error('get/setTabIndex failed');

    print 'get/setTabIndex works'

    print 'testing add'
    #This was already called
    if s.firstChild.nodeName != o1.nodeName:
        error('add does not work with 2 args');

    if s.lastChild.nodeName != o.nodeName:
        error('add does not work with 1 arg');

    print 'add works'
    print 'testing remove'
    s.remove(0);
    if s.firstChild.nodeName != o.nodeName:
        error('remove failed');
    if s.lastChild.nodeName != o.nodeName:
        error('remove failed');

    if s.firstChild._get_index() != 0:
        print s.firstChild.getIndex()
        error('reindex did not work on remove');

    print 'remove works'

    print 'testing clone node'
    s1 = s.cloneNode(1);

    if s._get_selectedIndex() != s1._get_selectedIndex():
        error('cloneNode did not copy Selected')
    print 'cloneNode Works'


if __name__ == '__main__':
    test()
