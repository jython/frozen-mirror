from TestSuite import EMPTY_NAMESPACE
from xml.dom import INDEX_SIZE_ERR
from xml.dom import DOMException
from xml.dom import implementation

def get_exception_name(code):
    import types
    from xml import dom
    for (name,value) in vars(dom).items():
        if (type(value) == types.IntType
        and value == code):
            return name

def test(tester):
    tester.startGroup('CharacterData')

    tester.startTest('Checking syntax')
    try:
        from xml.dom import CharacterData
        from xml.dom.CharacterData import CharacterData
    except:
        tester.error('Error in syntax', 1)
    tester.testDone()


    tester.startTest('Creating test environment')
    from xml.dom import implementation
    dt = implementation.createDocumentType('','','')
    doc = implementation.createDocument(EMPTY_NAMESPACE,'ROOT',dt)

    #shouldn't try to instantiate a CharacterData node, so test it through Text
    t1 = doc.createTextNode("")
    t2 = doc.createTextNode('SUBSTRING')
    t3 = doc.createTextNode('APPEND')
    t4 = doc.createTextNode('INSERT')
    t5 = doc.createTextNode('DELETE')
    t6 = doc.createTextNode('TEST')
    tester.testDone()


    tester.startTest('Testing attributes')
    t1.data = 'TEST';
    if t1.data != 'TEST':
        tester.error('Get/set data doesn\'t match')

    if t1.length != 4:
        tester.error('length returned wrong size')
    tester.testDone()


    tester.startTest('Testing substringData()')
    if t2.substringData(1,2) != 'UB':
        tester.error('substringData returns wrong section')
    if t2.substringData(5,100) != 'RING':
        tester.error('substringData fails on oversized \'count\'')
    try:
        t2.substringData(100,2)
    except DOMException, x:
        if x.code != INDEX_SIZE_ERR:
            name = get_exception_name(x.code)
            tester.error("Wrong exception '%s', expected INDEX_SIZE_ERR" % name)
    else:
        tester.error('substringData doesn\'t catch an invalid index')
    tester.testDone()


    tester.startTest('Testing appendData()')
    t3.appendData(' TEST')
    if t3.data != 'APPEND TEST':
        tester.error('appendData does not append')
    tester.testDone()


    tester.startTest('Testing insertData()')
    t4.insertData(2,'here')
    if t4.data != 'INhereSERT':
        tester.error('insertData did not properly insert');
    try:
        t4.insertData(100,'TEST');
    except DOMException, x:
        if x.code != INDEX_SIZE_ERR:
            name = get_exception_name(x.code)
            tester.error("Wrong exception '%s', expected INDEX_SIZE_ERR" % name)
    else:
        tester.error('insertData doesn\'t catch an invalid index')
    tester.testDone()


    tester.startTest('Testing deleteData()')
    # DELETE
    t5.deleteData(2,2)
    if t5.data != 'DETE':
        tester.error('deleteData did not properly get rid of the data')

    t5.deleteData(2,10)
    if t5.data != 'DE':
        tester.error('deleteData fails on oversized \'count\'')

    try:
        t5.deleteData(100,3);
    except DOMException, x:
        if x.code != INDEX_SIZE_ERR:
            name = get_exception_name(x.code)
            tester.error("Wrong exception '%s', expected INDEX_SIZE_ERR" % name)
    else:
        tester.error('deleteData doesn\'t catch an invalid index')
    tester.testDone()


    tester.startTest('Testing replaceData()')
    # REPLACE
    t6.replaceData(0,1,'CH')
    if t6.data != 'CHEST':
        tester.error('replaceData did not properly replace')
    t6.replaceData(3,7,'ESE')
    if t6.data != 'CHEESE':
        tester.error('replaceData did not properly replace')
    try:
        t6.replaceData(100,3,'Not Gonna Happen');
    except DOMException, x:
        if x.code != INDEX_SIZE_ERR:
            name = get_exception_name(x.code)
            tester.error("Wrong exception '%s', expected INDEX_SIZE_ERR" % name)
    else:
        tester.error('replaceData doesn\'t catch an invalid index')
    tester.testDone()


    return tester.groupDone()


if __name__ == '__main__':
    import sys
    import TestSuite

    tester = TestSuite.TestSuite()
    retVal = test(tester)
    sys.exit(retVal)
