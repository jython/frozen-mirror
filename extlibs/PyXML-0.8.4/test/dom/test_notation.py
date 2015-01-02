from TestSuite import EMPTY_NAMESPACE
def test(tester):

    tester.startGroup('Notation')

    tester.startTest('Testing syntax')
    try:
        from xml.dom import Notation
        from xml.dom.Notation import Notation
    except:
        tester.error('Error in syntax', 1)
    tester.testDone()


    tester.startTest('Creating test environment')
    from xml.dom import implementation
    dt = implementation.createDocumentType('','','')
    doc = implementation.createDocument(EMPTY_NAMESPACE,'ROOT',dt)

    nota = doc._4dom_createNotation("-//FOURTHOUGHT//EN", "/tmp/notation", "TestNotation")
    tester.testDone()


    tester.startTest('Testing attributes')
    if nota.publicId != '-//FOURTHOUGHT//EN':
        tester.error('publicId is incorrect')
    if nota.systemId != '/tmp/notation':
        tester.error('systemId is incorrect')
    tester.testDone()


    tester.startTest('Test cloneNode()')
    nota1 = nota.cloneNode(1)
    if nota1.publicId != nota.publicId:
        tester.error("cloneNode fails on publicId")

    if nota1.systemId != nota.systemId:
        tester.error("cloneNode fails on systemId")
    tester.testDone()


    return tester.groupDone()


if __name__ == '__main__':
    import sys
    import TestSuite

    tester = TestSuite.TestSuite()
    retVal = test(tester)
    sys.exit(retVal)
