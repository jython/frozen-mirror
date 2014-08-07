# Expression types
ABSOLUTE_LOCATION_PATH = 1                      
ABBREVIATED_ABSOLUTE_LOCATION_PATH = 2          
RELATIVE_LOCATION_PATH = 3                      
ABBREVIATED_RELATIVE_LOCATION_PATH = 4          
STEP_EXPR = 5                                        
NODE_TEST = 6                                   
NAME_TEST = 7                                   
BINARY_EXPR = 8                                 
UNARY_EXPR = 9                                  
PATH_EXPR = 10                                  
ABBREVIATED_PATH_EXPR = 11
FILTER_EXPR = 12                                
VARIABLE_REFERENCE = 13                         
LITERAL = 14                                    
NUMBER = 15                                     
FUNCTION_CALL = 16                              

# Axis specifier
ANCESTOR_AXIS = 1
ANCESTOR_OR_SELF_AXIS = 2
ATTRIBUTE_AXIS = 3
CHILD_AXIS = 4
DESCENDANT_AXIS = 5
DESCENDANT_OR_SELF_AXIS = 6
FOLLOWING_AXIS = 7
FOLLOWING_SIBLING_AXIS = 8
NAMESPACE_AXIS = 9
PARENT_AXIS = 10
PRECEDING_AXIS = 11
PRECEDING_SIBLING_AXIS = 12
SELF_AXIS = 13

# Node tests
COMMENT = 1
TEXT = 2
PROCESSING_INSTRUCTION = 3
NODE = 4

# Binary operators 
OR_OPERATOR = 1
AND_OPERATOR = 2
EQ_OPERATOR = 3
NEQ_OPERATOR = 4
LT_OPERATOR = 5
GT_OPERATOR = 6
LE_OPERATOR = 7
GE_OPERATOR = 8
PLUS_OPERATOR = 9
MINUS_OPERATOR = 10
TIMES_OPERATOR = 11
DIV_OPERATOR = 12
MOD_OPERATOR = 13
UNION_OPERATOR = 14

from xml.xpath import ParsedExpr, ParsedNodeTest
from xml.xpath.ParsedAbsoluteLocationPath import ParsedAbsoluteLocationPath
from xml.xpath.ParsedRelativeLocationPath import ParsedRelativeLocationPath
from xml.xpath.ParsedAbbreviatedRelativeLocationPath import ParsedAbbreviatedRelativeLocationPath
from xml.xpath.ParsedAbbreviatedAbsoluteLocationPath import ParsedAbbreviatedAbsoluteLocationPath
PALP = ParsedAbsoluteLocationPath
PRLP = ParsedRelativeLocationPath
PAALP = ParsedAbbreviatedAbsoluteLocationPath
PARLP = ParsedAbbreviatedRelativeLocationPath
from xml.xpath.ParsedStep import ParsedStep
from xml.xpath.ParsedAxisSpecifier import ParsedAxisSpecifier
from xml.xpath.ParsedPredicateList import ParsedPredicateList

from xml.xpath.ParsedAbsoluteLocationPath import ParsedAbsoluteLocationPath
from xml.xpath.ParsedRelativeLocationPath import ParsedRelativeLocationPath

# XSLT
try:
    from xml.xslt.ParsedPattern import ParsedPattern
    from xml.xslt import ParsedStepPattern
    from xml.xslt import ParsedRelativePathPattern
    from xml.xslt import ParsedLocationPathPattern
    _xslt_patterns = 1
except:
    _xslt_patterns = 0

import string,types

class FtFactory:
    createAbsoluteLocationPath = PALP
    createAbbreviatedAbsoluteLocationPath = PAALP
    createRelativeLocationPath = PRLP
    createAbbreviatedRelativeLocationPath = PARLP

    def createStep(self, axis, test, predicates):
        return ParsedStep(axis, test, ParsedPredicateList(predicates))

    def createAbbreviatedStep(self,parent):
        if parent:
            type = 'parent'
        else:
            type = 'self'
        return ParsedStep(ParsedAxisSpecifier(type),
                          ParsedNodeTest.ParsedNodeTest('node',""),
                          ParsedPredicateList([]))

    axisMap = {
        ANCESTOR_AXIS: 'ancestor',
        ANCESTOR_OR_SELF_AXIS: 'ancestor-or-self',
        ATTRIBUTE_AXIS: 'attribute',
        CHILD_AXIS: 'child',
        DESCENDANT_AXIS: 'descendant',
        DESCENDANT_OR_SELF_AXIS: 'descendant-or-self',
        FOLLOWING_AXIS: 'following',
        FOLLOWING_SIBLING_AXIS: 'following-sibling',
        NAMESPACE_AXIS: 'namespace',
        PARENT_AXIS: 'parent',
        PRECEDING_AXIS: 'preceding',
        PRECEDING_SIBLING_AXIS: 'preceding-sibling',
        SELF_AXIS: 'self'
        }
        
    def createAxisSpecifier(self,axis):
        # XXX: may use axis-ANCESTOR+XPATH.ANCESTOR instead
        return ParsedAxisSpecifier(self.axisMap[axis])

    ntMap = {
        COMMENT: 'comment',
        TEXT: 'text',
        PROCESSING_INSTRUCTION: 'processing-instruction',
        NODE: 'node'
        }
        
    def createNodeTest(self,type,val):
        if val is None:
            val = ""
        return ParsedNodeTest.ParsedNodeTest(self.ntMap[type],val)

    def createNameTest(self,prefix,local):
        if local == '*':
            if prefix:
                return ParsedNodeTest.LocalNameTest(prefix)
            else:
                return ParsedNodeTest.PrincipalTypeTest()
        if prefix:
            return ParsedNodeTest.QualifiedNameTest(prefix, local)
        return ParsedNodeTest.NodeNameTest(local)

    opMap = {
        OR_OPERATOR: ParsedExpr.ParsedOrExpr,
        AND_OPERATOR: ParsedExpr.ParsedAndExpr,
        EQ_OPERATOR: (ParsedExpr.ParsedEqualityExpr,"="),
        NEQ_OPERATOR: (ParsedExpr.ParsedEqualityExpr, "!="),
        LT_OPERATOR: (ParsedExpr.ParsedRelationalExpr, 0),
        GT_OPERATOR: (ParsedExpr.ParsedRelationalExpr, 2),
        LE_OPERATOR: (ParsedExpr.ParsedRelationalExpr, 1),
        GE_OPERATOR: (ParsedExpr.ParsedRelationalExpr, 3),
        PLUS_OPERATOR: (ParsedExpr.ParsedAdditiveExpr, 1),
        MINUS_OPERATOR: (ParsedExpr.ParsedAdditiveExpr, -1),
        TIMES_OPERATOR: (ParsedExpr.ParsedMultiplicativeExpr, 0),
        DIV_OPERATOR: (ParsedExpr.ParsedMultiplicativeExpr, 1),
        MOD_OPERATOR: (ParsedExpr.ParsedMultiplicativeExpr, 2),
        UNION_OPERATOR: ParsedExpr.ParsedUnionExpr,
        }

    def createNumericExpr(self,operator,left,right):
        if operator == MINUS_OPERATOR and right is None:
            return ParsedExpr.ParsedUnaryExpr(left)
        cl = self.opMap[operator]
        if type(cl) is types.TupleType:
            return cl[0](cl[1],left,right)
        return cl(left,right)

    def createBooleanExpr(self,operator,left,right):
        cl = self.opMap[operator]
        if type(cl) is types.TupleType:
            return cl[0](cl[1],left,right)
        return cl(left,right)

    def createPathExpr(self,left,right):
        return ParsedExpr.ParsedPathExpr("/",left,right)

    def createAbbreviatedPathExpr(self,left,right):
        return ParsedExpr.ParsedPathExpr(XPATH.DOUBLE_SLASH,left,right)

    def createFilterExpr(self, filter, predicates):
        return ParsedExpr.ParsedFilterExpr(filter, ParsedPredicateList(predicates))

    def createVariableReference(self,prefix,localName):
        if prefix:
            return ParsedExpr.ParsedVariableReferenceExpr('$'+prefix+':'+localName)
        else:
            return ParsedExpr.ParsedVariableReferenceExpr('$'+localName)
    createLiteral = ParsedExpr.ParsedLiteralExpr
    createNumber = ParsedExpr.ParsedNLiteralExpr

    # Cannot directly import, since ParsedNLiteralExpr is a function
    def createFunctionCall(self,prefix,localName,args):
        if prefix:
            return ParsedExpr.ParsedFunctionCallExpr(prefix+':'+localName,args)
        else:
            return ParsedExpr.ParsedFunctionCallExpr(localName,args)

    # XSLT
    if _xslt_patterns: createPattern = ParsedPattern

    def createLocationPathPattern(self, idkey, isparent, step):
        if idkey is None and step is None:
            # /
            return ParsedLocationPathPattern.RootPattern()
        if step is None:
            # idkey
            return ParsedLocationPathPattern.IdKeyPattern(idkey)
        if not isparent and idkey is None:
            # rel
            # // rel
            return step
        last = step
        while 1:
            parent = last.parent
            if hasattr(parent,"parent"):
                last = parent
            else:
                break
        if isparent and idkey is None:
            # / rel
            ctor = ParsedStepPattern.RootParentStepPattern
            args = ()
        elif isparent:
            # idkey / rel
            ctor = ParsedLocationPathPattern.IdKeyParentPattern
            args = (idkey,)
        else:
            # idkey // rel
            args = (idkey,)
            if parent is None:
                ctor = ParsedLocationPathPattern.IdKeyParentPattern
            else:
                ctor = ParsedLocationPathPattern.IdKeyAncestorPattern
        if parent is None:
            step = apply(ctor, args+last.getShortcut())
        else:
            last.parent = apply(ctor, args+last.parentAxis())
        return step
        
    
    def createRelativePathPattern(self, rel, parent, step):
        parent_test, parent_axis = rel.getShortcut()
        node_test, axis_type = step.getShortcut()
        if parent:
            ctor = ParsedStepPattern.ParentStepPattern
        else:
            ctor = ParsedStepPattern.AncestorStepPattern
        return ctor(node_test, axis_type, parent_test, parent_axis)

    def createStepPattern(self, axis, test, predicates):
        axis = axis.principalType
        if predicates:
            predicates = ParsedPredicateList(predicates)
            return ParsedStepPattern.PredicateStepPattern(test, axis, predicates)
        else:
            return ParsedStepPattern.StepPattern(test, axis)

factory = FtFactory()

import yappsrt
class SyntaxError(yappsrt.SyntaxError):
    def __init__(self, pos, msg, str):
	yappsrt.SyntaxError.__init__(self, pos, msg)
        self.str = str

    def __repr__(self):
	if self.pos < 0:
            return "#<syntax-error>"
	else:
            text = self.str
            if len(self.str) > 30:
                start = self.pos - 15
                if start>3:
                    text = "..."+self.str[start:]
                if len(text) > 30:
                    text = text[:27]+"..."
            fmt = "SyntaxError[@ char %s in '%s': %s]"
            return  fmt % (repr(self.pos), text, self.msg)

#obsolete
class Parser:
    def parseLocationPath(self, str):
        try:
            from XPathGrammar import XPath,XPathScanner
            return XPath(XPathScanner(str),factory).Start()
        except yappsrt.SyntaxError,e:
            raise SyntaxError(e.pos, e.msg, str)

    def parseExpr(self, str):
        try:
            from XPathGrammar import XPath,XPathScanner
            return XPath(XPathScanner(str),factory).FullExpr()
        except yappsrt.SyntaxError,e:
            raise SyntaxError(e.pos, e.msg, str)

    def parsePattern(self, str):
        try:
            from XPathGrammar import XPath,XPathScanner
            return XPath(XPathScanner(str),factory).FullPattern()
        except yappsrt.SyntaxError,e:
            raise SyntaxError(e.pos, e.msg, str)

parser = Parser()

def Compile(str):
    return parser.parseExpr(str)

def CompilePattern(str):
    return parser.parsePattern(str)

class Factory:
    def __init__(self, cl):
        self.new = cl

class ExprParser:
    def parse(self, str):
        try:
            from XPathGrammar import XPath,XPathScanner
            return XPath(XPathScanner(str),factory).FullExpr()
        except yappsrt.SyntaxError,e:
            raise SyntaxError(e.pos, e.msg, str)
ExprParserFactory = Factory(ExprParser)

class PatternParser:
    def parse(self, str):
        try:
            from XPathGrammar import XPath,XPathScanner
            return XPath(XPathScanner(str),factory).FullPattern()
        except yappsrt.SyntaxError,e:
            raise SyntaxError(e.pos, e.msg, str)

PatternParserFactory = Factory(PatternParser)
