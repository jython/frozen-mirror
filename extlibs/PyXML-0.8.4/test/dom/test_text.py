from TestSuite import EMPTY_NAMESPACE
from xml.dom import DOMException
from xml.dom import INDEX_SIZE_ERR

def get_exception_name(code):
    import types
    from xml import dom
    for (name,value) in vars(dom).items():
        if (type(value) == types.IntType
        and value == code):
            return name

def test(tester):

    tester.startGroup('Text')

    tester.startTest('Testing syntax')
    try:
        from xml.dom import Text
        from xml.dom.Text import Text
    except:
        tester.error('Error in syntax', 1)
    tester.testDone()


    tester.startTest('Creating test environment')
    from xml.dom import implementation
    dt = implementation.createDocumentType('','','')
    doc = implementation.createDocument(EMPTY_NAMESPACE,'ROOT',dt)

    t = doc.createTextNode("ONETWO")
    tester.testDone()


    tester.startTest('Testing splitText()')
    t2 = t.splitText(3)
    if t.data != 'ONE':
        tester.error('splitText did not properly split first half')
    if t2.data != 'TWO':
        tester.error('splitText did not properly split second half')
    try:
        t.splitText(100)
    except DOMException, x:
        if x.code != INDEX_SIZE_ERR:
            name = get_exception_name(x.code)
            tester.error("Wrong exception '%s', expected INDEX_SIZE_ERR" % name)
    else:
        tester.error('splitText doesn\'t catch an invalid index')
    tester.testDone()


    tester.startTest('Testing cloneNode()')
    t3 = t.cloneNode(0)
    if t3.data != t.data:
        error("cloneNode does not copy data")
    tester.testDone()

    return tester.groupDone()


if __name__ == '__main__':
    import sys
    import TestSuite

    tester = TestSuite.TestSuite()
    retVal = test(tester)
    sys.exit(retVal)
