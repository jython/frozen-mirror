from TestSuite import EMPTY_NAMESPACE
def test(tester):

    tester.startGroup('Comment')

    tester.startTest('Testing syntax')
    try:
        from xml.dom import Comment
        from xml.dom.Comment import Comment
    except:
        tester.error('Error in syntax', 1)
    tester.testDone()


    tester.startTest('Creating test environment')
    from xml.dom import implementation
    dt = implementation.createDocumentType('','','')
    doc = implementation.createDocument(EMPTY_NAMESPACE,'ROOT',dt)
    c = doc.createComment("Comment")
    tester.testDone()

    tester.startTest('Test cloneNode()')
    c1 = c.cloneNode(1)
    if c1.data != c.data:
        tester.error("cloneNode does not copy data")
    tester.testDone()


    return tester.groupDone()


if __name__ == '__main__':
    import sys
    import TestSuite

    tester = TestSuite.TestSuite()
    retVal = test(tester)
    sys.exit(retVal)
