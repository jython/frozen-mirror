#
# Top-level program for XML test suite
#

import regrtest
del regrtest.STDTESTS[:]

def main():
    tests = regrtest.findtests('.')
    regrtest.main( tests,  testdir = '.' )

if __name__ == '__main__':
    main()
