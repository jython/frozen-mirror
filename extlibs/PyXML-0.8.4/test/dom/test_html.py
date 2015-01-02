def test(tester):
    import os, string, sys
    if not os.path.exists('html/test.py'):
        tester.error('Cannot run the HTML test suite')
        return 1

    currdir = os.getcwd()
    os.chdir('html')

    files = __import__('test').fileList
    for file in files:
        modName = 'test_%s' % string.lower(file)
        if sys.modules.has_key(modName):
            del sys.modules[modName]
        tester.startGroup('HTML %s' % file)
        module = __import__('test_%s' % string.lower(file))
        module.test()
        tester.groupDone()

    os.chdir(currdir)
    return


if __name__ == '__main__':
    import sys

    import TestSuite
    tester = TestSuite.TestSuite()
    retVal = test(tester)
    sys.exit(retVal)
