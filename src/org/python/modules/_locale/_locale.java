package org.python.modules._locale;

import java.nio.charset.Charset;
import java.text.Collator;
import java.text.DateFormatSymbols;
import java.text.DecimalFormat;
import java.text.DecimalFormatSymbols;
import java.text.NumberFormat;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Locale;

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
import org.python.core.PyTuple;
import org.python.core.PyUnicode;


public class _locale implements ClassDictInit {

    /**
     *
     * The locale module exposes _locale.Error as locale.Error. Some Python 
     * functions, including strptime(), depend on locale.Error.
     * 
     */
    public static class LocaleError extends PyException{
        public LocaleError(String message){
            super(Error,message);
        }
    }

    // TODO - this lets us throw errors from Java and catch them in Python
    // but not raise locale.Error in Python ... because it's a String, not
    // an Exception. It runs but is ugly
    public static PyObject Error = new PyString("locale.Error");
       
    public static PyException LocaleException(String message){
        return new LocaleError(message); 
    }

    public static final PyString __doc__ = new PyString(
        "This module exposes locale functions in the underlying operating\n"+
        "system or platform in a consistent way. It is used by the locale\n" + 
	"module. It is a parallel Java implementation to C libraries \n" + 
        "in CPython which in turn depend on C libraries provided by the OS."
    );


    public static final String PYTHON_LOCALE_CONTROL = "python.locale.control";

    public static final String LOCALE_CONTROL_SETTABLE  = "settable";
    public static final String LOCALE_CONTROL_JYTHON2_LEGACY = "jython2_legacy";



    // These values are the same as glibc locale/bits/locale.h
    // Specific integer constants are not mandated by the POSIX locale spec, so an 
    // existing standard seemed as good an arbitrary set of values as any
    private static final int __LC_CTYPE             = 0;
    private static final int __LC_NUMERIC           = 1;
    private static final int __LC_TIME              = 2;
    private static final int __LC_COLLATE           = 3;
    private static final int __LC_MONETARY          = 4;
    private static final int __LC_MESSAGES          = 5;
    private static final int __LC_ALL               = 6;
    private static final int __LC_PAPER             = 7;
    private static final int __LC_NAME              = 8;
    private static final int __LC_ADDRESS           = 9;
    private static final int __LC_TELEPHONE         = 10;
    private static final int __LC_MEASUREMENT	    = 11;
    private static final int __LC_IDENTIFICATION    = 12;

    public static final PyInteger LC_CTYPE     = new PyInteger(__LC_CTYPE);
    public static final PyInteger LC_NUMERIC   = new PyInteger(__LC_NUMERIC);
    public static final PyInteger LC_TIME      = new PyInteger(__LC_TIME);
    public static final PyInteger LC_COLLATE   = new PyInteger(__LC_COLLATE);
    public static final PyInteger LC_MONETARY  = new PyInteger(__LC_MONETARY);
    public static final PyInteger LC_MESSAGES  = new PyInteger(__LC_MESSAGES);
    public static final PyInteger LC_ALL       = new PyInteger(__LC_ALL);
    // Remaining constants not used by locale.py so are not exposed here

    // 127 chosen as consistent with hardcoded default in locale.py for C locale
    public static final int CHAR_MAX = 127; 
    public static final PyInteger CHAR_MAX_PY_INT = new PyInteger(127); 

    public static final PyString C_LOCALE_PY_STRING = new PyString("C");

    private static final List<Locale> AVAILABLE_LOCALE_LIST;

    private static PyLocale currentLocale = 
                            new JyLocale(Locale.getDefault(), 
			    		Charset.defaultCharset().name());
    private static volatile boolean settable = false;


    static{
        final List<Locale> list = 
		new ArrayList<>(Arrays.asList(Locale.getAvailableLocales()));  
	AVAILABLE_LOCALE_LIST = Collections.unmodifiableList(list);
    }


    public static void classDictInit(PyObject dict) {
        settable = false;
        dict.__setitem__("Error", Error);
        try{
	    currentLocale = new JyLocale(Locale.getDefault(), 
			    		Charset.defaultCharset().name());
	}catch(Throwable t){
            throw Py.ImportError("Jython failed to load default Java locale, falling back. " + t.getMessage() );
        }
        final String localeControl = PySystemState.registry.getProperty(
			PYTHON_LOCALE_CONTROL, "");
        if ("".equals(localeControl) 
            || LOCALE_CONTROL_JYTHON2_LEGACY.equals(localeControl) )
	{
            throw Py.ImportError("Jython locale support not enabled with python.locale.control, falling back" );
        }
        if (!LOCALE_CONTROL_SETTABLE.equals(localeControl) ){
            throw Py.ImportError("Jython locale support python.locale.control unrecognized value, falling back" );
        }
        settable = true;
    }

    public static boolean isSettable(){
        return settable;
    }

    protected static void putConvEntry(PyDictionary result, String key, 
		                     String value)
    {
        result.put( new PyString(key), new PyString(value) );
    }

    protected static void putConvEntry(PyDictionary result, String key, 
		                     char value)
    {
        result.put( new PyString(key), new PyString(value) );
    }

    protected static void putConvEntry(PyDictionary result, String key, 
		                     PyObject value)
    {
        result.put( new PyString(key), value );
    }

    public static PyDictionary localeconv(){
        return currentLocale.localeconv();
    }

    /**
     *
     * Compare Java (unicode) strings using the Java collator for the current
     * locale, and the encoding normalization provided by strxfrm. In the 'C'
     * locale, this simply calls str.__cmp__() 
     * 
     */
    public static int strcoll(PyString str1, PyString str2){
        return currentLocale.strcoll(str1,str2);
    }

    /**
     *
     * Normalize a string to unicode, for common comparison, using the locale
     * encoding.  In the 'C' locale, this is a no-op, returning the parameter.
     *
     */
    public static PyString strxfrm(PyString str1){
        return currentLocale.strxfrm(str1);
    }

    public static int negativeSignPosition(DecimalFormat df){
        String prefix = df.getNegativePrefix();
	String suffix = df.getNegativeSuffix();
        if ("".equals(suffix)){
            if ("".equals(prefix)){
		// Nothing is specified in this locale.
                return CHAR_MAX;
	    } 
	}
        if (prefix.startsWith("(") && suffix.endsWith(")")){
	    // Currency and value are surrounded by parentheses.
            return 0;
	} 
        final String MINUS =
                 String.valueOf( df.getDecimalFormatSymbols().
					        getMinusSign())  ;
	if ( prefix.startsWith(MINUS)) {
            // The sign should precede the value and currency symbol.
            return 1;
	}
	if ( prefix.endsWith(MINUS) ) {
            // The sign should immediately precede the value.
            return 3;
	}
	if ( suffix.startsWith(MINUS) ) {
            // 	The sign should immediately follow the value.
            return 4;
	}
        // The sign should follow the value and currency symbol.
	return 2;
    }

    public static int positiveCurrencyPrecedesValue(DecimalFormat df){
        return currencyPrecedesValue( df, df.getPositivePrefix() );
    }

    public static int negativeCurrencyPrecedesValue(DecimalFormat df){
        return currencyPrecedesValue( df, df.getNegativePrefix() );
    }

    private static int currencyPrecedesValue(DecimalFormat df, String prefix){
        if (prefix.contains( 
                df.getDecimalFormatSymbols().getCurrencySymbol() ))
	{
            return 1; 
	}	
	return 0;
    }


    public static int positiveSeparatedBySpace(DecimalFormat df){
        return separatedBySpace(df.getPositivePrefix(),df.getPositiveSuffix());
    }

    public static int negativeSeparatedBySpace(DecimalFormat df){
        return separatedBySpace(df.getNegativePrefix(),df.getNegativeSuffix());
    }

    public static int separatedBySpace(String prefix, String suffix){
        if ((!prefix.isEmpty() 
             && isExtendedWhitespace(prefix.charAt(prefix.length()-1)) ) 
            || 
	    (!suffix.isEmpty() 
             && isExtendedWhitespace(suffix.charAt(0) ) ) )
        {
            return 1;
	}
	return 0;
    }

    /**
     * Includes non-breaking space, but not extended codepoints
     */
    public static boolean isExtendedWhitespace(char c){
        return Character.isWhitespace(c) 
	       || '\u00A0' == c ;
    }


    public static PyString setlocale(PyInteger category){
	return currentLocale.getLocaleString();
    } 

    /**
     *
     * Sets the locale given a category and normalized locale string.
     * Normalized format is per RFC 1766, but using underscores instead of 
     * dashes, eg zh_CH.UTF-8. Briefly, the format is 
     * [language]_[locality].[encoding], where [language] is a two
     * character language identifer, locality is a regional indicator, and 
     * encoding is a character encoding. Other examples are en_AU.ISO8859-1
     * and de_DE.ISO8859-15. 
     *
     * If this is an empty locale, the same language tag will be tried with
     * dashes instead of underscores, ie [lanuage]-[locality].
     *
     * Normalization would usually be done by the enclosing locale module 
     * (no leading underscore).
     *
     * This function treats a missing encoding as using UTF-8.
     *
     */
    public static PyString setlocale(PyInteger category, PyString locale){
	Py.writeDebug("_locale","setlocale(category,locale==" + locale + ")");
	if (locale == null || locale.equals(Py.None) 
                || locale.equals(currentLocale.getLocaleString() ) )
        {
            return setlocale(category); 
	}
	if (!category.equals(LC_ALL)){ 
            // Py.NotImplementedError not used as dependencies exist on 
            // locale.Error
            throw LocaleException( 
                    "Only LC_ALL is supported in this version of Jython");
	}
	if (locale.equals(C_LOCALE_PY_STRING)){
            changeCurrentLocale( new CEmulationLocale() );
            return C_LOCALE_PY_STRING;
	}
	String localeStr = locale.toString();
	String[] localeParts = localeStr.split("\\.");
	String language; 
	String encoding = "UTF-8";
	if (localeParts.length >= 3 ){
            throw LocaleException(
                "Does not conform to [language]_[locality].[encoding] format: "
	       	+ locale.toString() );
	}
	if (localeParts.length == 1){
            language = localeStr;
	}else{
	    // == 2
            language = localeParts[0];
	    encoding = localeParts[1];
	}
        Locale newLocale = loadLocale(language);
        if (!isAvailableLocale(newLocale)){
            String underscoreAlias = language.replace('_','-');
	    newLocale = loadLocale(underscoreAlias);
            if (!isAvailableLocale(newLocale)){
                throw LocaleException("No locale found: " + locale.toString() );
            }
	}
	changeCurrentLocale(new JyLocale(newLocale,encoding) );
	return currentLocale.getLocaleString();
    } 

    private static boolean isAvailableLocale(Locale locale){
        return locale != null
		&& !locale.toString().isEmpty()
		&& AVAILABLE_LOCALE_LIST.contains(locale);
    }

    private static Locale loadLocale(String language){
        Locale newLocale = Locale.forLanguageTag(language);
        Py.writeDebug("_locale","Current: " 
			+ currentLocale.getUnderlyingLocale());
	Py.writeDebug("_locale","New: " + newLocale + " loaded with tag: " + language);
	return newLocale;
    }

    private static synchronized void changeCurrentLocale(PyLocale pyLocale){
        Py.writeDebug("_locale","Locale changed to: " 
			+ pyLocale.getLocaleString() ) ;
	currentLocale = pyLocale;
    }

    public static PyLocale getPyLocale(){
        return currentLocale;
    }

}



class JyLocale implements PyLocale{
    private Locale locale;
    private String encoding;
    private DecimalFormat decimalFormat;
    private DecimalFormat currencyFormat;
    private PyDictionary conv;
    private Collator collator;
    private DateFormatSymbols dfSymbols;

    public JyLocale(Locale locale, String encoding){
        resetLocale(locale,encoding);
    }

    public synchronized void resetLocale(Locale locale, String encoding){
        this.locale = locale;
	this.encoding = encoding;
	this.decimalFormat = (DecimalFormat)NumberFormat.getInstance(locale);
        this.decimalFormat = (DecimalFormat)NumberFormat.
					getCurrencyInstance(locale);
        this.conv = initLocaleConv();
        this.collator = Collator.getInstance(locale);
        this.dfSymbols = DateFormatSymbols.getInstance(locale);
    }

    @Override
    public PyDictionary localeconv(){
        return conv;
    }

    private PyDictionary initLocaleConv(){
        PyDictionary result = new PyDictionary();
        DecimalFormat df = getDecimalFormat();
	DecimalFormat cf = getCurrencyFormat();
        DecimalFormatSymbols dfs = df.getDecimalFormatSymbols();
        _locale.putConvEntry(result, "decimal_point", 
                                dfs.getDecimalSeparator() ) ;
        _locale.putConvEntry(result, "thousands_sep", 
                                dfs.getGroupingSeparator() ) ;
        putConvUnicodeEntry(result, "currency_symbol", 
			            dfs.getCurrencySymbol(),
				    dfs.getInternationalCurrencySymbol() ); 
        _locale.putConvEntry(result, "int_curr_symbol", 
			     dfs.getInternationalCurrencySymbol()); 
        _locale.putConvEntry(result, "negative_sign", dfs.getMinusSign()) ;
	// No positive sign concept in Java locale
        _locale.putConvEntry(result, "positive_sign", new PyString("") ) ;
	_locale.putConvEntry( result, "p_sign_posn", 
			new PyInteger(3) );
	PyList groupingList = new PyList();
	groupingList.add( new PyInteger( df.getGroupingSize() ) );
        groupingList.add( new PyInteger( 0 ) );
	_locale.putConvEntry( result, "grouping", groupingList );
        _locale.putConvEntry( result, "mon_decimal_point", 
			dfs.getMonetaryDecimalSeparator()) ;
        _locale.putConvEntry( result, "mon_thousands_sep", 
		      dfs.getGroupingSeparator() ) ;
        _locale.putConvEntry( result, "frac_digits", 
		new PyInteger( df.getMaximumFractionDigits() ) );
        _locale.putConvEntry( result, "int_frac_digits", 
		new PyInteger( df.getMaximumFractionDigits() ) );
        _locale.putConvEntry( result, "mon_grouping", groupingList );
	_locale.putConvEntry( result, "n_sign_posn", 
		new PyInteger(_locale.negativeSignPosition(cf) ) );
	_locale.putConvEntry( result, "p_cs_precedes",
		new PyInteger(_locale.positiveCurrencyPrecedesValue(cf)  )  );
	_locale.putConvEntry( result, "n_cs_precedes",
		new PyInteger(_locale.negativeCurrencyPrecedesValue(cf)  )  );
	_locale.putConvEntry( result, "p_sep_by_space",
		new PyInteger( _locale.positiveSeparatedBySpace(cf) )  );
	_locale.putConvEntry( result, "n_sep_by_space",
		new PyInteger( _locale.negativeSeparatedBySpace(cf) )  );
	return result;
    }

    private void putConvUnicodeEntry(PyDictionary result, String key, 
		                     String value, String fallback)
    {
        try{
            result.put( new PyString(key), 
			new PyString( 
				new PyUnicode(value).encode(getEncoding() ) 
				) );
	}catch( PyException pye ){
            Py.writeComment( "_locale", 
			    "Could not encode value for key " + key + " "
			  + pye.getMessage() );
            result.put( new PyString(key), 
			new PyString(fallback) );
	}
    }

    public DecimalFormat getDecimalFormat(){
	return decimalFormat;
    }

    public DecimalFormat getCurrencyFormat(){
	return decimalFormat;
    }

    @Override
    public PyString getLocaleString(){
        return new PyString(locale.toString() + "." + encoding);
    }

    @Override
    public PyString getUnderlyingLocale(){
        return new PyString(locale.toString());
    }

    @Override
    public int strcoll(PyString str1, PyString str2){
        int result = collator.compare( unicoder(str1), unicoder(str2) );
        if (result > 0)
            return 1;
        if (result < 0)
            return -1;
        return 0;
    }

    private String unicoder(PyString str){
        return strxfrm(str).toString();
    }

    @Override
    public PyString strxfrm(PyString str){
        if (str instanceof PyUnicode){
            return str;
        }
        return (PyString)str.decode(encoding);
    }

    public String getEncoding(){
        return encoding;
    }

    @Override
    public String[] getShortWeekdays(){
        return dfSymbols.getShortWeekdays();
    }

    @Override
    public String[] getWeekdays(){
        return dfSymbols.getWeekdays();
    }

    @Override
    public String[] getShortMonths(){
        return dfSymbols.getShortMonths();
    }

    @Override
    public String[] getMonths(){
        return dfSymbols.getMonths();
    }

    @Override
    public String[] getAmPmStrings(){
        return dfSymbols.getAmPmStrings();
    }


}



class CEmulationLocale implements PyLocale{

    private static final String[] EN_SHORT_DAYS = new String[] {"",
                    "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"};

    private static final String[] EN_DAYS = new String[] {
                   "", "Sunday", "Monday", "Tuesday", "Wednesday", 
                   "Thursday", "Friday", "Saturday"};

    private static final String[] EN_SHORT_MONTHS = new String[] {"Jan",
                   "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
                   "Oct", "Nov", "Dec"};

    private static final String[] EN_MONTHS = new String[] {"January",
                   "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", 
                   "December"};

    private static final String[] EN_AM_PM = new String[]{ "am", "pm" };


    private static final PyDictionary EMULATION_CONV;

    private static void putEmpty(PyDictionary dict, String key){
       dict.put( new PyString(key), Py.EmptyString ); 
    } 

    private static void putCharMax(PyDictionary dict, String key){
       dict.put( new PyString(key),  _locale.CHAR_MAX_PY_INT ); 
    } 

    static{
        EMULATION_CONV = new PyDictionary();
        // This is a repetition of the locale emulation in the locale module
        // to allow resetting the locale back to C emulation
        _locale.putConvEntry(EMULATION_CONV, "decimal_point", "." ) ;
        putEmpty(EMULATION_CONV, "thousands_sep" );
        putEmpty(EMULATION_CONV, "currency_symbol" ); 
        putEmpty(EMULATION_CONV, "int_curr_symbol" );
        putEmpty(EMULATION_CONV, "negative_sign" );
        putEmpty(EMULATION_CONV, "positive_sign" );
        putCharMax(EMULATION_CONV, "p_sign_posn" );
	PyList groupingList = new PyList();
        groupingList.add( _locale.CHAR_MAX_PY_INT );
	_locale.putConvEntry( EMULATION_CONV, "grouping", groupingList );
        putEmpty( EMULATION_CONV, "mon_decimal_point" );
        putEmpty( EMULATION_CONV, "mon_thousands_sep" );
        putCharMax( EMULATION_CONV, "frac_digits" );
        putCharMax( EMULATION_CONV, "int_frac_digits" );
        _locale.putConvEntry( EMULATION_CONV, "mon_grouping", groupingList );
        putCharMax(EMULATION_CONV, "n_sign_posn" );
        putCharMax(EMULATION_CONV, "p_cs_precedes" );
        putCharMax(EMULATION_CONV, "n_cs_precedes" );
        putCharMax(EMULATION_CONV, "p_sep_by_space" );
        putCharMax(EMULATION_CONV, "n_sep_by_space" );
    }

    @Override
    public PyDictionary localeconv(){
        return EMULATION_CONV;
    }

    @Override
    public PyString getLocaleString(){
        return _locale.C_LOCALE_PY_STRING;
    }

    @Override
    public PyString getUnderlyingLocale(){
        return _locale.C_LOCALE_PY_STRING;
    }

    @Override
    public int strcoll(PyString str1, PyString str2){
        return str1.__cmp__(str2);
    }

    @Override
    public PyString strxfrm(PyString str1){
        return str1;
    }

    @Override
    public String[] getShortWeekdays(){
        return EN_SHORT_DAYS;
    }

    @Override
    public String[] getWeekdays(){
        return EN_DAYS;
    }

    @Override
    public String[] getShortMonths(){
        return EN_SHORT_MONTHS;
    }

    @Override
    public String[] getMonths(){
        return EN_MONTHS;
    }

    @Override
    public String[] getAmPmStrings(){
        return EN_AM_PM;
    }


}

