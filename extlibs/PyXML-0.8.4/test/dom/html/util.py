def error(msg):
    raise Exception('ERROR: ' + msg)

def testAttribute(elem, attr):
    setattr(elem, attr, 'TEST')
    if getattr(elem, attr) != 'TEST':
        error('get/set of %s failed' % attr)

def testIntAttribute(elem, attr):
    setattr(elem, attr, 1)
    if getattr(elem, attr) != 1:
        error('get/set of %s failed' % attr)
    setattr(elem, attr, 0)
    if getattr(elem, attr) != 0:
        error('get/set of %s failed' % attr)
