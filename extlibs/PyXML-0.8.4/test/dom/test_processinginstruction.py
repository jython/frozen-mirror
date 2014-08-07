from TestSuite import EMPTY_NAMESPACE
def test(tester):

    tester.startGroup('ProcessingInstruction')

    tester.startTest('Testing syntax')
    try:
        from xml.dom import ProcessingInstruction
        from xml.dom.ProcessingInstruction import ProcessingInstruction
    except:
        tester.error('Error in syntax', 1)
    tester.testDone()


    tester.startTest('Creating test environment')
    from xml.dom import implementation
    dt = implementation.createDocumentType('','','')
    doc = implementation.createDocument(EMPTY_NAMESPACE,'ROOT',dt)
    pi = doc.createProcessingInstruction("xml", 'version = "1.0"')
    tester.testDone()

    tester.startTest('Testing attributes')
    if pi.target != 'xml':
        tester.error('Problems with target')
    if pi.data != 'version = "1.0"':
        tester.error('Problems with data')
    tester.testDone()

    tester.startTest('Test cloneNode()')
    pi1 = pi.cloneNode(1)
    if pi1.target != pi.target:
        tester.error("cloneNode fails on target")
    if pi1.data != pi.data:
        tester.error("cloneNode fails on data")
    tester.testDone()


    return tester.groupDone()


if __name__ == '__main__':
    import sys
    import TestSuite

    tester = TestSuite.TestSuite()
    retVal = test(tester)
    sys.exit(retVal)
