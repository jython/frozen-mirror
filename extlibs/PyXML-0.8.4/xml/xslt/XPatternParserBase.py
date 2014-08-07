import XPattern

from xml.FtCore import get_translator

_ = get_translator("xslt")


SYNTAX_ERR_MSG = _("Error parsing pattern:\n'%s'\nSyntax error at or near '%s' Line: %d, Production Number: %s")
INTERNAL_ERR_MSG = _("Error parsing pattern:\n'%s'\nInternal error in processing at or near '%s', Line: %d, Production Number: %s, Exception: %s")

class SyntaxException(Exception):
    def __init__(self, source, lineNum, location, prodNum):
        Exception.__init__(self, SYNTAX_ERR_MSG%(source, location, lineNum, prodNum))
        self.source = source
        self.lineNum = lineNum
        self.loc = location
        self.prodNum = prodNum

class InternalException(Exception):
    def __init__(self, source, lineNum, location, prodNum, exc, val, tb):
        Exception.__init__(self, INTERNAL_ERR_MSG%(source, location, lineNum, prodNum, exc))
        self.source = source
        self.lineNum = lineNum
        self.loc = location
        self.prodNum = prodNum
        self.errorType = exc
        self.errorValue = val
        self.errorTraceback = tb

import threading
g_parseLock = threading.RLock()

class XPatternParserBase:
    def __init__(self):
        self.initialize()

    def initialize(self):
        self.results = None
        self.__stack = []
        XPattern.cvar.g_prodNum = "-1"
        XPattern.cvar.g_errorOccured = 0

    def parse(self,st):
        g_parseLock.acquire()
        try:
            self.initialize()
            XPattern.my_XPatternparse(self,st)
            if XPattern.cvar.g_errorOccured == 1:
                raise SyntaxException(
                    st,
                    XPattern.cvar.lineNum,
                    XPattern.cvar.g_errorLocation,
                    XPattern.cvar.g_prodNum)
            if XPattern.cvar.g_errorOccured == 2:
                raise InternalException(
                    st,
                    XPattern.cvar.lineNum,
                    XPattern.cvar.g_errorLocation,
                    XPattern.cvar.g_prodNum,
                    XPattern.cvar.g_errorType,
                    XPattern.cvar.g_errorValue,
                    XPattern.cvar.g_errorTraceback)
            return self.__stack
        finally:
            g_parseLock.release()

    def pop(self):
        if len(self.__stack):
            rt = self.__stack[-1]
            del self.__stack[-1]
            return rt
        self.raiseException("Pop with 0 stack length")

    def push(self,item):
        self.__stack.append(item)

    def empty(self):
        return len(self.__stack) == 0

    def size(self):
        return len(self.__stack)

    def raiseException(self, message):
        raise Exception(message + "\n" +
                        "EBNF ProductionNumber: " +
                        str(XPattern.cvar.g_prodNum)
                        )

    ### Callback methods ###

def PrintSyntaxException(e):
    print "********** Syntax Exception **********"
    print "Exception at or near '%s'" % e.loc
    print "  Line: %d, Production Number: %s" % (e.lineNum, str(e.prodNum))

def PrintInternalException(e):
    print "********** Internal Exception **********"
    print "Exception at or near '%s'" % e.loc
    print "  Line: %d, Production Number: %s" % (e.lineNum, e.prodNum)
    print "    Exception: %s" % e.errorType
    print "Original traceback:"
    import traceback
    traceback.print_tb(e.errorTraceback)

if __name__ == "__main__":
    import sys
    p = XPatternParserBase()
    if len(sys.argv) == 2:
        l = open(sys.argv[1],"r").read()
    else:
        l = raw_input(">>>")
    try:
        p.parse(l)
    except InternalException, e:
        PrintInternalException(e)
    except SyntaxException, e:
        PrintSyntaxException(e)
