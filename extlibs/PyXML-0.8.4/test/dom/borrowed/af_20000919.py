import cStringIO
from xml.dom import DOMException
from xml.dom import NAMESPACE_ERR
from xml.dom.ext import Print, PrettyPrint
from xml.dom.ext.reader import Sax2

def GetExceptionName(code):
    import types
    from xml import dom
    for (name,value) in vars(dom).items():
        if (type(value) == types.IntType and value == code):
            return name

source_1 = """<?xml version = "1.0"?>
<!DOCTYPE ADDRBOOK SYSTEM "addr_book.dtd">
<ADDRBOOK xmlns:xlink="http://www.w3.org/XML/XLink/0.9">
        <ENTRY ID="pa">
                <NAME>Pieter Aaron</NAME>
                <ADDRESS>404 Error Way</ADDRESS>
                <PHONENUM DESC="Work">404-555-1234</PHONENUM>
                <PHONENUM DESC="Fax">404-555-4321</PHONENUM>
                <PHONENUM DESC="Pager">404-555-5555</PHONENUM>
                <EMAIL>pieter.aaron@inter.net</EMAIL>
        </ENTRY>
        <ENTRY-LINK xlink:link="simple" xlink:href="addr_book2.xml"/>
        <ENTRY ID="en">
                <NAME>Emeka Ndubuisi</NAME>
                <ADDRESS>42 Spam Blvd</ADDRESS>
                <PHONENUM DESC="Work">767-555-7676</PHONENUM>
                <PHONENUM DESC="Fax">767-555-7642</PHONENUM>
                <PHONENUM DESC="Pager">800-SKY-PAGEx767676</PHONENUM>
                <EMAIL>endubuisi@spamtron.com</EMAIL>
        </ENTRY>
        <ENTRY ID="vz">
                <NAME>Vasia Zhugenev</NAME>
                <ADDRESS>2000 Disaster Plaza</ADDRESS>
                <PHONENUM DESC="Work">000-987-6543</PHONENUM>
                <PHONENUM DESC="Cell">000-000-0000</PHONENUM>
                <EMAIL>vxz@magog.ru</EMAIL>
        </ENTRY>
</ADDRBOOK>"""

expected_1 = """<?xml version='1.0' encoding='UTF-8'?><!DOCTYPE doc><doc><elt xmlns:spam='http://logilab' spam:att='value1'/></doc>"""

expected_2 = """<?xml version='1.0' encoding='UTF-8'?><!DOCTYPE doc><doc>
  <elt xmlns:spam='http://logilab' spam:att='value1'/>
</doc>
"""

expected_3 = """
        <ENTRY ID='pa'>
                <NAME>Pieter Aaron</NAME>
                <ADDRESS>404 Error Way</ADDRESS>
                <PHONENUM DESC='Work'>404-555-1234</PHONENUM>
                <PHONENUM DESC='Fax'>404-555-4321</PHONENUM>
                <PHONENUM DESC='Pager'>404-555-5555</PHONENUM>
                <EMAIL>pieter.aaron@inter.net</EMAIL>
        </ENTRY>
        <ENTRY-LINK xmlns:xlink='http://www.w3.org/XML/XLink/0.9' xlink:href='addr_book2.xml' xlink:link='simple'/>
        <ENTRY ID='en'>
                <NAME>Emeka Ndubuisi</NAME>
                <ADDRESS>42 Spam Blvd</ADDRESS>
                <PHONENUM DESC='Work'>767-555-7676</PHONENUM>
                <PHONENUM DESC='Fax'>767-555-7642</PHONENUM>
                <PHONENUM DESC='Pager'>800-SKY-PAGEx767676</PHONENUM>
                <EMAIL>endubuisi@spamtron.com</EMAIL>
        </ENTRY>
        <ENTRY ID='vz'>
                <NAME>Vasia Zhugenev</NAME>
                <ADDRESS>2000 Disaster Plaza</ADDRESS>
                <PHONENUM DESC='Work'>000-987-6543</PHONENUM>
                <PHONENUM DESC='Cell'>000-000-0000</PHONENUM>
                <EMAIL>vxz@magog.ru</EMAIL>
        </ENTRY>

"""

expected_4 = """<!DOCTYPE ADDRBOOK SYSTEM "addr_book.dtd" ><ADDRBOOK xmlns:xlink='http://www.w3.org/XML/XLink/0.9'>
        <ENTRY ID='pa'>
                <NAME>Pieter Aaron</NAME>
                <ADDRESS>404 Error Way</ADDRESS>
                <PHONENUM DESC='Work'>404-555-1234</PHONENUM>
                <PHONENUM DESC='Fax'>404-555-4321</PHONENUM>
                <PHONENUM DESC='Pager'>404-555-5555</PHONENUM>
                <EMAIL>pieter.aaron@inter.net</EMAIL>
        </ENTRY>
        <ENTRY-LINK xlink:href='addr_book2.xml' xlink:link='simple'/>
        <ENTRY ID='en'>
                <NAME>Emeka Ndubuisi</NAME>
                <ADDRESS>42 Spam Blvd</ADDRESS>
                <PHONENUM DESC='Work'>767-555-7676</PHONENUM>
                <PHONENUM DESC='Fax'>767-555-7642</PHONENUM>
                <PHONENUM DESC='Pager'>800-SKY-PAGEx767676</PHONENUM>
                <EMAIL>endubuisi@spamtron.com</EMAIL>
        </ENTRY>
        <ENTRY ID='vz'>
                <NAME>Vasia Zhugenev</NAME>
                <ADDRESS>2000 Disaster Plaza</ADDRESS>
                <PHONENUM DESC='Work'>000-987-6543</PHONENUM>
                <PHONENUM DESC='Cell'>000-000-0000</PHONENUM>
                <EMAIL>vxz@magog.ru</EMAIL>
        </ENTRY>
</ADDRBOOK>
"""


def Test(tester):

    tester.startGroup("Alexander Fayolle's Problems and variations")

    tester.startTest('Bad setAttNS test')
    d=Sax2.FromXml('<doc/>')
    e = d.createElementNS('', 'elt')
    d.documentElement.appendChild(e)
    try:
        e.setAttributeNS('http://logilab', 'att', 'value1')
    except DOMException, x:
        if x.code != NAMESPACE_ERR:
            name = getExceptionName(x.code)
            tester.error("Wrong exception '%s', expected NAMESPACE_ERR" % name)
    else:
        tester.error('setAttributeNS with no prefix and non-null URI doesn\'t raise exception.')
    e.setAttributeNS('http://logilab', 'spam:att', 'value1')
    stream = cStringIO.StringIO()
    Print(d, stream=stream)
    result = stream.getvalue()
    if result != expected_1:
        tester.error('Expected\n"""%s"""\ngot\n"""%s"""'%(repr(expected_1), repr(result)))

    stream = cStringIO.StringIO()
    PrettyPrint(d, stream=stream)
    result = stream.getvalue()
    if result != expected_2:
        tester.error('Expected\n"""%s"""\ngot\n"""%s"""'%(repr(expected_2), repr(result)))
    tester.testDone()

    tester.startTest('Document Fragment Printing')
    d = Sax2.FromXml(source_1)
    df = d.createDocumentFragment()
    for n in d.documentElement.childNodes:
        df.appendChild(n.cloneNode(1))
    if len(df.childNodes) != len(d.documentElement.childNodes):
        tester.error('Docfrag append error')
    if df.childNodes.length != d.documentElement.childNodes.length:
        tester.error('Docfrag append error')
    stream = cStringIO.StringIO()
    PrettyPrint(df, stream=stream)
    result = stream.getvalue()
    if result != expected_3:
        raise Exception('Expected\n"""%s"""\ngot\n"""%s"""'%(repr(expected_3), repr(result)))
    tester.testDone()

    tester.startTest('Document Type Printing')
    d = Sax2.FromXml(source_1)
    d.doctype.__dict__['__systemId'] = "addr_book.dtd"
    stream = cStringIO.StringIO()
    PrettyPrint(d, stream=stream)
    result = stream.getvalue()
    if result != expected_4:
        raise Exception('Expected\n"""%s"""\ngot\n"""%s"""'%(repr(expected_4), repr(result)))
    tester.testDone()

    return tester.groupDone()


if __name__ == '__main__':
    import sys
    import TestSuite

    tester = TestSuite.TestSuite()
    retVal = Test(tester)
    sys.exit(retVal)
