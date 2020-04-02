import unittest
from test.test_support import run_unittest

class Foo(object): pass

class MethodExceptionTestCase(unittest.TestCase):
    
    #############################
    ### Test for class methods###
    #############################

    def test_eq_classe_typeerror(self):
        try:
            Foo.__eq__(1,2)
        except TypeError as e:
            self.assertEqual(str(e),"__eq__() takes exactly one argument (2 given)")
            
    def test_ne_classe_typeerror(self):
        try:
            Foo.__ne__(1,2)
        except TypeError as e:
            self.assertEqual(str(e),"__ne__() takes exactly one argument (2 given)")
            
    def test_le_classe_typeerror(self):
        try:
            
            Foo.__le__(1,2)
        except TypeError as e:
            self.assertEqual(str(e),"__le__() takes exactly one argument (2 given)")

    def test_lt_classe_typeerror(self):
        try:
            
            Foo.__lt__(1,2)
        except TypeError as e:
            self.assertEqual(str(e),"__lt__() takes exactly one argument (2 given)")

    def test_ge_classe_typeerror(self):
        try:
            
            Foo.__ge__(1,2)
        except TypeError as e:
            self.assertEqual(str(e),"__ge__() takes exactly one argument (2 given)")
            
    def test_gt_classe_typeerror(self):
        try:
            
            Foo.__gt__(1,2)
        except TypeError as e:
            self.assertEqual(str(e),"__gt__() takes exactly one argument (2 given)")

    def test_subclasses_classe_typeerror(self):
        try:
            
            Foo.__subclasses__(1)
        except TypeError as e:
            self.assertEqual(str(e),"__subclasses__() takes no arguments (1 given)")

    def test_subclassescheck_classe_typeerror(self):
        try:
            
            Foo.__subclasscheck__(1,2)
        except TypeError as e:
            self.assertEqual(str(e),"__subclasscheck__() takes exactly one argument (2 given)")
            
    def test_instancecheck_classe_typeerror(self):
        try:
            
            Foo.__instancecheck__(1,2)
        except TypeError as e:
            self.assertEqual(str(e),"__instancecheck__() takes exactly one argument (2 given)")

    def test_mro_classe_typeerror(self):
        try:
            
            Foo.mro(1,2)
        except TypeError as e:
            self.assertEqual(str(e),"mro() takes at most 1 arguments (2 given)")

    #############################
    ### Test for dict methods ###
    #############################
            
    def test_fromkeys_dict_typeerror(self):
        try:
            dict().fromkeys(1,2,3)
        except TypeError as e:
            self.assertEqual(str(e),"fromkeys() takes 1-2 arguments (3 given)")

    def test_len_dict_typeerror(self):
        try:
            dict().__len__(1)
        except TypeError as e:
            self.assertEqual(str(e),"__len__() takes no arguments (1 given)")

    def test_getitem_dict_typeerror(self):
        try:
            dict().__getitem__(1,2)
        except TypeError as e:
            self.assertEqual(str(e),"__getitem__() takes exactly one argument (2 given)")

    def test_iter_dict_typeerror(self):
        try:
            dict().__iter__(1)
        except TypeError as e:
            self.assertEqual(str(e),"__iter__() takes no arguments (1 given)")

    def test_setitem_dict_typeerror(self):
        try:
            dict().__setitem__(1,2,3)
        except TypeError as e:
            self.assertEqual(str(e),"__setitem__() takes 2 arguments (3 given)")

    def test_delitem_dict_typeerror(self):
        try:
            dict().__delitem__(1,2)
        except TypeError as e:
            self.assertEqual(str(e),"__delitem__() takes exactly one argument (2 given)")

    def test_clear_dict_typeerror(self):
        try:
            dict().clear(1)
        except TypeError as e:
            self.assertEqual(str(e),"clear() takes no arguments (1 given)")

    def test_pop_dict_typeerror(self):
        try:
            dict().pop(1,2,3)
        except TypeError as e:
            self.assertEqual(str(e),"pop() takes 1-2 arguments (3 given)")
            
    def test_contains_dict_typeerror(self):
        try:
            dict().__contains__(1,2)
        except TypeError as e:
            self.assertEqual(str(e),"__contains__() takes exactly one argument (2 given)")
            
    def test_str_dict_typeerror(self):
        try:
            dict().__str__(1)
        except TypeError as e:
            self.assertEqual(str(e),"__str__() takes no arguments (1 given)")
            
    def test_get_dict_typeerror(self):
        try:
            dict().get(1,2,3)
        except TypeError as e:
            self.assertEqual(str(e),"get() takes 1-2 arguments (3 given)")
            
    #############################
    ### Test for str methods  ###
    #############################

    def test_upper_str_typeerror(self):
        try:
            str().upper(1)
        except TypeError as e:
            self.assertEqual(str(e),"upper() takes no arguments (1 given)")

    def test_lower_str_typeerror(self):
        try:
            str().lower(1)
        except TypeError as e:
            self.assertEqual(str(e),"lower() takes no arguments (1 given)")

    def test_split_str_typeerror(self):
        try:
            str().split(1,2,3)
        except TypeError as e:
            self.assertEqual(str(e),"split() takes at most 2 arguments (3 given)")

    def test_startswith_str_typeerror(self):
        try:
            str().startswith(1,2,3,4)
        except TypeError as e:
            self.assertEqual(str(e),"startswith() takes 1-3 arguments (4 given)")

    def test_index_str_typeerror(self):
        try:
            str().index(1,2,3,4)
        except TypeError as e:
            self.assertEqual(str(e),"index() takes 1-3 arguments (4 given)")

    def test_formatter_parser_str_typeerror(self):
        try:
            str()._formatter_parser(1)
        except TypeError as e:
            self.assertEqual(str(e),"_formatter_parser() takes no arguments (1 given)")

    #############################
    ### Test for list methods ###
    #############################

    def test_append_list_typeerror(self):
        try:
            list().append(1,2)
        except TypeError as e:
            self.assertEqual(str(e),"append() takes exactly one argument (2 given)")

    def test_extend_list_typeerror(self):
        try:
            list().extend(1,2)
        except TypeError as e:
            self.assertEqual(str(e),"extend() takes exactly one argument (2 given)")

    def test_eq_list_typeerror(self):
        try:
            list().__eq__(1,2)
        except TypeError as e:
            self.assertEqual(str(e),"__eq__() takes exactly one argument (2 given)")

    def test_ne_list_typeerror(self):
        try:
            list().__ne__(1,2)
        except TypeError as e:
            self.assertEqual(str(e),"__ne__() takes exactly one argument (2 given)")
            
    def test_delitem_list_typeerror(self):
        try:
            list().__delitem__(1,2)
        except TypeError as e:
            self.assertEqual(str(e),"__delitem__() takes exactly one argument (2 given)")

    def test_pop_list_typeerror(self):
        try:
            list().pop(1,2)
        except TypeError as e:
            self.assertEqual(str(e),"pop() takes at most 1 arguments (2 given)")

    #############################
    ### Test for set methods  ###
    #############################

    def test_symmetric_difference_set_typeerror(self):
        try:
            set().symmetric_difference(1,2)
        except TypeError as e:
            self.assertEqual(str(e),"symmetric_difference() takes exactly one argument (2 given)")

    def test_len_set_typeerror(self):
        try:
            set().__len__(1)
        except TypeError as e:
            self.assertEqual(str(e),"__len__() takes no arguments (1 given)")

    def test_ge_set_typeerror(self):
        try:
            set().__ge__(1,2)
        except TypeError as e:
            self.assertEqual(str(e),"__ge__() takes exactly one argument (2 given)")

    def test_contains_set_typeerror(self):
        try:
            set().__contains__(1,2)
        except TypeError as e:
            self.assertEqual(str(e),"__contains__() takes exactly one argument (2 given)")

    def test_isdisjoint_set_typeerror(self):
        try:
            set().isdisjoint(1,2)
        except TypeError as e:
            self.assertEqual(str(e),"isdisjoint() takes exactly one argument (2 given)")
    
    
def test_main():
    run_unittest(MethodExceptionTestCase)

if __name__ == '__main__':
    test_main()
