from util import error
from util import testAttribute
from util import testIntAttribute

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLInputElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    f = doc.createElement('Form')

    text = doc.createElement('Input')
    text.setAttribute('TYPE','TEXT')

    radio = doc.createElement('Input')
    radio.setAttribute('TYPE','RADIO')

    image = doc.createElement('Input')
    image.setAttribute('TYPE','IMAGE')

    f.appendChild(text)
    f.appendChild(radio)
    f.appendChild(image)

    print 'testing generic get/set functions'
    testAttribute(text,'defaultValue')
    testAttribute(text,'accept')
    testAttribute(text,'accessKey')
    testAttribute(text,'alt')
    testAttribute(text,'name')
    testAttribute(text,'size')
    testAttribute(image,'src')
    testAttribute(text,'useMap')
    testAttribute(text,'value')

    text._set_align('left')
    rt = text._get_align()
    if rt != 'Left':
        error('get/set of align failed')

    if image._get_type() != 'Image':
        error('get of type failed')

    print 'get/set works'

    print 'testing int Attributes'
    testIntAttribute(radio,'defaultChecked');
    testIntAttribute(radio,'checked');
    testIntAttribute(radio,'disabled');
    testIntAttribute(text,'maxLength');
    testIntAttribute(text,'readOnly');
    testIntAttribute(text,'tabIndex');

    print 'Int get/sets work'

    print "testing cloneNode"
    i2 = radio.cloneNode(0);
    if i2._get_defaultChecked() != radio._get_defaultChecked():
        error('cloneNode failed to copy defaultChecked')
    i3 = text.cloneNode(0)
    if i3._get_defaultValue() != text._get_defaultValue():
        error('cloneNode failed to copy defaultValue')
    print 'cloneNode works'


if __name__ == '__main__':
    test()
