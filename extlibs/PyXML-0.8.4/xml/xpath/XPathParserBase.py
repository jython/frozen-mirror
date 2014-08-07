try:
    import os, gettext
    locale_dir = os.path.split(__file__)[0]
    gettext.install('4Suite', locale_dir)
except (ImportError,AttributeError,IOError):
    def _(msg):
        return msg

SYNTAX_ERR_MSG = _("Error parsing expression:\n'%s'\nSyntax error at or near '%s' Line: %d")
INTERNAL_ERR_MSG = _("Error parsing expression:\n'%s'\nInternal error in processing at or near '%s', Line: %d, Exception: %s")

class SyntaxException(Exception):
    def __init__(self, source, lineNum, location):
        Exception.__init__(self, SYNTAX_ERR_MSG%(source, location, lineNum))
        self.source = source
        self.lineNum = lineNum
        self.loc = location

class InternalException(Exception):
    def __init__(self, source, lineNum, location, exc, val, tb):
        Exception.__init__(self, INTERNAL_ERR_MSG%(source, location, lineNum, exc))
        self.source = source
        self.lineNum = lineNum
        self.loc = location
        self.errorType = exc
        self.errorValue = val
        self.errorTraceback = tb

class XPathParserBase:
    def __init__(self):
        self.initialize()

    def initialize(self):
        self.results = None
        self.__stack = []
        XPath.cvar.g_errorOccured = 0

    def parse(self,st):
        g_parseLock.acquire()
        try:
            self.initialize()
            XPath.my_XPathparse(self,st)
            if XPath.cvar.g_errorOccured == 1:
                raise SyntaxException(
                    st,
                    XPath.cvar.lineNum,
                    XPath.cvar.g_errorLocation)
            if XPath.cvar.g_errorOccured == 2:
                raise InternalException(
                    st,
                    XPath.cvar.lineNum,
                    XPath.cvar.g_errorLocation,
                    XPath.cvar.g_errorType,
                    XPath.cvar.g_errorValue,
                    XPath.cvar.g_errorTraceback)
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
        raise Exception(message)

    ### Callback methods ###

def PrintSyntaxException(e):
    print "********** Syntax Exception **********"
    print "Exception at or near '%s'" % e.loc
    print "  Line: %d" % (e.lineNum)

def PrintInternalException(e):
    print "********** Internal Exception **********"
    print "Exception at or near '%s'" % e.loc
    print "  Line: %d" % (e.lineNum)
    print "    Exception: %s" % e.errorType
    print "Original traceback:"
    import traceback
    traceback.print_tb(e.errorTraceback)
