import cStringIO
from xml.dom import DOMException

from xml.dom.ext.reader import HtmlLib
from xml.dom.ext import XHtmlPrint

def GetExceptionName(code):
    import types
    from xml import dom
    for (name,value) in vars(dom).items():
        if (type(value) == types.IntType and value == code):
            return name

source_1 = """\
<!doctype html public "-//W3C//DTD HTML 3.2//EN">
<html>
<head>
<title>XML The future of EDI?</title>
</head>
<body bgcolor="#FFFFFF" text="#000000" link="#0000FF" alink="#FF0000" vlink="#551a8b" marginheight="0" topmargin="0">
<table border="0" width="100%" cellpadding="0" cellspacing="0">
<tr>
<td colspan="2" bgcolor="#FF6600"><font color="#FFFFFF" face="Arial,Helvetica,Sans-serif"><strong>Resources and Related Links</strong></font></td>
<td></td>
</tr>
<tr>
<td>&nbsp;</td>
<td>&#160;</td>
</tr>
</table>
</body>
</html>
"""


expected_1 = """\
<?xml version='1.0' encoding='UTF-8'?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "DTD/xhtml1-strict.dtd"><html xmlns='http://www.w3.org/1999/xhtml'>
<head>
<title>XML The future of EDI?</title>
</head>
<body marginheight='0' vlink='#551a8b' text='#000000' alink='#FF0000' topmargin='0' link='#0000FF' bgcolor='#FFFFFF'>
<table cellspacing='0' border='0' width='100%' cellpadding='0'>
<tr>
<td bgcolor='#FF6600' colspan='2'><font face='Arial,Helvetica,Sans-serif' color='#FFFFFF'><strong>Resources and Related Links</strong></font></td>
<td/>
</tr>
<tr>
<td> </td>
<td> </td>
</tr>
</table>
</body>
</html>
"""


def Test(tester):

    tester.startGroup("Uche Ogbuji's problems with &#160; and &nbsp;")

    tester.startTest('Tidy HTML with nbsps and 160s')
    reader = HtmlLib.Reader()
    doc = reader.fromString(source_1, charset="iso-8859-1")

    stream = cStringIO.StringIO()
    XHtmlPrint(doc, stream=stream)

    result = stream.getvalue()
    if result != expected_1:
        tester.error('Expected\n"""%s"""\ngot\n"""%s"""'%(repr(expected_1), repr(result)))
    tester.testDone()

    return tester.groupDone()


if __name__ == '__main__':
    import sys
    import TestSuite

    tester = TestSuite.TestSuite()
    retVal = Test(tester)
    sys.exit(retVal)
