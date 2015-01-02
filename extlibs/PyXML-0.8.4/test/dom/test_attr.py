from TestSuite import EMPTY_NAMESPACE
def test(tester):

    tester.startGroup('Attr')

    tester.startTest('Checking syntax')
    try:
        from xml.dom import Attr
        from xml.dom.Attr import Attr
    except:
        tester.error('Error in syntax', 1)
    tester.testDone()


    tester.startTest('Creating test environment')
    try:
        from xml.dom import implementation
        dt = implementation.createDocumentType('','','')
        doc = implementation.createDocument(EMPTY_NAMESPACE,'ROOT',dt)
    except:
        tester.error('Error creating document')

    a = doc.createAttribute('TestNode');
    e = doc.createElement('TestElement')
    tester.testDone()


    tester.startTest('Testing attributes')
    if a.name != 'TestNode':
        tester.error("name failed")
    if a.specified != 0:
        tester.error("specified failed")
    a.value = 'Test Value'
    if a.value != 'Test Value':
        tester.error("Error getting/seeting value")
    if a.specified != 1:
        tester.error("Assigning to value does not set specified")
    tester.testDone()


    tester.startTest('Testing cloneNode()')
    #Should always be done deep
    a1 = a.cloneNode(1)

    if a1.value != a.value:
        tester.error("cloneNode fails on value")

    if a1.name != a.name:
        tester.error("cloneNode fails on name")

    if a1.specified != a.specified:
        tester.error("cloneNode fails on specified")
    tester.testDone()


    return tester.groupDone()


if __name__ == '__main__':
    import sys

    import TestSuite
    tester = TestSuite.TestSuite()
    retVal = test(tester)
    sys.exit(retVal)
