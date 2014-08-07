#!/usr/bin/env python
import string, time
import TestSuite

### Methods ###

def runTests(tests, testSuite):
    banner = 'Performing a test of DOM Core/Traversal/HTML'
    markers = '#'*((testSuite.columns - len(banner)) / 2 - 1)
    print markers, banner, markers

    total = 0.0
    for test in tests:
        module = __import__('test_' + string.lower(test))
        start = time.time()
        module.test(testSuite)
        total = total + time.time() - start
    return total



### Application ###

if __name__ == '__main__':
    logLevel = 1
    logFile = None
    haltOnError = 1

    test_list = ['Node',
                 'NodeList',
                 'NamedNodeMap',
                 'NodeIterator',
                 'TreeWalker',
                 'Attr',
                 'Element',
                 'DocumentFragment',
                 'Document',
                 'DOMImplementation',
                 'CharacterData',
                 'Comment',
                 'Text',
                 'CDATASection',
                 'DocumentType',
                 'Entity',
                 'EntityReference',
                 'Notation',
                 'ProcessingInstruction',
                 'Range',
                 'Struct',
                 'HTML',
                 #'Demo',
                 #'Pythonic'
                 ]

    import sys, os, getopt

    prog_name = os.path.split(sys.argv[0])[1]
    short_opts = 'hl:nqtv:'
    long_opts = ['help',
                 'log=',
                 'no-error'
                 'tests'
                 'quiet',
                 'verbose='
                 ]

    usage = '''Usage: %s [options] [[all] [test]...]
Options:
  -h, --help             Print this message and exit
  -l, --log <file>       Write output to a log file (default=%s)
  -n, --no-error         Continue testing if error condition
  -q, --quiet            Display as little as possible
  -t, --tests            Show a list of tests that can be run
  -v, --verbose <level>  Set the output level (default=%s)
                           0 - display nothing
                           1 - errors only (same as --quiet)
                           2 - warnings and errors
                           3 - information, warnings and errors
                           4 - display everything
''' %(prog_name, logFile, logLevel)

    command_line_error = 0
    bad_options = []

    finished = 0
    args = sys.argv[1:]
    while not finished:
        try:
            optlist, args = getopt.getopt(args, short_opts, long_opts)
        except getopt.error, data:
            bad_options.append(string.split(data)[1])
            args.remove(bad_options[-1])
            command_line_error = 1
        else:
            finished = 1

    display_usage = 0
    display_tests = 0
    for op in optlist:
        if op[0] == '-h' or op[0] == '--help':
            display_usage = 1
        elif op[0] == "-l" or op[0] == '--log':
            logFile = op[1]
        elif op[0] == '-n' or op[0] == '--no-error':
            haltOnError = 0
        elif op[0] == '-t' or op[0] == '--tests':
            display_tests = 1
        elif op[0] == '-q' or op[0] == '--quiet':
            logLevel = 1
        elif op[0] == '-v' or op[0] == '--verbose':
            logLevel = int(op[1])

    all_tests = 0
    if args:
        lower_test = []
        for test in test_list:
            lower_test.append(string.lower(test))
        for test in args:
            if string.lower(test) == 'all':
                all_tests = 1
                break
            if string.lower(test) not in lower_test:
                print "%s: Test not found '%s'" %(prog_name, test)
                args.remove(test)
                display_tests = 1

    if len(args) and not all_tests:
        tests = args
    elif not display_tests:
        tests = test_list

    if command_line_error or display_usage or display_tests:
        for op in bad_options:
            print "%s: Unrecognized option '%s'" %(prog_name,op)
        if display_usage:
            print usage
        if display_tests:
            print 'Available tests are:'
            for t in test_list:
                print '  %s' % t
        sys.exit(command_line_error)

    testSuite = TestSuite.TestSuite(haltOnError)

    total = runTests(tests, testSuite)

    print "Test Time - %.3f secs" % total
