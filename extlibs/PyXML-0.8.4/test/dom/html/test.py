fileList =      ['Collection',
             'Element',
             'HTML',
             'HEAD',
             'LINK',
             'TITLE',
             'META',
             'BASE',
             'ISINDEX',
             'STYLE',
             'BODY',
             'FORM',
             'SELECT',
             'OPTGROUP',
             'OPTION',
             'INPUT',
             'TEXTAREA',
             'BUTTON',
             'LABEL',
             'FIELDSET',
             'LEGEND',
             'UL',
             'OL',
             'DL',
             'DIR',
             'MENU',
             'LI',
             'BLOCKQUOTE',
             'DIV',
             'P',
             'H',
             'Q',
             'PRE',
             'BR',
             'BASEFONT',
             'FONT',
             'HR',
             'MOD',
             'A',
             'IMG',
             'OBJECT',
             'PARAM',
             'APPLET',
             'MAP',
             'AREA',
             'SCRIPT',
             'CAPTION',
             'COL',
             'TD',
             'TR',
             'SECTION',
             'TABLE',
             'FRAMESET',
             'FRAME',
             'IFRAME',
             'DOCUMENT',
             'HTML_DOM_IMPLEMENTATION',
             ]

import string


def test(files):
    print 'Testing HTML Level 1'
    for file in files:
        print '**********Testing HTML %s**********' % file
        exec 'import test_%s;_mod = test_%s' % (string.lower(file),string.lower(file));
        _mod.test();


if __name__ == '__main__':
    import sys
    if len(sys.argv) <2:
        test(fileList)
    else:
        test(sys.argv[1:]);
