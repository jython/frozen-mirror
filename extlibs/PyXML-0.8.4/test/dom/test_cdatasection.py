from TestSuite import EMPTY_NAMESPACE
def test(tester):

    tester.startGroup('CDATASection')

    tester.startTest('Testing syntax')
    try:
        from xml.dom import CDATASection
        from xml.dom.CDATASection import CDATASection
    except:
        tester.tester.error('Error in syntax', 1)
    tester.testDone()


    tester.startTest('Creating test environment')
    from xml.dom import implementation
    dt = implementation.createDocumentType('','','')
    doc = implementation.createDocument(EMPTY_NAMESPACE,'ROOT',dt)

    cds = doc.createCDATASection("This is a CDATA Section")
    cds.data="This is a CDATA Section"
    tester.testDone()


    tester.startTest('Testing cloneNode()')
    #Should always be done deep
    cds1 = cds.cloneNode(1)

    if cds1.data != cds.data:
        tester.error("cloneNode does not copy data")
    tester.testDone()


    return tester.groupDone()


if __name__ == '__main__':
    import sys
    import TestSuite

    tester = TestSuite.TestSuite()
    retVal = test(tester)
    sys.exit(retVal)
