'''Java locale differences from JDK 9 onwards, and locale variation on
developer machines, break test_strptime tests. This manifests more on Windows.
Rather than diverge from the Python source, this overrides with extra locale
setup'''

from test.test_strptime import *
from test import test_support


def test_main(initialize=True):
    test_support.reset_locale_toC(initialize)

    test_support.run_unittest(
        getlang_Tests,
        LocaleTime_Tests,
        TimeRETests,
        StrptimeTests,
        Strptime12AMPMTests,
        JulianTests,
        CalculationTests,
        CacheTests
    )


if __name__ == '__main__':
    test_main(initialize=False)


