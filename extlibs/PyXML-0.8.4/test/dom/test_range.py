TEST_FILE = '../../demo/dom/addr_book1.xml'

from xml.dom.ext.reader import PyExpat
from xml.dom import Node
from xml.dom import Range

def ReadDoc():
    #Read in a doc
    r = PyExpat.Reader()

    global doc
    global ADDRBOOK
    global ENTRIES
    global PA
    global PA_NAME
    global PA_ADDR
    global PA_WORK
    global PA_FAX
    global PA_PAGER
    global PA_EMAIL
    global EN
    global EN_NAME
    global EN_ADDR
    global EN_WORK
    global EN_FAX
    global EN_PAGER
    global EN_EMAIL
    global VZ

    doc = r.fromUri(TEST_FILE)
    ADDRBOOK = doc.documentElement
    elementType = lambda n, nt=Node.ELEMENT_NODE: n.nodeType == nt
    ENTRIES = filter(elementType, ADDRBOOK.childNodes)
    PA = ENTRIES[0]
    children = filter(elementType, PA.childNodes)
    PA_NAME = children[0]
    PA_ADDR = children[1]
    PA_WORK = children[2]
    PA_FAX = children[3]
    PA_PAGER = children[4]
    PA_EMAIL = children[5]
    EN = ENTRIES[2]
    children = filter(elementType, EN.childNodes)
    EN_NAME = children[0]
    EN_ADDR = children[1]
    EN_WORK = children[2]
    EN_FAX = children[3]
    EN_PAGER = children[4]
    EN_EMAIL = children[5]

    VZ = ENTRIES[3]



def test(tester=None):
    if tester is None:
        import TestSuite
        tester = TestSuite.TestSuite(1,1)

    tester.startGroup('DOM Level II Ranges')

    tester.startTest('Creating test environment')
    ReadDoc()
    tester.testDone()


    tester.startTest("Compare Positions")
    range = doc.createRange()

    #CASE 1
    tester.testResults(Range.Range.POSITION_EQUAL,range._Range__comparePositions(ADDRBOOK,0,ADDRBOOK,0),done=0)
    tester.testResults(Range.Range.POSITION_LESS_THAN,range._Range__comparePositions(ADDRBOOK,0,ADDRBOOK,1),done=0)
    tester.testResults(Range.Range.POSITION_GREATER_THAN,range._Range__comparePositions(ADDRBOOK,1,ADDRBOOK,0),done=0)

    #CASE 2
    tester.testResults(Range.Range.POSITION_LESS_THAN,range._Range__comparePositions(ADDRBOOK,0,EN,1),done=0,msg = 'CASE 2 #1')
    tester.testResults(Range.Range.POSITION_LESS_THAN,range._Range__comparePositions(ADDRBOOK,5,EN,1),done=0,msg = 'CASE 2 #2')
    tester.testResults(Range.Range.POSITION_GREATER_THAN,range._Range__comparePositions(ADDRBOOK,6,EN,1),done=0,msg = 'CASE 2 #3')
    #CASE 3
    tester.testResults(Range.Range.POSITION_GREATER_THAN,range._Range__comparePositions(EN,1,ADDRBOOK,0),done=0,msg = 'CASE 3 #1')
    tester.testResults(Range.Range.POSITION_GREATER_THAN,range._Range__comparePositions(EN,1,ADDRBOOK,5),done=0,msg = 'CASE 3 #2')
    tester.testResults(Range.Range.POSITION_LESS_THAN,range._Range__comparePositions(EN,1,ADDRBOOK,6),done=0,msg = 'CASE 3 #3')

    #CASE 4
    tester.testResults(Range.Range.POSITION_LESS_THAN,range._Range__comparePositions(PA,0,EN_NAME,0),done=0,msg = 'CASE 4 #1')
    tester.testResults(Range.Range.POSITION_GREATER_THAN,range._Range__comparePositions(EN,0,PA_NAME,0),done=0,msg = 'CASE 4 #2')

    #TEst with one as doc
    tester.testResults(Range.Range.POSITION_LESS_THAN,range._Range__comparePositions(doc,0,EN_NAME,0),done=0,msg = 'w/doc')


    tester.testDone()


    tester.startTest("Range.setStart")
    range.setStart(PA,1)

    tester.testResults(PA,range.startContainer,done=0,msg='setStart 1')
    tester.testResults(1,range.startOffset,done=0,msg='setStart 2')
    tester.testResults(PA,range.endContainer,done=0,msg='setStart 3')
    tester.testResults(1,range.endOffset,done=0,msg='setStart 4')
    tester.testResults(PA,range.commonAncestorContainer,done=0,msg='setStart 5')
    tester.testResults(1,range.collapsed,done=0,msg='collapsed')
    tester.testDone()

    tester.startTest("Range.setEnd")

    range.setEnd(PA_NAME,1)
    tester.testResults(PA,range.startContainer,done=0,msg='setEnd 1')
    tester.testResults(1,range.startOffset,done=0,msg='setEnd 2')
    tester.testResults(PA_NAME,range.endContainer,done=0,msg='setEnd 3')
    tester.testResults(1,range.endOffset,done=0,msg='setEnd 4')
    tester.testResults(PA,range.commonAncestorContainer,done=0,msg='setEnd 5')
    tester.testResults(0,range.collapsed,done=0,msg='collapsed')

    range.setEnd(EN_NAME,1)
    tester.testResults(PA,range.startContainer,done=0,msg='setEnd 6')
    tester.testResults(1,range.startOffset,done=0,msg='setEnd 7')
    tester.testResults(EN_NAME,range.endContainer,done=0,msg='setEnd 8')
    tester.testResults(1,range.endOffset,done=0,msg='setEnd 9')
    tester.testResults(ADDRBOOK,range.commonAncestorContainer,done=0,msg='setEnd 10')
    tester.testResults(0,range.collapsed,done=0,msg='collapsed')

    range.setEnd(doc,0)
    tester.testResults(doc,range.startContainer,done=0,msg='setEnd 11')
    tester.testResults(0,range.startOffset,done=0,msg='setEnd 12')
    tester.testResults(doc,range.endContainer,done=0,msg='setEnd 13')
    tester.testResults(0,range.endOffset,done=0,msg='setEnd 14')
    tester.testResults(doc,range.commonAncestorContainer,done=0,msg='setEnd 15')
    tester.testResults(1,range.collapsed,done=0,msg='collapsed')
    tester.testDone()

    tester.startTest("Range.startAfter")

    range.setEnd(EN_NAME,1)
    range.setStartAfter(EN)
    tester.testResults(ADDRBOOK,range.startContainer,done=0,msg='startAfter 1')
    tester.testResults(6,range.startOffset,done=0,msg='startAfter 2')
    tester.testResults(ADDRBOOK,range.commonAncestorContainer,done=0,msg='startAfter 3')
    tester.testDone()

    tester.startTest("Range.startBefore")
    range.setEnd(EN_NAME,1)
    range.setStartBefore(EN)
    tester.testResults(ADDRBOOK,range.startContainer,done=0,msg='startBefore 1')
    tester.testResults(5,range.startOffset,done=0,msg='startBefore 2')
    tester.testResults(ADDRBOOK,range.commonAncestorContainer,done=0,msg='startBefore 3')
    tester.testDone()

    tester.startTest("Range.endAfter")
    range.setStart(ADDRBOOK,0)
    range.setEndAfter(EN_NAME)
    tester.testResults(EN,range.endContainer,done=0,msg='endAfter 1')
    tester.testResults(2,range.endOffset,done=0,msg='endAfter 2')
    tester.testResults(ADDRBOOK,range.commonAncestorContainer,done=0,msg='endAfter 3')
    tester.testDone()

    tester.startTest("Range.endBefore")
    range.setStart(ADDRBOOK,0)
    range.setEndBefore(EN_NAME)
    tester.testResults(EN,range.endContainer,done=0,msg='endBefore 1')
    tester.testResults(1,range.endOffset,done=0,msg='endBefore 2')
    tester.testResults(ADDRBOOK,range.commonAncestorContainer,done=0,msg='endBefore 3')
    tester.testDone()

    tester.startTest("Range.collapse")
    range.setStart(ADDRBOOK,0)
    range.setEndBefore(EN_NAME)
    range.collapse(1)
    tester.testResults(ADDRBOOK,range.startContainer,done=0,msg='collapse 1')
    tester.testResults(0,range.startOffset,done=0,msg='collapse 2')
    tester.testResults(ADDRBOOK,range.endContainer,done=0,msg='collapse 3')
    tester.testResults(0,range.endOffset,done=0,msg='collapse 4')
    range.setStart(ADDRBOOK,0)
    range.setEndBefore(EN_NAME)
    range.collapse(0)
    tester.testResults(EN,range.startContainer,done=0,msg='collapse 5')
    tester.testResults(1,range.startOffset,done=0,msg='collapse 6')
    tester.testResults(EN,range.endContainer,done=0,msg='collapse 7')
    tester.testResults(1,range.endOffset,done=0,msg='collapse 8')
    tester.testDone()

    tester.startTest("Range.selectNode")
    range.selectNode(EN)
    tester.testResults(ADDRBOOK,range.startContainer,done=0,msg='selectNode 1')
    tester.testResults(5,range.startOffset,done=0,msg='selectNode 2')
    tester.testResults(ADDRBOOK,range.endContainer,done=0,msg='selectNode 3')
    tester.testResults(6,range.endOffset,done=0,msg='selectNode 4')
    tester.testDone()

    tester.startTest("Range.selectNodeContents")
    range.selectNodeContents(EN)
    tester.testResults(EN,range.startContainer,done=0,msg='selectNodeContents 1')
    tester.testResults(0,range.startOffset,done=0,msg='selectNodeContents 2')
    tester.testResults(EN,range.endContainer,done=0,msg='selectNodeContents 3')
    tester.testResults(13,range.endOffset,done=0,msg='selectNodeContents 4')
    tester.testDone()

    tester.startTest("Range.compareBoundaryPoints")
    range.selectNodeContents(EN)
    r2 = doc.createRange()
    r2.selectNode(PA)

    tester.testResults(1,range.compareBoundaryPoints(range.START_TO_START,r2),done=0,msg='compareBoundaryPoints 1')
    tester.testResults(1,range.compareBoundaryPoints(range.START_TO_END,r2),done=0,msg='compareBoundaryPoints 2')
    tester.testResults(1,range.compareBoundaryPoints(range.END_TO_START,r2),done=0,msg='compareBoundaryPoints 3')
    tester.testResults(1,range.compareBoundaryPoints(range.END_TO_END,r2),done=0,msg='compareBoundaryPoints 4')
    tester.testDone()


    tester.startTest("Range.deleteContents")
    range.setStart(EN_NAME.firstChild,2)
    range.setEnd(EN_NAME.firstChild,11)

    range.deleteContents()

    tester.testResults('Emsi',EN_NAME.firstChild.data,done=0,msg='deleteContents 1')

    ReadDoc()
    range = doc.createRange()
    range.setStart(EN,2)
    range.setEnd(EN,12)

    range.deleteContents()

    tester.testResults(2,len(EN.childNodes),done=0,msg='deleteContents 2')
    tester.testResults(EN_NAME,EN.childNodes[1],done=0,msg='deleteContents 3')


    #Start is the ancestor
    ReadDoc()
    range = doc.createRange()
    range.setStart(ADDRBOOK,0)
    range.setEnd(EN_PAGER,1)

    range.deleteContents()

    tester.testResults(4,len(ADDRBOOK.childNodes),done=0,msg='deleteContents 4')
    tester.testResults(4,len(EN.childNodes),done=0,msg='deleteContents 5')
    tester.testResults(EN_PAGER,EN.childNodes[0],done=0,msg='deleteContents 6')
    tester.testResults(None,EN.childNodes[0].firstChild,done=0,msg='deleteContents 7')


    #End is the acnestor
    ReadDoc()
    range = doc.createRange()
    range.setStart(PA_NAME,0)
    range.setEnd(ADDRBOOK,4)

    range.deleteContents()

    tester.testResults(6,len(ADDRBOOK.childNodes),done=0,msg='deleteContents 18')
    tester.testResults(2,len(PA.childNodes),done=0,msg='deleteContents 19')
    tester.testResults(PA_NAME,PA.childNodes[1],done=0,msg='deleteContents 20')
    tester.testResults(None,PA.childNodes[1].firstChild,done=0,msg='deleteContents 21')


    #Text to text deep ancestor
    ReadDoc()
    range = doc.createRange()
    range.setStart(PA_NAME.firstChild,2)
    range.setEnd(EN_PAGER.firstChild,4)

    range.deleteContents()


    tester.testResults(2,len(PA.childNodes),done=0,msg='deleteContents 2')
    tester.testResults(PA_NAME,PA.childNodes[1],done=0,msg='deleteContents 3')
    tester.testResults(6,len(ADDRBOOK.childNodes),done=0,msg='deleteContents 4')
    tester.testResults(4,len(EN.childNodes),done=0,msg='deleteContents 5')
    tester.testResults(EN_PAGER,EN.childNodes[0],done=0,msg='deleteContents 6')


    ReadDoc()
    range = doc.createRange()
    range.setStart(PA_NAME,0)
    range.setEnd(EN_PAGER,1)

    range.deleteContents()

    tester.testResults(2,len(PA.childNodes),done=0,msg='deleteContents 7')
    tester.testResults(PA_NAME,PA.childNodes[1],done=0,msg='deleteContents 8')
    tester.testResults(None,PA.childNodes[1].firstChild,done=0,msg='deleteContents 9')
    tester.testResults(6,len(ADDRBOOK.childNodes),done=0,msg='deleteContents 10')
    tester.testResults(4,len(EN.childNodes),done=0,msg='deleteContents 11')
    tester.testResults(EN_PAGER,EN.childNodes[0],done=0,msg='deleteContents 12')
    tester.testResults(None,EN.childNodes[0].firstChild,done=0,msg='deleteContents 13')


    tester.testDone()

    tester.startTest("Range.extractContents")

    #Test two text nodes same
    ReadDoc()
    range = doc.createRange()
    range.setStart(EN_NAME.firstChild,2)
    range.setEnd(EN_NAME.firstChild,11)

    df = range.extractContents()

    tester.testResults('Emsi',EN_NAME.firstChild.data,done=0,msg='extractContents 1')
    tester.testResults(1,len(df.childNodes),done=0,msg='extractContents 2')
    tester.testResults('eka Ndubui',df.childNodes[0].data,done=0,msg='extractContents 3')

    #Two elements, same node
    ReadDoc()
    range = doc.createRange()
    range.setStart(EN,2)
    range.setEnd(EN,12)

    df = range.extractContents()

    tester.testResults(2,len(EN.childNodes),done=0,msg='extractContents 4')
    tester.testResults(EN_NAME,EN.childNodes[1],done=0,msg='extractContents 5')
    tester.testResults(11,len(df.childNodes),done=0,msg='extractContents 6')
    tester.testResults(EN_ADDR,df.childNodes[1],done=0,msg='extractContents 7')
    tester.testResults(EN_EMAIL,df.childNodes[9],done=0,msg='extractContents 8')


    #Start is the ancestor
    ReadDoc()
    range = doc.createRange()
    range.setStart(ADDRBOOK,0)
    range.setEnd(EN_PAGER,1)

    df = range.extractContents()

    tester.testResults(4,len(ADDRBOOK.childNodes),done=0,msg='extractContents 9')
    tester.testResults(4,len(EN.childNodes),done=0,msg='extractContents 10')
    tester.testResults(EN_PAGER,EN.childNodes[0],done=0,msg='extractContents 11')
    tester.testResults(None,EN.childNodes[0].firstChild,done=0,msg='extractContents 12')
    tester.testResults(6,len(df.childNodes),done=0,msg='extractContents 13')

    #End is the acnestor
    ReadDoc()
    range = doc.createRange()
    range.setStart(PA_NAME,0)
    range.setEnd(ADDRBOOK,4)

    df = range.extractContents()


    tester.testResults(6,len(ADDRBOOK.childNodes),done=0,msg='extractContents 14')
    tester.testResults(2,len(PA.childNodes),done=0,msg='extractContents 15')
    tester.testResults(PA_NAME,PA.childNodes[1],done=0,msg='extractContents 16')
    tester.testResults(None,PA.childNodes[1].firstChild,done=0,msg='extractContents 17')
    tester.testResults(4,len(df.childNodes),done=0,msg='extractContents 18')





    #Text to text deep ancestor
    ReadDoc()
    range = doc.createRange()
    range.setStart(PA_NAME.firstChild,2)
    range.setEnd(EN_PAGER.firstChild,4)

    df = range.extractContents()


    tester.testResults(2,len(PA.childNodes),done=0,msg='extractContents 19')
    tester.testResults(PA_NAME,PA.childNodes[1],done=0,msg='extractContents 20')
    tester.testResults(6,len(ADDRBOOK.childNodes),done=0,msg='extractContents 21')
    tester.testResults(4,len(EN.childNodes),done=0,msg='extractContents 22')
    tester.testResults(EN_PAGER,EN.childNodes[0],done=0,msg='extractContents 23')
    tester.testResults(5,len(df.childNodes),done=0,msg='extractContents 24')



    ReadDoc()
    range = doc.createRange()
    range.setStart(PA_NAME,0)
    range.setEnd(EN_PAGER,1)

    df = range.extractContents()

    tester.testResults(2,len(PA.childNodes),done=0,msg='extractContents 25')
    tester.testResults(PA_NAME,PA.childNodes[1],done=0,msg='extractContents 26')
    tester.testResults(None,PA.childNodes[1].firstChild,done=0,msg='extractContents 27')
    tester.testResults(6,len(ADDRBOOK.childNodes),done=0,msg='extractContents 28')
    tester.testResults(4,len(EN.childNodes),done=0,msg='extractContents 29')
    tester.testResults(EN_PAGER,EN.childNodes[0],done=0,msg='extractContents 30')
    tester.testResults(None,EN.childNodes[0].firstChild,done=0,msg='extractContents 31')
    tester.testResults(5,len(df.childNodes),done=0,msg='extractContents 32')


    tester.testDone()


    tester.startTest("Range.cloneContents")

    #Test two text nodes same
    ReadDoc()
    range = doc.createRange()
    range.setStart(EN_NAME.firstChild,2)
    range.setEnd(EN_NAME.firstChild,11)

    df = range.cloneContents()


    tester.testResults('Emeka Ndubuisi',EN_NAME.firstChild.data,done=0,msg='cloneContents 1')
    tester.testResults(1,len(df.childNodes),done=0,msg='cloneContents 2')
    tester.testResults('eka Ndubui',df.childNodes[0].data,done=0,msg='cloneContents 3')



    #Two elements, same node
    ReadDoc()
    range = doc.createRange()
    range.setStart(EN,2)
    range.setEnd(EN,12)

    df = range.cloneContents()


    tester.testResults(13,len(EN.childNodes),done=0,msg='cloneContents 4')
    tester.testResults(EN_NAME,EN.childNodes[1],done=0,msg='cloneContents 5')
    tester.testResults(11,len(df.childNodes),done=0,msg='cloneContents 6')
    tester.testResults('42 Spam Blvd',df.childNodes[1].firstChild.data,done=0,msg='cloneContents 7')
    tester.testResults('endubuisi@spamtron.com',df.childNodes[9].firstChild.data,done=0,msg='cloneContents 8')


    #Start is the ancestor
    ReadDoc()
    range = doc.createRange()
    range.setStart(ADDRBOOK,0)
    range.setEnd(EN_PAGER,1)

    df = range.cloneContents()




    tester.testResults(9,len(ADDRBOOK.childNodes),done=0,msg='cloneContents 9')
    tester.testResults(13,len(EN.childNodes),done=0,msg='cloneContents 10')
    tester.testResults(EN_PAGER,EN.childNodes[9],done=0,msg='cloneContents 11')
    tester.testResults('800-SKY-PAGEx767676',EN_PAGER.firstChild.data,done=0,msg='cloneContents 12')
    tester.testResults(6,len(df.childNodes),done=0,msg='cloneContents 13')


    #End is the acnestor
    ReadDoc()
    range = doc.createRange()
    range.setStart(PA_NAME,0)
    range.setEnd(ADDRBOOK,4)

    df = range.cloneContents()


    tester.testResults(9,len(ADDRBOOK.childNodes),done=0,msg='cloneContents 14')
    tester.testResults(13,len(PA.childNodes),done=0,msg='cloneContents 15')
    tester.testResults(PA_NAME,PA.childNodes[1],done=0,msg='cloneContents 16')
    tester.testResults('Pieter Aaron',PA_NAME.firstChild.data,done=0,msg='cloneContents 17')
    tester.testResults(4,len(df.childNodes),done=0,msg='cloneContents 18')


    #Text to text deep ancestor
    ReadDoc()
    range = doc.createRange()
    range.setStart(PA_NAME.firstChild,2)
    range.setEnd(EN_PAGER.firstChild,4)

    df = range.cloneContents()


    tester.testResults(13,len(PA.childNodes),done=0,msg='cloneContents 19')
    tester.testResults(PA_NAME,PA.childNodes[1],done=0,msg='cloneContents 20')
    tester.testResults(9,len(ADDRBOOK.childNodes),done=0,msg='cloneContents 21')
    tester.testResults(13,len(EN.childNodes),done=0,msg='cloneContents 22')
    tester.testResults(EN_PAGER,EN.childNodes[9],done=0,msg='cloneContents 23')
    tester.testResults(5,len(df.childNodes),done=0,msg='cloneContents 24')


    ReadDoc()
    range = doc.createRange()
    range.setStart(PA_NAME,0)
    range.setEnd(EN_PAGER,1)

    df = range.cloneContents()

    tester.testResults(13,len(PA.childNodes),done=0,msg='cloneContents 25')
    tester.testResults(PA_NAME,PA.childNodes[1],done=0,msg='cloneContents 26')
    tester.testResults(9,len(ADDRBOOK.childNodes),done=0,msg='cloneContents 27')
    tester.testResults(13,len(EN.childNodes),done=0,msg='cloneContents 29')
    tester.testResults(EN_PAGER,EN.childNodes[9],done=0,msg='cloneContents 30')
    tester.testResults(5,len(df.childNodes),done=0,msg='cloneContents 32')


    tester.testDone()

    tester.startTest("Range.insertNode")
    ReadDoc()
    range = doc.createRange()
    range.setStart(PA_NAME.firstChild,1)
    range.setEnd(EN_PAGER,1)

    newNode = doc.createElement('FOO')

    range.insertNode(newNode)

    tester.testResults(3,len(PA_NAME.childNodes),done=0,msg='insertNode 1')
    tester.testResults('P',PA_NAME.firstChild.data,done=0,msg='insertNode 2')
    tester.testResults(newNode,PA_NAME.childNodes[1],done=0,msg='insertNode 3')


    ReadDoc()
    range = doc.createRange()
    range.setStart(PA,1)
    range.setEnd(EN_PAGER,1)

    newNode = doc.createElement('FOO')

    range.insertNode(newNode)

    tester.testResults(14,len(PA.childNodes),done=0,msg='insertNode 3')
    tester.testResults(newNode,PA.childNodes[2],done=0,msg='insertNode 4')

    tester.testDone()


    tester.startTest("Range.surroundContents")
    ReadDoc()
    range = doc.createRange()
    range.setStart(PA,0)
    range.setEnd(PA,9)

    newNode = doc.createElement('FOO')

    range.surroundContents(newNode)


    tester.testResults(4,len(PA.childNodes),done=0,msg='insertNode 1')
    tester.testResults(newNode,PA.childNodes[1],done=0,msg='insertNode 2')
    tester.testDone()


    tester.startTest("Range.cloneRange")
    ReadDoc()
    range = doc.createRange()
    range.setStart(PA,0)
    range.setEnd(PA,9)

    newRange = range.cloneRange()

    tester.testResults(newRange.endOffset,range.endOffset,done=0,msg='cloneRange 1')
    tester.testResults(newRange.endContainer,range.endContainer,done=0,msg='cloneRange 2')
    tester.testResults(newRange.startOffset,range.startOffset,done=0,msg='cloneRange 3')
    tester.testResults(newRange.startContainer,range.startContainer,done=0,msg='cloneRange 4')
    tester.testResults(newRange.collapsed,range.collapsed,done=0,msg='cloneRange 5')
    tester.testResults(newRange.commonAncestorContainer,range.commonAncestorContainer,done=0,msg='cloneRange 6')
    tester.testDone()

    tester.startTest("Range.toString")
    ReadDoc()
    range = doc.createRange()
    range.setStart(PA,0)
    range.setEnd(PA,9)

    range.toString()

    range.setStart(PA_NAME.firstChild,3)
    range.setEnd(EN_EMAIL.firstChild,9)

    range.toString()

    tester.testDone()

    tester.startTest("Range.detach")

    ReadDoc()
    range = doc.createRange()
    range.detach()
    from xml.dom import InvalidStateErr

    try:
        print range.startOffset
    except InvalidStateErr, e:
        tester.testDone
    else:
        tester.testError()

    tester.groupDone()

if __name__ == '__main__':
    test()
