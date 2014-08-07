# This module contains common functionality used by xvcmd.py and xpcmd.py

import sys,string

from xml.parsers.xmlproc import xmlapp, utils

# Backwards compatibility declarations

ESISDocHandler = utils.ESISDocHandler
Canonizer = utils.Canonizer
DocGenerator = utils.DocGenerator

# Error handler

class MyErrorHandler(xmlapp.ErrorHandler):

    def __init__(self, locator, parser, warnings, entstack, rawxml):
        xmlapp.ErrorHandler.__init__(self,locator)
        self.show_warnings=warnings
        self.show_entstack=entstack
        self.show_rawxml=rawxml
        self.parser=parser
        self.reset()

    def __show_location(self,prefix,msg):
        print "%s:%s: %s" % (prefix,self.get_location(),msg)
        if self.show_entstack:
            print "  Document entity"
            for item in self.parser.get_current_ent_stack():
                print "  %s: %s" % item
        if self.show_rawxml:
            raw=self.parser.get_raw_construct()
            if len(raw)>50:
                print "  Raw construct too big, suppressed."
            else:
                print "  '%s'" % raw

    def get_location(self):
        return "%s:%d:%d" % (self.locator.get_current_sysid(),\
                               self.locator.get_line(),
                               self.locator.get_column())

    def warning(self,msg):
        if self.show_warnings:
            self.__show_location("W",msg)
            self.warnings=self.warnings+1

    def error(self,msg):
        self.fatal(msg)

    def fatal(self,msg):
        self.__show_location("E",msg)
        self.errors=self.errors+1

    def reset(self):
        self.errors=0
        self.warnings=0
