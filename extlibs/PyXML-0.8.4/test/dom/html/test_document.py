from util import error
from util import testAttribute

CLONE_TEST_ENABLED = 0

def test():
    print 'Testing Syntax'
    from xml.dom.html.HTMLDocument import HTMLDocument
    from xml.dom import implementation

    d = implementation.createHTMLDocument('')
    print 'testing title'

    if d._get_title() != '':
        error('getTitle failed with no title');

    #This will test ADC
    d._set_title('TEST');
    if d._get_title() != 'TEST':
        error('get/set title failed with body')

    #Print test replace of a child

    d._set_title('TEST2');

    if d._get_title() != 'TEST2':
        error('replace a title failed')

    print 'title works'
    #d.removeChild(h);

    print 'testing documentElement'
    if d.documentElement == None:
        error('documentElement ADC failed');
    print 'documentElement works'

    print 'testing body'

    if d._get_body() == None:
        error('body ADC failed');

    b = d.createElement('BODY');
    d._set_body(b)
    if d._get_body().nodeName != b.nodeName:
        error('body failed on replace');

    print 'get/set Body works'

    print 'testing getImages'

    i = d.createElement('Img');

    b.appendChild(i);

    hc = d._get_images()
    if hc.length != 1:
        error('getImages failed');

    print 'getImages works'

    print 'getApplets'

    a = d.createElement('Applet');
    o = d.createElement('Object');
    o._set_code('TEST');

    hc = d._get_applets()
    if hc.length != 0:
        error('getApplets failed with none');

    b.appendChild(a);

    hc = d._get_applets();

    if hc.length != 1:
        error('getApplets failed for applets');

    b.appendChild(o)

    hc = d._get_applets()

    if hc.length != 2:
        error('getApplets failed for object');

    print 'getApplets works'

    print 'testing getLinks'

    a1 = d.createElement('Area');
    a1._set_href('TEST')
    a2 = d.createElement('A');
    a2._set_href('TEST')

    if d._get_links().length != 0:
        error('getLinks failed with no Links');

    b.appendChild(a1);

    if d._get_links().length != 1:
        error('getLinks failed with Area');

    b.appendChild(a2);
    if d._get_links().length != 2:
        error('getLinks failed with Anchor');

    print 'getLinks works'

    print 'testing getForms';

    if d._get_forms().length != 0:
        error('getForms failed with no Forms');

    f = d.createElement('FORM');

    b.appendChild(f);
    if d._get_forms().length != 1:
        error('getForms failed with a form');

    print 'getForms works'

    print 'testing getAnchors'

    if d._get_anchors().length != 0:
        error('get Anchors failed with none in there');

    a2._set_name('TEST');

    if d._get_anchors().length != 1:
        error('getAnchors failed with an Anchor');

    print 'getAnchors works'

    testAttribute(d,'cookie');


    if CLONE_TEST_ENABLED:
        print 'test cloneNode (deep)'
        d2 = d.cloneNode(1)

        if d2._get_referrer() != d._get_referrer():
            error('cloneNode did not set referrer');
        if d2._get_domain() != d._get_domain():
            error('cloneNode did not set Domain');
        if d2._get_URL() != d._get_URL():
            error('cloneNode did not set URL');
        if d2._get_cookie() != d._get_cookie():
            error('cloneNode did not set cookie');
    else:
        print "NOTE: DOCUMENT CLONE TEST SKIPPED"

    print 'cloneNode works'


if __name__ == '__main__':

    test();
