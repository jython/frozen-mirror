import sys, traceback, os

OK = 0
PASSED = 1
FAILED = -1

class TestItem:
    def __init__(self, suite, title):
        self.suite = suite
        self.title = title
        self.messages = []
        self.hasErrors = 0
        self.hasWarnings = 0


        if suite.useColor:
            #self.moveTo = '\033[%dG' % (suite.columns - 9)
            self.colorSuccess = '\033[1;32m'
            self.colorFailure = '\033[1;31m'
            self.colorWarning = '\033[1;33m'
            self.colorNormal = '\033[0;39m'
        else:
            self.colorSuccess = ''
            self.colorFailure = ''
            self.colorWarning = ''
            self.colorNormal = ''

    def finish(self):
        if self.hasErrors:
            msg = self._failure()
            retVal = FAILED
        elif self.hasWarnings:
            msg = self._passed()
            retVal = PASSED
        else:
            msg = self._success()
            retVal = OK

        spaces = self.suite.columns - 9
        spaces = spaces - len(self.title)
        title = self.title + ' '*spaces + msg

        for msg in self.messages:
            print msg[0]
        return retVal

    def debug(self, msg):
        self.messages.append(msg)

    def message(self, msg):
        self.messages.append(msg)

    def warning(self, msg):
        self.messages.append(msg)
        self.hasWarnings = 1

    def error(self, msg, saveTrace=0):
        if self.suite.stopOnError:
            raise msg
        if saveTrace:
            tb = sys.exc_info()[-1]
            ftb = traceback.format_list(traceback.extract_tb(tb))
            if ftb:
                msg = msg + '\n'
                for t in ftb:
                    msg = msg + t
        self.messages.append(msg)
        self.hasErrors = 1

    ### Internal Methods ###
    def _success(self):
        return '[%s  OK  %s]' %(self.colorSuccess, self.colorNormal)

    def _passed(self):
        return '[%sPASSED%s]' %(self.colorWarning, self.colorNormal)

    def _failure(self):
        return '[%sFAILED%s]' %(self.colorFailure, self.colorNormal)


class TestGroup:
    def __init__(self, suite, title=None):
        self.suite = suite
        self.title = title
        self.tests = []
        self.retVal = OK

        if title:
            msg = '********** ' + title + ' **********'
            print msg

    ### Methods ###

    def finish(self):
        for test in self.tests:
            self.retVal = self.retVal or test.finish()
        return self.retVal


    def startTest(self, title):
        test = TestItem(self.suite, title)
        self.tests.append(test)

    def testDone(self):
        if self.tests:
            self.retVal = self.retVal | self.tests[-1].finish()
            del self.tests[-1]
            return self.retVal


class TestSuite:
    def __init__(self, stopOnError=1, useColor=0, cols=80):
        if os.name == 'posix':
            self.useColor = 1
        else:
            self.useColor = useColor
        self.stopOnError = stopOnError
        self.useColor = useColor
        self.columns = cols
        self.groups = []
        self.retVal = OK

    def __del__(self):
        retVal = OK
        while len(self.groups):
            retVal = retVal or group[-1].finish()
        return retVal

    ### Methods ###

    def startGroup(self, title):
        group = TestGroup(self, title)
        self.groups.append(group)

    def groupDone(self):
        retVal = OK
        if self.groups:
            retVal = self.groups[-1].finish()
            del self.groups[-1]
        return retVal

    def startTest(self, title):
        if not self.groups:
            self.startGroup(self)
            print 'Added (null) group'
        self.groups[-1].startTest(title)

    def testDone(self):
        if self.groups:
            self.groups[-1].testDone()

    def testResults(self,expected,actual, done = 1):
        if expected != actual:
            self.error("Expected %s, got %s" % (expected,actual))
            return 0
        elif done:
            self.testDone()
        return 1
    def message(self, msg):
        if self.groups:
            if self.groups[-1].tests:
                self.groups[-1].tests[-1].message(msg)

    def warning(self, msg):
        if self.groups:
            if self.groups[-1].tests:
                self.groups[-1].tests[-1].warning(msg)

    def error(self, msg, saveTrace=0):
        if self.groups:
            if self.groups[-1].tests:
                self.groups[-1].tests[-1].error(msg, saveTrace)
