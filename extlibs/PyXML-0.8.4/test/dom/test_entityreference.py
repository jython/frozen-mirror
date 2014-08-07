from TestSuite import EMPTY_NAMESPACE
def test(tester):

    tester.startGroup('EntityReference')

    tester.startTest('Testing syntax')
    try:
        from xml.dom import EntityReference
        from xml.dom.EntityReference import EntityReference
    except:
        tester.error('Error in syntax',1)
    tester.testDone()


    tester.startTest('Creating test environment')
    from xml.dom import implementation
    dt = implementation.createDocumentType('','','')
    doc = implementation.createDocument(EMPTY_NAMESPACE,'ROOT',dt)

    entr = doc.createEntityReference("TestEntity")
    tester.testDone()

    tester.startTest('Test cloneNode()')
    entr1 = entr.cloneNode(1)
    if entr1.nodeName != entr.nodeName:
        tester.error("cloneNode failed")
    tester.testDone()


    return tester.groupDone()


if __name__ == '__main__':
    import sys
    import TestSuite

    tester = TestSuite.TestSuite()
    retVal = test(tester)
    sys.exit(retVal)
