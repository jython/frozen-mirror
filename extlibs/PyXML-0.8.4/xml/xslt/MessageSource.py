from xml.xslt import Error
from xml.FtCore import get_translator

_ = get_translator("xslt")


g_errorMessages = {
    Error.INTERNAL_ERROR: _('There is an internal bug in 4XSLT.  Please report this error code to support@4suite.org: %s'),
    Error.PATTERN_SYNTAX: _('Syntax error in pattern at location %s (XPattern production number: %d).'),
    Error.PATTERN_SEMANTIC: _('Parse tree error in pattern at location %s (XPattern production number: %d, error type: %s, error value: %s, traceback:\n%s'),

    Error.APPLYIMPORTS_WITH_NULL_CURR_TPL: _('apply-imports used where there is no current template.  (see XSLT Spec)'),
    Error.ILLEGAL_IMPORT: _('import is not allowed here.  '),
    Error.STYLESHEET_PARSE_ERROR: _('Stylesheet (%s): XML parse error at line %d, column %d: %s'),
    Error.CIRCULAR_VAR: _('Circular variable reference error (see XSLT Spec: 11.4) for variable or parameter: (%s, %s)'),
    Error.SOURCE_PARSE_ERROR: _('Source document (%s): %s'),
#    Error.STYLESHEET_PARSE_ERROR: _('Stylesheet(XML) parse exception at line %d, column %d: %s'),
#    Error.SOURCE_PARSE_ERROR: _('Source document XML parse exception at line %d, column %d: %s'),
    Error.ILLEGAL_CALLTEMPLATE_CHILD: _('call-templates child must be with-param., (see XSLT Spec: 6)'),
    Error.ILLEGAL_APPLYTEMPLATE_CHILD: _('apply-templates child must be with-param or sort., (see XSLT Spec: 5.4)'),
    Error.WHEN_AFTER_OTHERWISE: _('when cannot succeed otherwise.'),
    Error.MULTIPLE_OTHERWISE: _('there cannot be more than one otherwise within a choose.'),
    Error.ILLEGAL_CHOOSE_CHILD: _('choose child must be "when" or "otherwise"., (see XSLT Spec: 9.2)'),
    Error.CHOOSE_WHEN_AFTER_OTHERWISE: _('choose cannot have "when" child after "otherwise" child., (see XSLT Spec: 9.2)'),
    Error.CHOOSE_MULTIPLE_OTHERWISE: _('choose only allowed one "otherwise" child., (see XSLT Spec: 9.2)'),
    Error.CHOOSE_REQUIRES_WHEN_CHILD: _('choose must have atleast one "when" child., (see XSLT Spec: 9.2)'),
    Error.ILLEGAL_TEXT_CHILD: _('xsl:text cannot have any child elements"., (see XSLT Spec: 7.2)'),
    Error.ILLEGAL_ATTRIBUTESET_CHILD: _('attribute-set child must be "attribute"., (see XSLT Spec: 7.1.4)'),
    Error.ATTRIBUTESET_REQUIRES_NAME: _('missing attribute-set required attribute name., (see XSLT Spec: 7.1.4)'),
    Error.INVALID_FOREACH_SELECT: _('for-each select attribute must evaluate to a node set (see XSLT Spec: 8)'),

    Error.VALUEOF_MISSING_SELECT: _('missing value-of requried attribute select (see XSLT Spec: 7.6.1)'),
    Error.COPYOF_MISSING_SELECT: _('missing copy-of requried attribute select (see XSLT Spec: 11.3)'),
    Error.WHEN_MISSING_TEST: _('missing when requried attribute test (see XSLT Spec: 9.2)'),

    Error.TOP_LEVEL_ELEM_WITH_NULL_NS: _(''),
    Error.XSLT_ILLEGAL_ATTR: _('Illegal attribute "%s" with null namespace in XSLT element "%s" (see XSLT Spec: 2.1).'),
    Error.XSLT_ILLEGAL_ELEMENT: _('Illegal Element "%s" in XSLT Namespace (see XSLT Spec: 2.1).'),
    Error.STYLESHEET_ILLEGAL_ROOT: _('Illegal Document Root Element "%s" (see XSLT Spec: 2.2).'),

    Error.ILLEGAL_SORT_DATA_TYPE_VALUE: _('The "data-type" attribute of sort must be either "text" or "number" (see XSLT Spec: 10).'),
    Error.ILLEGAL_SORT_CASE_ORDER_VALUE: _('The "case-order" attribute of sort must be either "upper-first" or "lower-first" (see XSLT Spec: 10)'),
    Error.ILLEGAL_SORT_ORDER_VALUE: _('The "order" attribute of sort must be either "ascending" or "descending". (see XSLT Spec: 10)'),
    Error.AVT_SYNTAX: _('Syntax error in attribute-value template. (see XSLT Spec: 7.6.2)'),
    Error.NO_STYLESHEET: _('No stylesheets to process.'),
    Error.STYLESHEET_MISSING_VERSION: _('Style-sheet document root element must have a version attribute.  (see XSLT Spec: 2.2 - 2.3)'),
    Error.STYLESHEET_MISSING_VERSION_NOTE1: _('Style-sheet document root element must have a version attribute.  (see XSLT Spec: 2.2 - 2.3).  Note that you do not have the http://www.w3.org/1999/XSL/Transform namespace declared in your top element.'),
    Error.ILLEGAL_TEMPLATE_PRIORITY: _('Invalid priority value for template. (see XSLT Spec: 5.5)'),

    Error.ILLEGAL_NUMBER_GROUPING_SIZE_VALUE: _('The "grouping-size" attribute of number must be an integer. (see XSLT Spec: 7.7.1)'),
    Error.ILLEGAL_NUMBER_LEVEL_VALUE: _('The "level" attribute of number must be "single", "multiple" or "any". (see XSLT Spec: 7.7)'),
    Error.ILLEGAL_NUMBER_FORMAT_VALUE: _('Invalid value for "format" attribute of number. (see XSLT Spec: 7.7)'),
    Error.ILLEGAL_NUMBER_LETTER_VALUE_VALUE: _('The "letter-value" attribute of number must be "alphabetic" or "traditional". (see XSLT Spec: 7.7.1)'),

    Error.INVALID_NAMESPACE_ALIAS: _('Invalid arguments to the namespace-alias instruction. (see XSLT Spec: 7.1.1)'),

    Error.WRONG_NUMBER_OF_ARGUMENTS: _('A built-in or extension function was called with the wrong number of arguments.'),
    Error.WRONG_ARGUMENT_TYPE: _('A built-in or extension function was called with the wrong number of arguments.'),

    Error.FEATURE_NOT_SUPPORTED: _('4XSLT does not yet support this feature.'),

    Error.INVALID_PATTERN: _('Invalid pattern (%s).'),
    Error.INVALID_OPERAND_IN_PATTERN: _('Invalid operand (%s) in pattern.'),
    Error.INVALID_OPERAND_ID: _('Invalid operand (%s) for "id".'),
    Error.INVALID_OPERAND_IDREL: _('Invalid operand (%s) for "id" with relative path.'),
    Error.INVALID_OPERAND_SREL: _('Invalid operand (%s) in absolute location path.'),
    Error.INVALID_OPERAND_REL: _('Invalid operand (%s) in relative location path.'),
    Error.INVALID_LEFT_OR_RIGHT_OPERAND_S: _('Invalid left or right operand (%s or %s) to "/".'),
    Error.INVALID_LEFT_OR_RIGHT_OPERAND_RELP: _('Invalid left or right operand (%s or %s) in relative path.'),
    Error.INVALID_AXIS_SPEC: _('Invalid axis specifier'),
    Error.INVALID_NODE_TEST: _('Invalid node test'),
    Error.INVALID_PREDICATE_LIST: _('Invalid predicate list'),

    Error.ATTRIBUTE_ADDED_AFTER_ELEMENT: _('xsl:attribute instantiated within an element instantiation after a child element has been added. (see XSLT Spec: 7.1.3)'),
    Error.ATTRIBUTE_MISSING_NAME: _('xsl:attribute missing required name attribute. (see XSLT Spec: 7.1.3)'),


    Error.UNDEFINED_ATTRIBUTE_SET: _('Undefined attribute set (%s)'),
    Error.RESTRICTED_OUTPUT_VIOLATION: _('The requested output of element "%s" is forbidden accirding to output restrictions'),
    #Error.: _(''),

    Error.STYLESHEET_REQUESTED_TERMINATION: _('A message instruction in the Stylesheet requested termination of processing:\n%s'),
    }

