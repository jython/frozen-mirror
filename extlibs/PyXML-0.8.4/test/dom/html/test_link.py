def error(msg):
    raise 'ERROR: ' + msg

def test():
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')

    print 'Testing source code syntax'
    from xml.dom.html import HTMLLinkElement

    l = doc.createElement('LINK')

    print 'testing get/set of attributes'

    if l._get_disabled() != 0:
        error('get disabled failed for false');

    l._set_disabled(0)

    if l._get_disabled() != 0:
        error('get disabled failed for false');

    l._set_disabled(1);

    if l._get_disabled() != 1:
        error('get/set disabled failed for true');

    l._set_charset('TEST');
    if l._get_charset() != 'TEST':
        error('get/set failed for CharSet');

    l._set_href('TEST');
    if l._get_href() != 'TEST':
        error('get/set failed for href');

    l._set_hreflang('EN');
    if l._get_hreflang() != 'EN':
        error('get/set failed for hrefLang');

    l._set_media('TEST');
    if l._get_media() != 'TEST':
        error('get/set failed for MEDIA');

    l._set_rel('TEST');
    if l._get_rel() != 'TEST':
        error('get/set failed for REL');

    l._set_rev('TEST');
    if l._get_rev() != 'TEST':
        error('get/set failed for Rev');

    l._set_target('TEST');
    if l._get_target() != 'TEST':
        error('get/set failed for TARGET');

    l._set_type('TEST');
    if l._get_type() != 'TEST':
        error('get/set failed for TYPE')

    print 'get/set works'


if __name__ == '__main__':
    test()
