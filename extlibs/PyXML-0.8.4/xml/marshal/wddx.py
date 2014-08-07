from generic import *

"""WDDX marshalling"""

# WDDX marshalling can be either "strict", in which Python objects
# with no good WDDX equivalent cause a marshalling exception, or
# "loose", in which WDDX takes extra steps to prevent marshalling
# exception by finding the closest match for a Python object.
#
# If the module variable STRICT is true, any marshalling instances
# created will use strict marshalling rules. If STRICT is false,
# any marshalling instances created will use loose rules.
# Changing the value of STRICT affects any marshallers
# subsequently created; previously created marshaller objects
# will not change their behavior.
#
# By default, STRICT is false. This default setting allows WDDX
# the most flexible behavior for naive users of the module.
#
# In the current implementation of "loose" marshalling, there are
# very few differences with loose marshalling:
#
# 1) the None object becomes an empty <string> element,
#    which is unmarshalled as the empty string "".
#
# 2) Tuples become <array> elements, which are unmarshalled
#    as lists.
#
# 3) Instances which have a __wddx__ method will have the
#    result of calling that method used as the marshalling
#    value. (See _WDDX_METHOD below.)

STRICT = 0

# Added _WDDX_METHOD, which names a special method for WDDX
# marshalling. If an instance to be marshalled has this method
# defined, it is called with no arguments and the return value is used
# for marshalling. (The marshaller code in m_instance forbids
# the return value to be an instance with its own special
# WDDX method, to prevent recursive death.)
#
# This method is useful for user-defined classes whose instances
# mimic the behavior of built-in types such as dictionaries or
# lists.
#
# This special method is used only if STRICT is false.

_WDDX_METHOD = '__wddx__'

# WDDX has a Boolean type.  We need to generate such variables, so
# this defines a class representing a truth value, and then creates
# TRUE and FALSE.

class TruthValue:
    def __init__(self, value):
        if value:
            self.__dict__['value'] = 1
        else:
            self.__dict__['value'] = 0

    def __setattr__(self, item, value):
        raise TypeError, "TruthValue object is read-only"

    def __nonzero__(self): return self.value
    def __cmp__(self, other): return cmp(self.value, other)
    def __hash__(self): return hash(self.value)

    def __repr__(self):
        if self.value:
            return "<TruthValue instance: True>"
        else:
            return "<TruthValue instance: False>"

TRUE = TruthValue(1)
FALSE = TruthValue(0)

RECORDSET = {}
import UserDict
class RecordSet(UserDict.UserDict):
    def __init__(self, fields, *lists):
        UserDict.UserDict.__init__(self)
        if len(fields) != len(lists):
            raise ValueError, "Number of fields and lists must be the same"
        for L in lists[1:]:
            if len(L) != len(lists[0]):
                raise ValueError, "Number of entries in each list must be the same"
        self.fields = fields
        for i in range(len(fields)):
            f = fields[i]
            self.data[f] = lists[i]

class WDDXMarshaller(Marshaller):
    DTD = '<!DOCTYPE wddxPacket SYSTEM "wddx_0090.dtd">'
    tag_root = 'wddxPacket'
    tag_float = tag_int = tag_long = 'number'
    tag_instance = 'boolean'
    wddx_version = "0.9"

    m_reference = m_complex = m_code = Marshaller.m_unimplemented

    def __init__(self, strict=None):
        if strict is None:
            self._strict = STRICT
        else:
            self._strict = strict

    def m_root(self, value, dict):
        L = ['<%s version="%s">' % (self.tag_root, self.wddx_version)]
        # add header
        L.append('<header/><data>')
        L = L + self._marshal(value, dict)
        L.append('</data></%s>' % self.tag_root)
        return L

    def m_instance(self, value, dict):
        if isinstance(value, RecordSet):
            return self.m_recordset(value, dict)

        # allow any TruthValue instance, not just
        # the predefined helpful "constants"; else
        # why make the class?
        if isinstance(value, TruthValue):
            if value:
                return ['<boolean value="true"/>']
            else:
                return ['<boolean value="false"/>']

        # check for _WDDX_METHOD method, but prevent
        # recursive death if return value also has wddx method
        if not self._strict and hasattr(value, _WDDX_METHOD):
            newval = getattr(value, _WDDX_METHOD)()
            # newval may not have its own wddx method
            if hasattr(newval, _WDDX_METHOD):
                raise ValueError, \
                      "%s method of object %s may not " \
                      "return object having own %s method" % \
                      (_WDDX_METHOD, repr(value), _WDDX_METHOD)
            return self._marshal(newval, dict)

        self.m_unimplemented(value, dict)

    def m_recordset(self, value, dict):
        L = ['<recordset rowCount="%i" fieldNames="%s">' %
             (len(value), string.join(value.fields, ','))]
        for f in value.fields:
            recs = value[f]
            L.append('<field name="%s">' % f)
            for r in recs:
                L = L + self._marshal(r, dict)
            L.append('</field>')

        L.append('</recordset>')
        return L

    def m_list(self, value, dict):
        L = []
        i = str(id(value))
        dict[i] = 1
        L.append('<array length="%i">' % len(value))
        for elem in value:
            L = L + self._marshal(elem, dict)
        L.append('</array>')
        return L

    def m_tuple(self, value, dict):
        if self._strict:
            return self.m_unimplemented(value, dict)
        else:
            return self.m_list(value, dict)

    def m_None(self, value, dict):
        if self._strict:
            return self.m_unimplemented(value, dict)
        else:
            return self.m_string("", dict)

    def m_dictionary(self, value, dict):
        L = []
        i = str(id(value))
        dict[i] = 1
        L.append('<struct>')
        items = value.items()
        # Sort the items so the order they're written in is
        # deterministic; this is only needed to make testing easier.
        items.sort()
        for key, v in items:
            L.append('<var name="%s">' % key)
            L = L + self._marshal(v, dict)
            L.append('</var>')
        L.append('</struct>')
        return L


class WDDXUnmarshaller(Unmarshaller):
    unmarshal_meth = {
        'wddxPacket': (None, None),
        'data': ('um_start_root', None),
        'header': (None, None),
        'char': ('um_start_char', None),
        'boolean': ('um_start_boolean', 'um_end_boolean'),
        'number': ('um_start_number', 'um_end_number'),
        'string': ('um_start_string', 'um_end_string'),
        'array': ('um_start_list', 'um_end_list'),
        'struct': ('um_start_dictionary', 'um_end_dictionary'),
        'var': ('um_start_var', None),
        'recordset': ('um_start_recordset', 'um_end_recordset'),
        'field': ('um_start_field', 'um_end_field'),
        }

    def um_start_char(self, name, attrs):
        self.data_stack[-1].append(str(chr(string.atoi(attrs['code'], 16))))

    def um_start_boolean(self, name, attrs):
        v = attrs['value']
        self.data_stack.append([v])

    def um_end_boolean(self, name):
        ds = self.data_stack
        if ds[-1][0] == 'true':
            ds[-1] = TRUE
        else:
            ds[-1] = FALSE

    um_start_number = Unmarshaller.um_start_generic
    um_end_number = Unmarshaller.um_end_float

    def um_start_var(self, name, attrs):
        name = attrs['name']
        self.data_stack.append(name)

    def um_start_recordset(self, name, attrs):
        fields = string.split(attrs['fieldNames'], ',')
        rowCount = int(attrs['rowCount'])
        self.data_stack.append(RECORDSET)
        self.data_stack.append((rowCount, fields))

    def um_end_recordset(self, name):
        ds = self.data_stack
        for index in range(len(ds) - 1, -1, -1):
            if ds[index] is RECORDSET:
                break
        assert index!=-1
        rowCount, fields = ds[index + 1]
        lists = [None] * len(fields)
        for i in range(index+2, len(ds), 2):
            field = ds[i]
            value = ds[i + 1]
            pos = fields.index(field)
            lists[pos] = value
        ds[index:] = [apply(RecordSet, tuple([fields]+lists))]

    def um_start_field(self, name, attrs):
        field = attrs['name']
        self.data_stack.append(field)
        self.data_stack.append(LIST)
        self.data_stack.append([])
    um_end_field = Unmarshaller.um_end_list

def dump(value, file, strict=None):
    m = WDDXMarshaller(strict)
    return m.dump(value, file)

def dumps(value, strict=None):
    m = WDDXMarshaller(strict)
    return m.dumps(value)

def load(file):
    return WDDXUnmarshaller().load(file)

def loads(string):
    return WDDXUnmarshaller().loads(string)

def runtests():
    print "Testing WDDX marshalling..."
    recordset = RecordSet(['NAME', 'AGE'],
                          ['John Doe', 'Jane Doe'],
                          [34, 31])

    class Custom:
        def __init__(self, value): self.value = value
        def __wddx__(self): return self.value
        def __repr__(self): return repr(self.value)

    global STRICT
    STRICT = 1

    test(load, loads, dump, dumps,
         [TRUE, FALSE, 1, pow(2,123L), 19.72,
          "here is a string & a <fake tag>",
          [1,2,3,"foo"], recordset,
          {'lowerBound': 18, 'upperBound': 139,
           'eggs': ['rhode island red', 'bantam']},
          {'s': 'a string',
           'obj': {'s': 'a string', 'n': -12.456},
           'n': -12.456, 'b': TRUE, 'a': [10,'second element'],
           }
          ])

    STRICT = 0
    test(load, loads, dump, dumps,
         [(1, 3, "five", 7, None, Custom(42)),], do_assert=0)

if __name__ == '__main__':
    runtests()
