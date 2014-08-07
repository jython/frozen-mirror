def error(msg):
    raise 'ERROR: ' + msg


def test():
    from xml.dom import implementation

    print 'testing source code syntax'
    from xml.dom.html.HTMLCollection import HTMLCollection

    print '### implementation: ' + str(implementation)
    doc = implementation.createHTMLDocument('Title')
    hc = doc._get_images()

    if hc.length != 0:
        error('Initial Length wrong');

    e = doc.createElement('IMG');
    doc.documentElement.appendChild(e);
    hc = doc._get_images()
    print 'test item'

    if hc[0].nodeName != e.nodeName:
        error('item returns the worng value');

    if hc.item(1) != None:
        error('item returns a value when it should be none')

    print 'item works'

    e.setAttribute('NAME','TEST')
    e.setAttribute('ID','1')
    print 'test namedItem'

    if hc.namedItem('TEST').nodeName != e.nodeName:
        error('namedItem did not find a named item')

    if hc.namedItem('1').nodeName != e.nodeName:
        error('namedItem did not find an IDed item')

    if hc.namedItem('TEST1') != None:
        error('namedItem found an item when one did not exist')

    print 'namedItem works';

if __name__ == '__main__':
    test()
