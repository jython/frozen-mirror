// (c) 2019 Jython Developers
// Licensed to PSF under a contributor agreement

package org.python.modules._locale;

import java.nio.charset.Charset;
import java.text.Collator;
import java.text.DateFormatSymbols;
import java.text.DecimalFormat;
import java.text.DecimalFormatSymbols;
import java.text.NumberFormat;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.Locale;
import java.util.Set;

import org.python.core.ClassDictInit;
import org.python.core.Py;
import org.python.core.PyDictionary;
import org.python.core.PyException;
import org.python.core.PyInteger;
import org.python.core.PyList;
import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.core.PyStringMap;
import org.python.core.PySystemState;
import org.python.core.PyUnicode;

/**
 *
 * Java native implementation of underlying locale functions, fitting the
 * interface defined or implied by the locale package.
 *
 * Functional documentation can be found in the Python module docstring.
 * Additional implementation details for users of this class are captured
 * below.
 * <p>
 * Unicode. In general, Java and its locale settings are quite unicode heavy,
 * making rich use of different symbols for eg currencies. This solution allows
 * some of that to leak through by encoding the Java locale value with the
 * current character encoding. The Python locale module is quite conservative
 * and tends to keep things as solely strings. Python 2.x usually supports only
 * string / ascii by default in many cases, and only unicode when asked. This
 * is a little less conservative while only allowing values consistent with the
 * current encoding.
 * <p>
 * An example of this is Python using EUR rather than the Euro symbol € /
 * {@code 'u20ac'}, probably because € is only available in Unicode. In the
 * Java implementation, if UTF-8 encoding is set, the resulting entry in
 * {@code localeconv()['currency_code']} is {@code '\xe2\x82\xac'}. This can be
 * used by {@code print()} and related functions directly. Encoding failures in
 * for {@code currency_symbol} fallback to {@code int_curr_symbol} (eg EUR).
 * <p>
 * The C emulation locale uses only ANSI characters in non-unicode strings, in
 * keeping with it being the locale of last resort and maximum compatibility.
 * <p>
 * Positive sign position ({@code p_sign_posn}) is not a distinguished concept
 * in Java and so this is hardcoded to 3.
 * <p>
 * This class object is used as a static thread lock by private method
 * {@code changeCurrentLocale()} when changing locales via
 * {@link #setlocale(PyInteger,PyString)}.
 *
 * @since Jython 2.7.2
 * 
 * 
 */
public class _locale implements ClassDictInit {

    /**
     *
     * The {@code locale} module exposes {@code _locale.Error} as
     * {@code locale.Error}. Some Python functions, including
     * {@code strptime()}, depend on {@code locale.Error}, making it part of the
     * public API for native locale implementations.
     *
     */
    public static PyObject Error;

    public static PyException LocaleException(String message) {
        return new PyException(Error, message);
    }

    public static final PyString __doc__ = new PyString(
        "The _locale module exposes locale functions in the underlying "
        + "operating system or platform in a consistent way, for use by "
        + "the Python locale module. It is a native Java implementation, "
        + "paralleling libmodule.c in CPython and its dependence on C "
        + "libraries provided by the OS.\n"
        + "This module is currently in beta, and is enabled with the "
        + "registry property ``python.locale.control``. It is "
        + "disabled by default, resulting in jython 2.7.1 (and previous) "
        + "locale behaviour.\n" 
        + "\n"
        + "+-------------------+-----------------------------------------+\n"
        + "+ Property Value    + Behaviour                               |\n"
        + "+===================+=========================================+\n"
        + "| jython2_legacy    | Mix of implicit Java locale and         |\n"
        + "|                   | emulated 'C'. Text and date formatting  |\n"
        + "|                   | mostly Java locale (eg ``%b``).         |\n"
        + "|                   | ``asctime()`` matches C emulation       |\n"
        + "|                   | ``setlocale()`` always errors by design.|\n"
        + "|                   | This matches version 2.7.1 and previous |\n"
        + "|                   | behaviour. Will be deprecated in future |\n"
        + "|                   | versions.                               |\n"
        + "+-------------------+-----------------------------------------+\n"
        + "| settable          | Java platform locale services made      |\n"
        + "|                   | available via locale module.            |\n"
        + "|                   | ``setlocale()`` works, using Java locale|\n"
        + "|                   | identifiers and LC_ALL (only). C locale |\n"
        + "|                   | available via ``setlocale()``. Initial  |\n"
        + "|                   | locale and encoding per Java defaults.  |\n"
        + "+-------------------+-----------------------------------------+\n"
        + "| '' or unset       | As per ``jython2_legacy``.              |\n"
        + "|                   | In future versions, per ``settable``.   |\n"
        + "+-------------------+-----------------------------------------+\n");

    public static final String PYTHON_LOCALE_CONTROL = "python.locale.control";

    public static final String LOCALE_CONTROL_SETTABLE = "settable";
    public static final String LOCALE_CONTROL_JYTHON2_LEGACY = "jython2_legacy";

    // These values are the same as glibc locale/bits/locale.h
    // Specific integer constants are not mandated by the POSIX locale spec,
    // so an existing standard seemed as good an arbitrary set of values as
    // any
    private static final int __LC_CTYPE = 0;
    private static final int __LC_NUMERIC = 1;
    private static final int __LC_TIME = 2;
    private static final int __LC_COLLATE = 3;
    private static final int __LC_MONETARY = 4;
    private static final int __LC_MESSAGES = 5;
    private static final int __LC_ALL = 6;
    @SuppressWarnings("unused")
    private static final int __LC_PAPER = 7;
    @SuppressWarnings("unused")
    private static final int __LC_NAME = 8;
    @SuppressWarnings("unused")
    private static final int __LC_ADDRESS = 9;
    @SuppressWarnings("unused")
    private static final int __LC_TELEPHONE = 10;
    @SuppressWarnings("unused")
    private static final int __LC_MEASUREMENT = 11;
    @SuppressWarnings("unused")
    private static final int __LC_IDENTIFICATION = 12;

    public static final PyInteger LC_CTYPE = new PyInteger(__LC_CTYPE);
    public static final PyInteger LC_NUMERIC = new PyInteger(__LC_NUMERIC);
    public static final PyInteger LC_TIME = new PyInteger(__LC_TIME);
    public static final PyInteger LC_COLLATE = new PyInteger(__LC_COLLATE);
    public static final PyInteger LC_MONETARY = new PyInteger(__LC_MONETARY);
    public static final PyInteger LC_MESSAGES = new PyInteger(__LC_MESSAGES);
    public static final PyInteger LC_ALL = new PyInteger(__LC_ALL);
    // Remaining constants not used by locale.py so are not exposed here

    // 127 chosen as consistent with hardcoded default in locale.py for C locale
    public static final int CHAR_MAX = 127;
    public static final PyInteger CHAR_MAX_PY_INT = new PyInteger(127);

    public static final PyString C_LOCALE_PY_STRING = new PyString("C");

    private static final Set<Locale> AVAILABLE_LOCALES;

    // This has a subtle initialization dependency on the codecs module
    // due to the initialization in JyLocale(). Let the interpreter
    // initialize via classDictInit().
    private static PyLocale currentLocale = null;
    private static volatile boolean settable = false;

    static {
        final Set<Locale> set =
                new HashSet<>(Arrays.asList(Locale.getAvailableLocales()));
        AVAILABLE_LOCALES = Collections.unmodifiableSet(set);
    }

    @SuppressWarnings("serial")
    public static void initClassExceptions(PyObject exceptions) {
        PyObject baseException = exceptions.__finditem__("BaseException");
        Error = Py.makeClass("_locale.Error", baseException, new PyStringMap() {

            {
                __setitem__("__module__", Py.newString("_locale"));
            }
        });
    }

    public static void classDictInit(PyObject dict) {
        settable = false;
        dict.__setitem__("Error", Error);
        try {
            currentLocale = new JyLocale(Locale.getDefault(),
                    Charset.defaultCharset().name());
        } catch (Throwable t) {
            throw Py.ImportError(
                    "Jython failed to load default Java locale, falling back. "
                            + t.getMessage());
        }
        final String localeControl =
                PySystemState.registry.getProperty(PYTHON_LOCALE_CONTROL, "");
        if ("".equals(localeControl)
                || LOCALE_CONTROL_JYTHON2_LEGACY.equals(localeControl)) {
            throw Py.ImportError(
                    "Jython locale support not enabled with python.locale.control, falling back");
        }
        if (!LOCALE_CONTROL_SETTABLE.equals(localeControl)) {
            throw Py.ImportError(
                    "Jython locale support python.locale.control unrecognized value, falling back");
        }
        settable = true;
    }

    public static boolean isSettable() {
        return settable;
    }

    protected static void putConvEntry(PyDictionary result, String key,
            String value) {
        result.put(new PyString(key), new PyString(value));
    }

    protected static void putConvEntry(PyDictionary result, String key,
            char value) {
        result.put(new PyString(key), new PyString(value));
    }

    protected static void putConvEntry(PyDictionary result, String key,
            PyObject value) {
        result.put(new PyString(key), value);
    }

    public static PyString __doc___localeconv = new PyString(
            "Database of local conventions, mapped from Java.\n"
        + ""
        + "Note that Java locale information is relatively unicode-rich, "
        + "particularly for currency symbols. Where that is not supported "
        + "by the current encoding, the international currency symbol is "
        + "used.\n" + ""
        + "C locale emulation matches CPython C locale emulation.");

    public static PyDictionary localeconv() {
        return currentLocale.localeconv();
    }

    public static PyString __doc___strcoll = new PyString(
            "Compare Java (unicode) strings using the Java collator for the "
        + "current locale, and the encoding normalization provided by "
        + "strxfrm\n." + ""
        + "In the 'C' locale, this simply calls str.__cmp__() ");

    public static int strcoll(PyString str1, PyString str2) {
        return currentLocale.strcoll(str1, str2);
    }

    public static PyString __doc___strxfrm = new PyString(
            "Normalize a string to unicode, for common comparison, using the "
        + "locale encoding.\n" + ""
        + "In the 'C' locale, this is a no-op, returning the parameter.");

    public static PyString strxfrm(PyString str1) {
        return currentLocale.strxfrm(str1);
    }

    public static int negativeSignPosition(DecimalFormat df) {
        String prefix = df.getNegativePrefix();
        String suffix = df.getNegativeSuffix();
        if ("".equals(suffix)) {
            if ("".equals(prefix)) {
                // Nothing is specified in this locale.
                return CHAR_MAX;
            }
        }
        if (prefix.startsWith("(") && suffix.endsWith(")")) {
            // Currency and value are surrounded by parentheses.
            return 0;
        }
        final String MINUS =
                String.valueOf(df.getDecimalFormatSymbols().getMinusSign());
        if (prefix.startsWith(MINUS)) {
            // The sign should precede the value and currency symbol.
            return 1;
        }
        if (prefix.endsWith(MINUS)) {
            // The sign should immediately precede the value.
            return 3;
        }
        if (suffix.startsWith(MINUS)) {
            // The sign should immediately follow the value.
            return 4;
        }
        // The sign should follow the value and currency symbol.
        return 2;
    }

    public static int positiveCurrencyPrecedesValue(DecimalFormat df) {
        return currencyPrecedesValue(df, df.getPositivePrefix());
    }

    public static int negativeCurrencyPrecedesValue(DecimalFormat df) {
        return currencyPrecedesValue(df, df.getNegativePrefix());
    }

    private static int currencyPrecedesValue(DecimalFormat df, String prefix) {
        if (prefix.contains(df.getDecimalFormatSymbols().getCurrencySymbol())) {
            return 1;
        }
        return 0;
    }

    public static int positiveSeparatedBySpace(DecimalFormat df) {
        return separatedBySpace(df.getPositivePrefix(), df.getPositiveSuffix());
    }

    public static int negativeSeparatedBySpace(DecimalFormat df) {
        return separatedBySpace(df.getNegativePrefix(), df.getNegativeSuffix());
    }

    public static int separatedBySpace(String prefix, String suffix) {
        if ((!prefix.isEmpty()
                && isExtendedWhitespace(prefix.charAt(prefix.length() - 1)))
                || (!suffix.isEmpty()
                        && isExtendedWhitespace(suffix.charAt(0)))) {
            return 1;
        }
        return 0;
    }

    /**
     * Includes non-breaking space, but not extended codepoints
     */
    public static boolean isExtendedWhitespace(char c) {
        return Character.isWhitespace(c) || '\u00A0' == c;
    }

    public static PyString setlocale(PyInteger category) {
        return currentLocale.getLocaleString();
    }

    public static PyString __doc___setlocale = new PyString(
            "Sets the locale given a category and normalized locale string.\n"
        + ""
        + "Only category LC_ALL is supported. Other categories such as "
        + "LC_TIME or LC_NUMERIC result in a locale.Error." 
        + "\n"
        + "Normalized format is per RFC 1766, but using underscores instead "
        + "of dashes, eg zh_CH.UTF-8. Briefly, the format is "
        + "[language]_[locality].[encoding], where [language] is a two "
        + "character language identifer, locality is a regional indicator, "
        + "and encoding is a character encoding. Other examples are "
        + "en_AU.ISO8859-1 and de_DE.ISO8859-15. "
        + "\n" + ""
        + "If this is an empty locale, the same language tag will be tried "
        + "with dashes instead of underscores, ie [lanuage]-[locality]."
        + "\n"
        + "Normalization would usually be done by the enclosing locale module."
        + "\n"
        + "This function treats a missing encoding as using UTF-8.\n");

    /**
     *
     * Java Locale loading behaviour is quite forgiving, or uninformative,
     * depending on your perspective. It will return a dummy locale for any
     * language tag that fits the syntax, or make various attempts to
     * approximate a locale. This solution instead follows the stricter Python
     * behaviour of requiring a particular locale to be installed.
     */
    public static PyString setlocale(PyInteger category, PyString locale) {
        Py.writeDebug("_locale", "setlocale(category,locale==" + locale + ")");
        if (locale == null || locale.equals(Py.None)
                || locale.equals(currentLocale.getLocaleString())) {
            return setlocale(category);
        }
        if (!category.equals(LC_ALL)) {
            // Py.NotImplementedError not used as dependencies exist on
            // locale.Error
            throw LocaleException(
                    "Only LC_ALL is supported in this version of Jython");
        }
        if (locale.equals(C_LOCALE_PY_STRING)) {
            changeCurrentLocale(new CEmulationLocale());
            return C_LOCALE_PY_STRING;
        }
        String localeStr = locale.toString();
        String[] localeParts = localeStr.split("\\.");
        String language;
        String encoding = "UTF-8";
        if (localeParts.length >= 3) {
            throw LocaleException(
                    "Does not conform to [language]_[locality].[encoding] format: "
                            + locale.toString());
        }
        if (localeParts.length == 1) {
            language = localeStr;
        } else {
            // == 2
            language = localeParts[0];
            encoding = localeParts[1];
        }
        Locale newLocale = loadLocale(language);
        if (!isAvailableLocale(newLocale)) {
            String underscoreAlias = language.replace('_', '-');
            newLocale = loadLocale(underscoreAlias);
            if (!isAvailableLocale(newLocale)) {
                throw LocaleException("No locale found: " + locale.toString());
            }
        }
        changeCurrentLocale(new JyLocale(newLocale, encoding));
        return currentLocale.getLocaleString();
    }

    private static boolean isAvailableLocale(Locale locale) {
        return locale != null && !locale.toString().isEmpty()
                && AVAILABLE_LOCALES.contains(locale);
    }

    private static Locale loadLocale(String language) {
        Locale newLocale = Locale.forLanguageTag(language);
        Py.writeDebug("_locale",
                "Current: " + currentLocale.getUnderlyingLocale());
        Py.writeDebug("_locale",
                "New: " + newLocale + " loaded with tag: " + language);
        return newLocale;
    }

    private static synchronized void changeCurrentLocale(PyLocale pyLocale) {
        Py.writeDebug("_locale",
                "Locale changed to: " + pyLocale.getLocaleString());
        currentLocale = pyLocale;
    }

    public static PyLocale getPyLocale() {
        return currentLocale;
    }

}


/**
 *
 * Sources locale information from standard Java API functions, such as that in
 * {@link java.util.Locale} and {@link java.text.DecimalFormat}.
 *
 * @Immutable
 *
 */
class JyLocale implements PyLocale {

    private Locale locale;
    private String encoding;
    private DecimalFormat decimalFormat;
    private DecimalFormat currencyFormat;
    private PyDictionary conv;
    private Collator collator;
    private DateFormatSymbols dfSymbols;

    public JyLocale(Locale locale, String encoding) {
        resetLocale(locale, encoding);
    }

    private void resetLocale(Locale locale, String encoding) {
        this.locale = locale;
        this.encoding = encoding;
        this.decimalFormat = (DecimalFormat)NumberFormat.getInstance(locale);
        this.currencyFormat =
                (DecimalFormat)NumberFormat.getCurrencyInstance(locale);
        this.conv = initLocaleConv();
        this.collator = Collator.getInstance(locale);
        this.dfSymbols = DateFormatSymbols.getInstance(locale);
    }

    @Override
    public PyDictionary localeconv() {
        return conv;
    }

    private PyDictionary initLocaleConv() {
        PyDictionary result = new PyDictionary();
        DecimalFormat df = getDecimalFormat();
        DecimalFormat cf = getCurrencyFormat();
        DecimalFormatSymbols dfs = df.getDecimalFormatSymbols();
        DecimalFormatSymbols cfs = cf.getDecimalFormatSymbols();
        _locale.putConvEntry(result, "decimal_point",
                dfs.getDecimalSeparator());
        _locale.putConvEntry(result, "thousands_sep",
                dfs.getGroupingSeparator());
        putConvUnicodeEntry(result, "currency_symbol", cfs.getCurrencySymbol(),
                dfs.getInternationalCurrencySymbol());
        _locale.putConvEntry(result, "int_curr_symbol",
                cfs.getInternationalCurrencySymbol());
        _locale.putConvEntry(result, "negative_sign", cfs.getMinusSign());
        // No positive sign concept in Java locale
        _locale.putConvEntry(result, "positive_sign", new PyString(""));
        _locale.putConvEntry(result, "p_sign_posn", new PyInteger(3));
        PyList groupingList = new PyList();
        groupingList.add(new PyInteger(df.getGroupingSize()));
        groupingList.add(new PyInteger(0));
        _locale.putConvEntry(result, "grouping", groupingList);
        _locale.putConvEntry(result, "mon_decimal_point",
                cfs.getMonetaryDecimalSeparator());
        _locale.putConvEntry(result, "mon_thousands_sep",
                cfs.getGroupingSeparator());
        _locale.putConvEntry(result, "frac_digits",
                new PyInteger(cf.getMaximumFractionDigits()));
        _locale.putConvEntry(result, "int_frac_digits",
                new PyInteger(cf.getMaximumFractionDigits()));
        PyList monGroupingList = new PyList();
        monGroupingList.add(new PyInteger(cf.getGroupingSize()));
        monGroupingList.add(new PyInteger(0));
        _locale.putConvEntry(result, "mon_grouping", monGroupingList);
        _locale.putConvEntry(result, "n_sign_posn",
                new PyInteger(_locale.negativeSignPosition(cf)));
        _locale.putConvEntry(result, "p_cs_precedes",
                new PyInteger(_locale.positiveCurrencyPrecedesValue(cf)));
        _locale.putConvEntry(result, "n_cs_precedes",
                new PyInteger(_locale.negativeCurrencyPrecedesValue(cf)));
        _locale.putConvEntry(result, "p_sep_by_space",
                new PyInteger(_locale.positiveSeparatedBySpace(cf)));
        _locale.putConvEntry(result, "n_sep_by_space",
                new PyInteger(_locale.negativeSeparatedBySpace(cf)));
        return result;
    }

    private void putConvUnicodeEntry(PyDictionary result, String key,
            String value, String fallback) {
        try {
            result.put(new PyString(key),
                    new PyString(new PyUnicode(value).encode(getEncoding())));
        } catch (PyException pye) {
            Py.writeComment("_locale", "Could not encode value for key " + key
                    + " " + pye.getMessage());
            result.put(new PyString(key), new PyString(fallback));
        }
    }

    public DecimalFormat getDecimalFormat() {
        return decimalFormat;
    }

    public DecimalFormat getCurrencyFormat() {
        return currencyFormat;
    }

    @Override
    public PyString getLocaleString() {
        return new PyString(locale.toString() + "." + encoding);
    }

    @Override
    public PyString getUnderlyingLocale() {
        return new PyString(locale.toString());
    }

    @Override
    public int strcoll(PyString str1, PyString str2) {
        int result = collator.compare(unicoder(str1), unicoder(str2));
        if (result > 0)
            return 1;
        if (result < 0)
            return -1;
        return 0;
    }

    private String unicoder(PyString str) {
        return strxfrm(str).toString();
    }

    @Override
    public PyString strxfrm(PyString str) {
        if (str instanceof PyUnicode) {
            return str;
        }
        return (PyString)str.decode(encoding);
    }

    public String getEncoding() {
        return encoding;
    }

    @Override
    public String[] getShortWeekdays() {
        return dfSymbols.getShortWeekdays();
    }

    @Override
    public String[] getWeekdays() {
        return dfSymbols.getWeekdays();
    }

    @Override
    public String[] getShortMonths() {
        return dfSymbols.getShortMonths();
    }

    @Override
    public String[] getMonths() {
        return dfSymbols.getMonths();
    }

    @Override
    public String[] getAmPmStrings() {
        return dfSymbols.getAmPmStrings();
    }

}


/**
 *
 * @Immutable
 */
class CEmulationLocale implements PyLocale {
    // A number of these structures are repeated from Time.java and elsewhere
    // They can be removed from those other classes and pointed here once
    // jython2_legacy behaviour is deprecated or removed.

    private static final String[] EN_SHORT_DAYS =
            new String[] {"", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"};

    private static final String[] EN_DAYS = new String[] {"", "Sunday",
            "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};

    private static final String[] EN_SHORT_MONTHS =
            new String[] {"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
                    "Aug", "Sep", "Oct", "Nov", "Dec"};

    private static final String[] EN_MONTHS = new String[] {"January",
            "February", "March", "April", "May", "June", "July", "August",
            "September", "October", "November", "December"};

    private static final String[] EN_AM_PM = new String[] {"am", "pm"};

    private static final PyDictionary EMULATION_CONV;

    private static void putEmpty(PyDictionary dict, String key) {
        dict.put(new PyString(key), Py.EmptyString);
    }

    private static void putCharMax(PyDictionary dict, String key) {
        dict.put(new PyString(key), _locale.CHAR_MAX_PY_INT);
    }

    static {
        EMULATION_CONV = new PyDictionary();
        // This is a repetition of the locale emulation in the locale module
        // to allow resetting the locale back to C emulation
        _locale.putConvEntry(EMULATION_CONV, "decimal_point", ".");
        putEmpty(EMULATION_CONV, "thousands_sep");
        putEmpty(EMULATION_CONV, "currency_symbol");
        putEmpty(EMULATION_CONV, "int_curr_symbol");
        putEmpty(EMULATION_CONV, "negative_sign");
        putEmpty(EMULATION_CONV, "positive_sign");
        putCharMax(EMULATION_CONV, "p_sign_posn");
        PyList groupingList = new PyList();
        groupingList.add(_locale.CHAR_MAX_PY_INT);
        _locale.putConvEntry(EMULATION_CONV, "grouping", groupingList);
        putEmpty(EMULATION_CONV, "mon_decimal_point");
        putEmpty(EMULATION_CONV, "mon_thousands_sep");
        putCharMax(EMULATION_CONV, "frac_digits");
        putCharMax(EMULATION_CONV, "int_frac_digits");
        _locale.putConvEntry(EMULATION_CONV, "mon_grouping", groupingList);
        putCharMax(EMULATION_CONV, "n_sign_posn");
        putCharMax(EMULATION_CONV, "p_cs_precedes");
        putCharMax(EMULATION_CONV, "n_cs_precedes");
        putCharMax(EMULATION_CONV, "p_sep_by_space");
        putCharMax(EMULATION_CONV, "n_sep_by_space");
    }

    @Override
    public PyDictionary localeconv() {
        return EMULATION_CONV;
    }

    @Override
    public PyString getLocaleString() {
        return _locale.C_LOCALE_PY_STRING;
    }

    @Override
    public PyString getUnderlyingLocale() {
        return _locale.C_LOCALE_PY_STRING;
    }

    @Override
    public int strcoll(PyString str1, PyString str2) {
        return str1.__cmp__(str2);
    }

    @Override
    public PyString strxfrm(PyString str1) {
        return str1;
    }

    @Override
    public String[] getShortWeekdays() {
        return EN_SHORT_DAYS;
    }

    @Override
    public String[] getWeekdays() {
        return EN_DAYS;
    }

    @Override
    public String[] getShortMonths() {
        return EN_SHORT_MONTHS;
    }

    @Override
    public String[] getMonths() {
        return EN_MONTHS;
    }

    @Override
    public String[] getAmPmStrings() {
        return EN_AM_PM;
    }

}
