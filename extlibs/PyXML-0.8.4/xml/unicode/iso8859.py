"""This module adds a backwards-compatibility to the older wstring module.
It is intended for use by 4Suite only; do not use it in your own code."""

import string
import utf8_iso

_trans = string.maketrans("_:","- ")
def _normalize(codeset):
    codeset = string.lower(codeset)
    codeset = string.translate(codeset, _trans)
    return codeset

class _Wstringmod:
    "Emulator for old wstring module"
    def __init__(self):
        self.aliases = {'iso-ir-100' : 'iso-8859-1',
                        'cp819' : 'iso-8859-1',
                        'l1' : 'iso-8859-1',
                        'latin1' : 'iso-8859-1',
                        'ibm819' : 'iso-8859-1',
                        }
        self.encodings = {'utf-8' : 0}
        for i in range(1, len(utf8_iso.code_to_uni)):
            if utf8_iso.code_to_uni[i]:
                self.encodings['iso-8859-%d' % i] = i

    def install_alias(self, newname, oldname):
        self.aliases[_normalize(newname)] = _normalize(oldname)

    def from_utf8(self, utf8):
        return UTF8String(utf8)

    def decode(self, encoding, string):
        return UTF8String(string, encoding)

    def chr(self, ch):
        return UTF8String(utf8_iso.utf8chr(ch))

wstring = _Wstringmod()

class UTF8String:
    "Emulator for the wstring type"
    def __init__(self, string, encoding='utf-8'):
        self.data = string
        enc = _normalize(encoding)
        codeset = wstring.encodings.get(enc)
        if codeset is None:
            if wstring.aliases.has_key(enc):
                codeset = wstring.encoding.get(wstring.aliases[enc])
            if codeset is None:
                raise utf8_iso.ConvertError('Unknown encoding: %s' % encoding)
        self.codeset = codeset

    def utf8(self):
        if self.codeset == 0:
            return self.data
        output = map(lambda char, codeset=self.codeset:
                     utf8_iso.code_to_utf8(codeset, char),
                     self.data)
        return string.join(output, '')

    def encode(self, encoding):
        enc = _normalize(encoding)
        codeset = wstring.encodings.get(enc)
        if codeset is None:
            if wstring.aliases.has_key(enc):
                codeset = wstring.encoding.get(wstring.aliases[enc])
            if codeset is None:
                raise utf8_iso.ConvertError('Unknown encoding: %s' % encoding)

        if codeset == 0:
            return self.data

        input = self.data
        output = []
        while input:
            for i in range(len(input)):
                if ord(input[i])>128:
                    break
            if i == 0:
                char, input = utf8_iso.utf8_to_code(codeset, input)
                output.append(char)
            else:
                output.extend(list(input[:i]))
                input = input[i:]
        return string.join(output, '')
