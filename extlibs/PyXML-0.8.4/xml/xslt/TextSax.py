########################################################################
#
# File Name:            TextSax.py
#
#
#
"""
Components for reading Text files from a SAX-like producer.
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 1999-2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


import sys, string, cStringIO

class TextGenerator:
    def __init__(self, keepAllWs=0):
        self.__currText = ''

    def getRootNode(self):
        return self.__currText

    def startElement(self, name, attribs):
        st = "<" + name
        for attr in attribs.keys():
            st = st + " %s = %s " % (attr,attribs[attr])
        st = st + '>\n'
        self.__currText = self.__currText + st

    def endElement(self, name):
        st =  "</%s>" % name
        self.__currText = self.__currText + st

    def ignorableWhitespace(self, ch, start, length):
        """
        If 'keepAllWs' permits, add ignorable white-space as a text node.
        Remember that a Document node cannot contain text nodes directly.
        If the white-space occurs outside the root element, there is no place
        for it in the DOM and it must be discarded.
        """
        if self.__keepAllWs:
            self.__currText = self.__currText + ch[start:start+length]

    def characters(self, ch, start, length):
        self.__currText = self.__currText + ch[start:start+length]


    #Overridden ErrorHandler methods
    #def warning(self, exception):
    #   raise exception

    def error(self, exception):
        raise exception

    def fatalError(self, exception):
        raise exception


