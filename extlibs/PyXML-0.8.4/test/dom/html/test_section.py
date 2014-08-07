from util import testAttribute
from util import error

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLTableSectionElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    s = doc.createElement('TFOOT')

    #Row index and section row index tested in section
    print 'testing get/set'
    testAttribute(s,'ch')
    testAttribute(s,'chOff')

    s._set_align('left')
    rt = s._get_align()
    if rt != 'Left':
        error('get/set align failed')
    s._set_vAlign('Top')
    rt = s._get_vAlign()
    if rt != 'Top':
        error('get/set align failed')

    print 'get/set works'

    print 'testing insertRow,deleteRow, getRows, and TR.getRowSelectionIndex'

    try:
        r1 = s.insertRow(-1)
        error('insertRow(-1) does not raise exception');
    except:
        pass

    r1 = s.insertRow(0)
    if r1 == None:
        error('insertRow(0) failed');

    r2 = s.insertRow(1)
    if r2 == None:
        error('insertRow(1) failed');

    if r2._get_sectionRowIndex() != 1:
        error('getSectionRowIndex Failed');

    rows = s._get_rows()
    if rows._get_length() != 2:
        error('getRows failed')

    if rows.item(0).nodeName != r1.nodeName:
        error('getRows failed')

    if rows.item(1).nodeName != r2.nodeName:
        error('getRows failed')

    try:
        s.deleteRow(-1)
        error('deleteRow(-1) does not raise exception')
    except:
        pass

    s.deleteRow(1)
    if r2._get_rowIndex() != -1:
        error('deleted row still in tree')

    if s._get_rows()._get_length() != 1:
        error('deleteRow failed');

    s.deleteRow(0)
    if s._get_rows()._get_length() != 0:
        error('deleteRow(0) failed')

    print 'insertRow, deleteRow, getRows, and TR.getSelectionRowIndex works'


if __name__ == '__main__':
    test()
