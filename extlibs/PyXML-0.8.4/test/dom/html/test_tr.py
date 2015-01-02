from util import testAttribute
from util import error

def test():
    print 'testing source code syntax'
    from xml.dom.html import HTMLTableRowElement
    from xml.dom import implementation
    doc = implementation.createHTMLDocument('Title')
    r = doc.createElement('TR')

    #Row index and section row index tested in section

    print 'testing get/set'
    testAttribute(r,'bgColor');
    testAttribute(r,'ch');
    testAttribute(r,'chOff');
    r._set_align('left')
    rt = r._get_align()
    if rt != 'Left':
        error('get/set align failed')
    r._set_vAlign('top')
    rt = r._get_vAlign()
    if rt != 'Top':
        error('get/set align failed')
    print 'get/set works'

    print 'testing insertCell,deleteCell, getCells, and TD.cellIndex'

    try:
        c1 = r.insertCell(-1)
        error('insertCell(-1) does not raise exception')
    except:
        pass

    c1 = r.insertCell(0)
    if c1 == None:
        error('insertCell(0) failed');

    try:
        c2 = r.insertCell(10)
        error('insertCell(10) does not raise exception')
    except:
        pass

    cells = r._get_cells()
    if cells._get_length() != 1:
        error('getCells failed');

    if cells.item(0).nodeName != c1.nodeName:
        error('getCells failed');

    try:
        r.deleteCell(-1);
        error('deleteCell(-1) does not raise exception');
    except:
        pass

    r.deleteCell(0);
    if c1._get_cellIndex() != -1:
        error('deleted cell still in tree');

    if r._get_cells().length != 0:
        error('deleteCell failed');

    print 'insertCell, deleteCell, getCells, and TD.getCellIndex works'


if __name__ == '__main__':
    test();
