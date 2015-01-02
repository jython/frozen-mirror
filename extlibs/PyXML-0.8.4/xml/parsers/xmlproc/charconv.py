# Some experiments in adding character encoding conversions to xmlproc.
# This module is not yet used by the released xmlproc, since I'm awaiting
# a reorganization.
#
# $Id: charconv.py,v 1.7 2001/12/30 12:09:14 loewis Exp $

import string

# --- Conversion tables

# CP 850 to ISO 8859-1

# First element is no. 128, second 129 ...
# The non-ISO characters, such as <empty set>, are mapped to non-ISO chars
# 127-145 and 147-159 in the order they appear in CP 850. Since there are
# more non-ISO chars than there is room for in these intervals, some of
# the last chars are also mapped to 159.

cp850_iso=[199,252,233,226,228,224,229,231,234,235,232,239,238,236,196,197,
           201,230,198,244,246,242,251,249,255,246,220,248,163,127,215,128,
           225,237,243,250,241,209,170,186,191,174,172,189,188,161,171,187,
           129,130,131,132,133,193,194,192,169,134,135,136,137,162,165,138,
           139,140,141,142,143,144,227,195,145,147,148,149,150,151,152,164,
           240,208,202,203,200,153,205,206,207,154,155,156,157,166,204,158,
           211,223,212,210,245,213,181,222,254,218,219,217,253,221,175,180,
           173,177,159,190,182,167,247,184,176,168,159,185,179,178,159,160]

cp850_iso_tbl=""
for ix in range(128):
    cp850_iso_tbl=cp850_iso_tbl+chr(ix)
for chno in cp850_iso:
    cp850_iso_tbl=cp850_iso_tbl+chr(chno)

# ISO 8859-1 to CP 850

iso_cp850=[0]*256
for ix in range(256):
    iso_cp850[ord(cp850_iso_tbl[ix])]=ix

iso_cp850_tbl=""
for chno in iso_cp850:
    iso_cp850_tbl=iso_cp850_tbl+chr(chno)

# Windows CP 1252 to ISO 8859-1
# Maps characters 128-159, 63 means non-mappable, 127 means unused in 1252
# Does a fuzzy transform (ndash and mdash both mapped to -, and so on)

cp1252_iso=[127,127,44,63,63,95,63,63,94,63,63,60,198,127,127,127,127,39,39,
            34,34,183,45,45,126,63,63,62,230,127,127,127]

cp1252_iso_tbl=""
for char in map(chr,range(128)+cp1252_iso+range(160,256)):
    cp1252_iso_tbl=cp1252_iso_tbl+char

# --- Conversion functions

def utf8_to_iso8859(data):
    out=""

    ix=0
    for ix in range(len(data)):
        chn=ord(data[ix])
        if chn & 224==192: # 110xxxxx
            out=out+chr( ((chn & 3) << 6) + (ord(data[ix+1]) & 63))
        elif chn & 128==0: # 0xxxxxxx
            out=out+data[ix]

    return out

def iso8859_to_utf8(data):
    out=""

    for ch in data:
        if ord(ch)<128:
            out=out+ch
        else:
            chno=ord(ch)
            out=out+chr(192+((chno & 192)>>6))+chr(128+(chno & 63))

    return out

def cp850_to_iso8859(data):
    return string.translate(data,cp850_iso_tbl)

def iso8859_to_cp850(data):
    return string.translate(data,iso_cp850_tbl)

def id_conv(data):
    return data

def cp850_to_utf8(data):
    return iso8859_to_utf8(cp850_to_iso8859(data))

def utf8_to_cp850(data):
    return iso8859_to_cp850(utf8_to_iso8859(data))

def cp1252_to_iso8859(data):
    return string.translate(data,cp1252_iso_tbl)

# --- Conversion function database

class ConverterDatabase:
    """This class knows about all registered converting functions, and can be
    queried for information about converters."""

    def __init__(self):
        self.__map={}
        self.__alias_map={}

    def add_alias(self,canonical,alias):
        "Adds an alias for a character set."
        self.__alias_map[string.lower(alias)]=string.lower(canonical)

    def can_convert(self,from_encoding,to_encoding):
        """Returns true if converters to from from_encoding to to_encoding are
        known. Encoding names follow the syntax specified by the XML rec."""
        from_encoding=self._canonize_name(from_encoding)
        to_encoding=self._canonize_name(to_encoding)

        if from_encoding==to_encoding:
            return 1

        try:
            return self.__map[from_encoding].has_key(to_encoding)
        except KeyError:
            return 0

    def get_converter(self,from_encoding,to_encoding):
        """Returns a converter function that converts from the character
        encoding from_encoding to to_encoding. A KeyError will be thrown
        if no converter is known."""
        from_encoding=self._canonize_name(from_encoding)
        to_encoding=self._canonize_name(to_encoding)

        if from_encoding==to_encoding:
            return id_conv
        else:
            return self.__map[from_encoding][to_encoding]

    def add_converter(self,from_encoding,to_encoding,converter):
        from_encoding=self._canonize_name(from_encoding)
        to_encoding=self._canonize_name(to_encoding)

        if not self.__map.has_key(from_encoding):
            self.__map[from_encoding]={}

        self.__map[from_encoding][to_encoding]=converter

    def _canonize_name(self,name):
        "Returns the canonical form of a charset name."
        name=string.lower(name)
        if self.__alias_map.has_key(name):
            return self.__alias_map[name]
        else:
            return name

# --- Globals

convdb=ConverterDatabase()
convdb.add_alias("US-ASCII","ANSI_X3.4-1968")
convdb.add_alias("US-ASCII","iso-ir-6")
convdb.add_alias("US-ASCII","ANSI_X3.4-1986")
convdb.add_alias("US-ASCII","ISO_646.irv:1991")
convdb.add_alias("US-ASCII","ASCII")
convdb.add_alias("US-ASCII","ISO646-US")
convdb.add_alias("US-ASCII","us")
convdb.add_alias("US-ASCII","IBM367")
convdb.add_alias("US-ASCII","cp367")
convdb.add_alias("US-ASCII","csASCII")

convdb.add_alias("ISO-8859-1","ISO_8859-1:1987")
convdb.add_alias("ISO-8859-1","iso-ir-100")
convdb.add_alias("ISO-8859-1","ISO_8859-1")
convdb.add_alias("ISO-8859-1","latin1")
convdb.add_alias("ISO-8859-1","l1")
convdb.add_alias("ISO-8859-1","IBM819")
convdb.add_alias("ISO-8859-1","CP819")
convdb.add_alias("ISO-8859-1","csISOLatin1")

convdb.add_alias("IBM850","cp850")
convdb.add_alias("IBM850","850")
convdb.add_alias("IBM850","csPC850Multilingual")

# converters (foo -> foo case not needed, handled automatically)

convdb.add_converter("IBM850","ISO-8859-1",cp850_to_iso8859)
convdb.add_converter("US-ASCII","ISO-8859-1",id_conv)
convdb.add_converter("windows-1252","ISO-8859-1",cp1252_to_iso8859)

convdb.add_converter("ISO-8859-1","IBM850",iso8859_to_cp850)
convdb.add_converter("US-ASCII","IBM850",id_conv)

convdb.add_converter("ISO-8859-1","WINDOWS-1252",id_conv)

convdb.add_converter("US-ASCII","UTF-8",id_conv)

# these are slow, so you should use Python 2.x

convdb.add_converter("UTF-8","ISO-8859-1",utf8_to_iso8859)
convdb.add_converter("ISO-8859-1","UTF-8",iso8859_to_utf8)
convdb.add_converter("UTF-8","IBM850",utf8_to_cp850)
convdb.add_converter("IBM850","UTF-8",cp850_to_utf8)
