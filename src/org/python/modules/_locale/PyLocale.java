// (c) 2019 Jython Developers
// Licensed to PSF under a contributor agreement

package org.python.modules._locale;

import org.python.core.PyDictionary;
import org.python.core.PyString;

/**
 * Definition of a Python native locale implementation. Based on Python locale
 * module behaviour and implicit dependencies, and the {@code _localemodule.c}
 * implementation in CPython.
 * 
 * @since Jython 2.7.2
 */
public interface PyLocale {

    public PyDictionary localeconv();

    public PyString getLocaleString();

    public PyString getUnderlyingLocale();

    public int strcoll(PyString str1, PyString str2);

    public PyString strxfrm(PyString str1);

    public String[] getShortWeekdays();

    public String[] getWeekdays();

    public String[] getShortMonths();

    public String[] getMonths();

    public String[] getAmPmStrings();
}
