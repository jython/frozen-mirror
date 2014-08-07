#!/usr/bin/env python
import os

def test(testSuite):

    #rt = os.system("cd ../demo && python dom_from_html_file.py employee_table.html")
    #if rt:
    #    return 0

    rt = os.system("cd ../demo && python dom_from_xml_file.py addr_book1.xml")
    if rt:
        return 0



    #os.system("cd ../demo && python generate_html1.py")
    #if rt:
    #    return 0

    rt = os.system("cd ../demo && python iterator1.py addr_book1.xml")
    if rt:
        return 0

    rt = os.system("cd ../demo && python visitor1.py addr_book1.xml")
    if rt:
        return 0


    rt = os.system("cd ../demo && python trace_ns.py book_catalog1.xml")
    if rt:
        return 0

    rt = os.system("cd ../demo && python xll_replace.py addr_book1.xml")
    if rt:
        return 0

    rt = os.system("cd ../demo && python xpointer_query.py root\(\).child\(1\) addr_book1.xml")
    if rt:
        return 0

    return 1
