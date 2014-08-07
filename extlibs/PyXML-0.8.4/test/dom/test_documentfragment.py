from TestSuite import EMPTY_NAMESPACE
def test(tester):
    tester.startGroup('DocumentFragment')

    tester.startTest('Testing syntax')
    try:
        from xml.dom import DocumentFragment
        from xml.dom.DocumentFragment import DocumentFragment
    except:
        tester.error('Error in syntax', 1)
    tester.testDone()


    tester.startTest('Creating test environment')
    from xml.dom import implementation
    dt = implementation.createDocumentType('','','')
    doc = implementation.createDocument(EMPTY_NAMESPACE,'ROOT',dt)
    df = doc.createDocumentFragment()
    tester.testDone()


    tester.startTest('Testing cloneNode()')
    df1 = df.cloneNode(1)
    tester.testDone()


    return tester.groupDone()


if __name__ == '__main__':
    import sys
    import TestSuite

    tester = TestSuite.TestSuite()
    retVal = test(tester)
    sys.exit(retVal)
