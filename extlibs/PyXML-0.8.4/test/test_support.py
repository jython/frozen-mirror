"""PyUNIT-based compatibility module for the test.test_support module.

When running PyUNIT-based tests, this should be used for the
run_suite() and run_unittest() functions.
"""

from test.test_support import verbose, TestFailed

try:
    from test.test_support import run_suite, run_unittest
except ImportError:

    #=======================================================================
    # Preliminary PyUNIT integration.

    import sys
    import unittest


    class BasicTestRunner:
        def run(self, test):
            result = unittest.TestResult()
            test(result)
            return result


    def run_suite(suite, testclass=None):
        """Run tests from a unittest.TestSuite-derived class."""
        if verbose:
            runner = unittest.TextTestRunner(sys.stdout, verbosity=2)
        else:
            runner = BasicTestRunner()

        result = runner.run(suite)
        if not result.wasSuccessful():
            if len(result.errors) == 1 and not result.failures:
                err = result.errors[0][1]
            elif len(result.failures) == 1 and not result.errors:
                err = result.failures[0][1]
            else:
                if testclass is None:
                    msg = "errors occurred; run in verbose mode for details"
                else:
                    msg = "errors occurred in %s.%s" \
                          % (testclass.__module__, testclass.__name__)
                raise TestFailed(msg)
            raise TestFailed(err)


    def run_unittest(testclass):
        """Run tests from a unittest.TestCase-derived class."""
        run_suite(unittest.makeSuite(testclass), testclass)
