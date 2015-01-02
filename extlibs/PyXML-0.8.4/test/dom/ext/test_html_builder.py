########################################################################
#
# File Name:   TestHtmlBuilder.py
#
#
"""
Test suite for the Html portion of the builder.
WWW: http://4suite.com/4Dom        e-mail: support@4suite.com
Copyright (c) 2000 Fourthought, Inc., USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


def test():
    from xml.dom.ext.reader import HtmlLib
    from xml.dom import ext

    d = HtmlLib.FromHtmlFile('single.html')
    ext.PrettyPrint(d)

    d = HtmlLib.FromHtmlFile('mulit-single.html')
    ext.PrettyPrint(d)

    d = HtmlLib.FromHtmlFile('bigTest.html')
    ext.PrettyPrint(d)

if __name__ == '__main__':
    test()
