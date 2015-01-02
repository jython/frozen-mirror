########################################################################
#
# File Name:   ParsedExpr.py
#
#
"""
The implementation of all of the expression pared tokens.
WWW: http://4suite.org/XPATH        e-mail: support@4suite.org

Copyright (c) 2000-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""

import string, UserList, types

from xml.dom import EMPTY_NAMESPACE
from xml.dom.ext import SplitQName
from xml.xpath import CompiletimeException, RuntimeException
from xml.xpath import g_extFunctions
from xml.xpath import ParsedNodeTest
from xml.xpath import CoreFunctions, Conversions
from xml.xpath import Util
from xml.xpath import ParsedStep
from xml.xpath import ParsedAxisSpecifier
from xml.utils import boolean
import Set

class NodeSet(UserList.UserList):
    def __init__(self, data=None):
        UserList.UserList.__init__(self, data or [])

    def __repr__(self):
        st = '<NodeSet at %x: [' % id(self)
        if len(self):
            for i in self[:-1]:
                st = st + repr(i) + ', '
            st = st + repr(self[-1])
        st = st + ']>'
        return st


class ParsedLiteralExpr:
    def __init__(self,literal):
        if len(literal) >= 2 and (
            literal[0] in ['\'', '"'] and
            literal[0] == literal[-1]):
            literal = string.strip(literal)[1:-1]
        self._literal = literal

    def evaluate(self, context):
        return self._literal

    def pprint(self, indent=''):
        print indent + str(self)

    def __str__(self):
        return '<Literal at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        return '"' + self._literal + '"'


class ParsedNLiteralExpr(ParsedLiteralExpr):
    def __init__(self,nliteral):
        ParsedLiteralExpr.__init__(self,"")
        self._nliteral = nliteral
        self._literal = float(nliteral)

    def pprint(self, indent=''):
        print indent + str(self)

    def __str__(self):
        return '<Number at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        return str(self._nliteral)

class ParsedVariableReferenceExpr:
    def __init__(self,name):
        self._name = name
        self._key = SplitQName(name[1:])
        return

    def evaluate(self, context):
        """Returns a string"""
        (prefix, local) = self._key
        uri = context.processorNss.get(prefix)
        if prefix and not uri:
            raise RuntimeException(RuntimeException.UNDEFINED_PREFIX, prefix)
        expanded = (prefix and uri or EMPTY_NAMESPACE, local)
        try:
            return context.varBindings[expanded]
        except:
            raise RuntimeException(RuntimeException.UNDEFINED_VARIABLE,
                                   expanded[0], expanded[1])

    def pprint(self, indent=''):
        print indent + str(self)

    def __str__(self):
        return '<Variable at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        return self._name


def ParsedFunctionCallExpr(name, args):
    name = string.strip(name)
    key = SplitQName(name)
    count = len(args)
    if count == 0:
        return FunctionCall(name, key, args)
    if count == 1:
        return FunctionCall1(name, key, args)
    if count == 2:
        return FunctionCall2(name, key, args)
    if count == 3:
        return FunctionCall3(name, key, args)
    return FunctionCallN(name, key, args)


class FunctionCall:
    def __init__(self, name, key, args):
        self._name = name
        self._key = key
        self._args = args
        self._func = None

    def pprint(self, indent=''):
        print indent + str(self)
        for arg in self._args:
            arg.pprint(indent + '  ')

    def error(self, *args):
        raise Exception('Unknown function call: %s' % self._name)

    def evaluate(self, context):
        """Call the function"""
        if not self._func:
            (prefix, local) = self._key
            uri = context.processorNss.get(prefix)
            if prefix and not uri:
                raise RuntimeException(RuntimeException.UNDEFINED_PREFIX, prefix)
            expanded = (prefix and uri or EMPTY_NAMESPACE, local)
            self._func = (g_extFunctions.get(expanded) or
                          CoreFunctions.CoreFunctions.get(expanded, self.error))
        try:
            result = self._func(context)
        except TypeError:
            raise RuntimeException(RuntimeException.WRONG_ARGUMENTS, str(expanded), '')
        return result

    def __getinitargs__(self):
        return (self._name, self._key, self._args)

    def __getstate__(self):
        state = vars(self).copy()
        del state['_func']
        return state
                    
    def __str__(self):
        return '<%s at %x: %s>' % (self.__class__.__name__, id(self), repr(self))

    def __repr__(self):
        result = self._name + '('
        if len(self._args):
            result = result + repr(self._args[0])
            for arg in self._args[1:]:
                result = result + ', ' + repr(arg)
        return result + ')'
        

class FunctionCall1(FunctionCall):
    def __init__(self, name, key, args):
        FunctionCall.__init__(self, name, key, args)
        self._arg0 = args[0]

    def evaluate(self, context):
        arg0 = self._arg0.evaluate(context)
        if not self._func:
            (prefix, local) = self._key
            uri = context.processorNss.get(prefix)
            if prefix and not uri:
                raise RuntimeException(RuntimeException.UNDEFINED_PREFIX, prefix)
            expanded = (prefix and uri or EMPTY_NAMESPACE, local)
            self._func = (g_extFunctions.get(expanded) or
                          CoreFunctions.CoreFunctions.get(expanded, self.error))
        try:
            result = self._func(context, arg0)
        except TypeError:
            raise RuntimeException(RuntimeException.WRONG_ARGUMENTS, str(expanded), '')
        return result


class FunctionCall2(FunctionCall):
    def __init__(self, name, key, args):
        FunctionCall.__init__(self, name, key, args)
        self._arg0 = args[0]
        self._arg1 = args[1]

    def evaluate(self, context):
        arg0 = self._arg0.evaluate(context)
        arg1 = self._arg1.evaluate(context)
        if not self._func:
            (prefix, local) = self._key
            uri = context.processorNss.get(prefix)
            if prefix and not uri:
                raise RuntimeException(RuntimeException.UNDEFINED_PREFIX, prefix)
            expanded = (prefix and uri or EMPTY_NAMESPACE, local)
            self._func = (g_extFunctions.get(expanded) or
                          CoreFunctions.CoreFunctions.get(expanded, self.error))
        try:
            result = self._func(context, arg0, arg1)
        except TypeError:
            raise RuntimeException(RuntimeException.WRONG_ARGUMENTS, str(expanded), '')
        return result


class FunctionCall3(FunctionCall):
    def __init__(self, name, key, args):
        FunctionCall.__init__(self, name, key, args)
        self._arg0 = args[0]
        self._arg1 = args[1]
        self._arg2 = args[2]

    def evaluate(self, context):
        arg0 = self._arg0.evaluate(context)
        arg1 = self._arg1.evaluate(context)
        arg2 = self._arg2.evaluate(context)
        if not self._func:
            (prefix, local) = self._key
            uri = context.processorNss.get(prefix)
            if prefix and not uri:
                raise RuntimeException(RuntimeException.UNDEFINED_PREFIX, prefix)
            expanded = (prefix and uri or EMPTY_NAMESPACE, local)
            self._func = (g_extFunctions.get(expanded) or
                          CoreFunctions.CoreFunctions.get(expanded, self.error))
        try:
            result = self._func(context, arg0, arg1, arg2)
        except TypeError:
            raise RuntimeException(RuntimeException.WRONG_ARGUMENTS, str(expanded), '')
        return result


class FunctionCallN(FunctionCall):
    def __init__(self, name, key, args):
        FunctionCall.__init__(self, name, key, args)

    def evaluate(self, context):
        args = [context] + map(lambda x, c=context:
                               x.evaluate(c),
                               self._args)
        if not self._func:
            (prefix, local) = self._key
            uri = context.processorNss.get(prefix)
            if prefix and not uri:
                raise RuntimeException(RuntimeException.UNDEFINED_PREFIX, prefix)
            expanded = (prefix and uri or EMPTY_NAMESPACE, local)
            self._func = (g_extFunctions.get(expanded) or
                          CoreFunctions.CoreFunctions.get(expanded, self.error))
        try:
            result = apply(self._func, args)
        except TypeError:
            raise RuntimeException(RuntimeException.WRONG_ARGUMENTS, str(expanded), '')
        return result


#Node Set Expressions
#These must return a node set

class ParsedUnionExpr:
    def __init__(self,left,right):
        self._left = left
        self._right = right

    def pprint(self, indent=''):
        print indent + str(self)
        self._left.pprint(indent + '  ')
        self._right.pprint(indent + '  ')

    def evaluate(self, context):
        lSet = self._left.evaluate(context)
        if type(lSet) != type([]):
            raise "Left Expression does not evaluate to a node set"
        rSet = self._right.evaluate(context)
        if type(rSet) != type([]):
            raise "Right Expression does not evaluate to a node set"
        set = Set.Union(lSet, rSet)
        set = Util.SortDocOrder(set)
        return set

    def __str__(self):
        return '<UnionExpr at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        return repr(self._left) + ' | ' + repr(self._right)


class ParsedPathExpr:
    def __init__(self, descendant, left, right):
        self._left = left
        self._right = right
        if descendant:
            nt = ParsedNodeTest.ParsedNodeTest('node', '')
            axis = ParsedAxisSpecifier.ParsedAxisSpecifier('descendant-or-self')
            from xml.xpath import ParsedPredicateList
            pList = ParsedPredicateList.ParsedPredicateList([])
            self._step = ParsedStep.ParsedStep(axis, nt, pList)
        else:
            self._step = None

    def pprint(self, indent=''):
        print indent + str(self)
        self._left.pprint(indent + '  ')
        self._right.pprint(indent + '  ')

    def evaluate(self, context):
        """Evaluate the left, then if op =// the parsedStep, then the right, push context each time"""
        """Returns a node set"""

        rt = self._left.evaluate(context)
        if type(rt) != type([]):
            raise "Invalid Expression for a PathExpr %s" % str(self._left)

        origState = context.copyNodePosSize()
        if self._step:
            res = []
            l = len(rt)
            for ctr in range(l):
                r = rt[ctr]
                context.setNodePosSize((r,ctr+1,l))
                subRt = self._step.select(context)
                res = Set.Union(res,subRt)
            rt = res
        res = []
        l = len(rt)
        for ctr in range(l):
            r = rt[ctr]
            context.setNodePosSize((r,ctr+1,l))
            subRt = self._right.select(context)
            if type(subRt) != type([]):
                raise Exception("Right Expression does not evaluate to a Node Set")
            res = Set.Union(res,subRt)

        context.setNodePosSize(origState)
        return res

    def __str__(self):
        return '<PathExpr at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        op = self._step and '//' or '/'
        return repr(self._left) + op + repr(self._right)


class ParsedFilterExpr:
    def __init__(self, filter, predicates):
        self._filter = filter
        self._predicates = predicates

    def evaluate(self, context):
        """
        evaluate(context) -> node-set
        Evaluate our filter into a node set, filter that through the predicates.
        """
        node_set = self._filter.evaluate(context)
        if type(node_set) != type([]):
            raise "ParsedFilterExpr: return value must evalute to a node-set"
        if node_set:
            node_set = self._predicates.filter(node_set, context, reverse=0)
        return node_set

    def pprint(self, indent=''):
        print indent + str(self)
        self._filter.pprint(indent + '  ')
        self._predicates.pprint(indent + '  ')

    def shiftContext(self,context,index,set,len,func):
        return func(context)

    def __str__(self):
        return '<FilterExpr at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        return repr(self._filter) + repr(self._predicates)

#Boolean Expressions
#All will return a boolean value

class ParsedOrExpr:
    def __init__(self, left, right):
        self._left = left
        self._right = right

    def pprint(self, indent=''):
        print indent + str(self)
        self._left.pprint(indent + '  ')
        self._right.pprint(indent + '  ')

    def evaluate(self, context):
        rt = Conversions.BooleanEvaluate(self._left, context)
        if not rt:
            rt = Conversions.BooleanEvaluate(self._right, context)
        return rt

    def __str__(self):
        return '<OrExpr at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        return repr(self._left) +' or ' + repr(self._right)


class ParsedAndExpr:
    def __init__(self,left,right):
        self._left = left
        self._right = right

    def evaluate(self, context):
        rt = Conversions.BooleanEvaluate(self._left, context)
        if rt:
            rt = Conversions.BooleanEvaluate(self._right, context)
        return rt

    def __str__(self):
        return '<AndExpr at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        return repr(self._left) + ' and ' + repr(self._right)

NumberTypes = [types.IntType, types.FloatType, types.LongType]

class ParsedEqualityExpr:
    def __init__(self, op, left, right):
        self._op = op
        self._left = left
        self._right = right

    def evaluate(self, context):
        if self._op == '=':
            true = boolean.true
            false = boolean.false
        else:
            true = boolean.false
            false = boolean.true

        lrt = self._left.evaluate(context)
        rrt = self._right.evaluate(context)
        lType = type(lrt)
        rType = type(rrt)
        if lType == types.ListType == rType:
            #Node set to node set
            for right_curr in rrt:
                right_curr = Conversions.StringValue(right_curr)
                for left_curr in lrt:
                    if right_curr == Conversions.StringValue(left_curr):
                        return true
            return false
        elif lType == types.ListType or rType == types.ListType:
            func = None
            if lType == types.ListType:
                set = lrt
                val = rrt
            else:
                set = rrt
                val = lrt
            if type(val) in NumberTypes:
                func = Conversions.NumberValue
            elif boolean.IsBooleanType(val):
                func = Conversions.BooleanValue
            elif type(val) == types.StringType:
                func = Conversions.StringValue
            else:
                #Deal with e.g. RTFs
                val = Conversions.StringValue(val)
                func = Conversions.StringValue
            for n in set:
                if func(n) == val:
                    return true
            return false

        if boolean.IsBooleanType(lrt) or boolean.IsBooleanType(rrt):
            rt = Conversions.BooleanValue(lrt) == Conversions.BooleanValue(rrt)
        elif lType in NumberTypes or rType in NumberTypes:
            rt = Conversions.NumberValue(lrt) == Conversions.NumberValue(rrt)
        else:
            rt = Conversions.StringValue(lrt) == Conversions.StringValue(rrt)
        if rt:
            # Due to the swapping of true/false, true might evaluate to 0
            # We cannot compact this to 'rt and true or false'
            return true
        return false
        
    def pprint(self, indent=''):
        print indent + str(self)
        self._left.pprint(indent + '  ')
        self._right.pprint(indent + '  ')

    def __str__(self):
        return '<EqualityExpr at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        if self._op == '=':
            op = ' = '
        else:
            op = ' != '
        return repr(self._left) + op + repr(self._right)



class ParsedRelationalExpr:
    def __init__(self, opcode, left, right):
        self._op = opcode

        if isinstance(left, ParsedLiteralExpr):
            self._left = Conversions.NumberValue(left.evaluate(None))
            self._leftLit = 1
        else:
            self._left = left
            self._leftLit = 0

        if isinstance(right, ParsedLiteralExpr):
            self._right = Conversions.NumberValue(right.evaluate(None))
            self._rightLit = 1
        else:
            self._right = right
            self._rightLit = 0

    def evaluate(self, context):
        if self._leftLit:
            lrt = self._left
        else:
            lrt = Conversions.NumberValue(self._left.evaluate(context))
        if self._rightLit:
            rrt = self._right
        else:
            rrt = Conversions.NumberValue(self._right.evaluate(context))

        if self._op == 0:
            rt = (lrt < rrt)
        elif self._op == 1:
            rt = (lrt <= rrt)
        elif self._op == 2:
            rt = (lrt > rrt)
        elif self._op == 3:
            rt = (lrt >= rrt)
        return rt and boolean.true or boolean.false

    def pprint(self, indent=''):
        print indent + str(self)
        if type(self._left) == types.InstanceType:
            self._left.pprint(indent + '  ')
        else:
            print indent + '  ' + '<Primitive: %s>' % str(self._left)
        if type(self._right) == types.InstanceType:
            self._right.pprint(indent + '  ')
        else:
            print indent + '  ' + '<Primitive: %s>' % str(self._right)

    def __str__(self):
        return '<RelationalExpr at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        if self._op == 0:
            op = ' < '
        elif self._op == 1:
            op = ' <= '
        elif self._op == 2:
            op = ' > '
        elif self._op == 3:
            op = ' >= '
        return repr(self._left) + op + repr(self._right)

#Number Expressions


class ParsedAdditiveExpr:
    def __init__(self, sign, left, right):
        self._sign = sign
        self._leftLit = 0
        self._rightLit = 0
        if isinstance(left, ParsedLiteralExpr):
            self._leftLit = 1
            self._left = Conversions.NumberValue(left.evaluate(None))
        else:
            self._left = left
        if isinstance(right, ParsedLiteralExpr):
            self._rightLit = 1
            self._right = Conversions.NumberValue(right.evaluate(None))
        else:
            self._right = right
        return

    def evaluate(self, context):
        '''returns a number'''
        if self._leftLit:
            lrt = self._left
        else:
            lrt = self._left.evaluate(context)
            lrt = Conversions.NumberValue(lrt)
        if self._rightLit:
            rrt = self._right
        else:
            rrt = self._right.evaluate(context)
            rrt = Conversions.NumberValue(rrt)
        return lrt + (rrt * self._sign)

    def __str__(self):
        return '<AdditiveExpr at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        if self._sign > 0:
            op = ' + '
        else:
            op = ' - '
        return repr(self._left) + op + repr(self._right)


from xml.xpath import Inf, NaN

class ParsedMultiplicativeExpr:
    def __init__(self, opcode, left, right):
        self._op = opcode
        self._left = left
        self._right = right

    def evaluate(self, context):
        '''returns a number'''
        lrt = self._left.evaluate(context)
        lrt = Conversions.NumberValue(lrt)
        rrt = self._right.evaluate(context)
        rrt = Conversions.NumberValue(rrt)
        res = 0
        if self._op == 0:
            res = lrt * rrt
        elif self._op == 1:
            if rrt == 0:
                res = NaN
            else:
                res = lrt / rrt
        elif self._op == 2:
            if rrt == 0:
                res = NaN
            else:
                res = lrt % rrt
        return res

    def __str__(self):
        return '<MultiplicativeExpr at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        if self._op == 0:
            op = ' * '
        elif self._op == 1:
            op = ' div '
        elif self._op == 2:
            op = ' mod '
        return repr(self._left) + op + repr(self._right)

class ParsedUnaryExpr:
    def __init__(self,exp):
        self._exp = exp

    def evaluate(self, context):
        '''returns a number'''
        exp = self._exp.evaluate(context)
        exp = Conversions.NumberValue(exp)
        rt = exp * -1.0
        return rt

    def __str__(self):
        return '<UnaryExpr at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        return '-' + repr(self._exp)
