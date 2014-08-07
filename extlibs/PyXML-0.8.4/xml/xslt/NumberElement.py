########################################################################
#
# File Name:            NumberElement.py
#
#
"""
Implementation of the XSLT Spec number stylesheet element.
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import re, string
from xml.dom import EMPTY_NAMESPACE
from xml.xslt import Roman
import xml.xslt
import xml.dom.ext
from xml.dom import Node
from xml.xslt import XsltElement, XsltException, Error, AttributeValueTemplate
from xml.xslt import XPatternParser
from xml.xpath import XPathParser, Conversions

#Pattern for format tokens (see spec 7.7.1)
g_formatToken = re.compile(r"([^a-zA-Z0-9]*)([a-zA-Z0-9]+)([^a-zA-Z0-9]*)")


class NumberElement(XsltElement):
    legalAttrs = ('level', 'count', 'from', 'value', 'format', 'lang', 'letter-value', 'grouping-separator', 'grouping-size',)

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE, localName='number',
                 prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)

    def setup(self):
        self._nss = {}
        self._level = None
        self._count = None
        self._from = None
        self._value = None
        self._format = None
        self._lang = None
        self._letter_value = None
        self._grouping_separator = None
        self._grouping_size = None
        self._value_expr = None
        self._sibling_expr = None
        self._count_prior_doc_order_expr = None
        self._count_pattern = None
        self._ancorself_expr = None

        path_parser = XPathParser.XPathParser()
        pattern_parser = XPatternParser.XPatternParser()
        self.__dict__['_level'] = self.getAttributeNS(EMPTY_NAMESPACE, 'level') or 'single'
        if self._level not in ['single', 'multiple', 'any']:
            raise XsltException(Error.ILLEGAL_NUMBER_LEVEL_VALUE)
        self.__dict__['_count'] = self.getAttributeNS(EMPTY_NAMESPACE, 'count')
        self.__dict__['_from'] = self.getAttributeNS(EMPTY_NAMESPACE, 'from')
        self.__dict__['_value'] = self.getAttributeNS(EMPTY_NAMESPACE, 'value')
        format = self.getAttributeNS(EMPTY_NAMESPACE, 'format')
        self.__dict__['_format'] = format and AttributeValueTemplate.AttributeValueTemplate(format) or None
        lang = self.getAttributeNS(EMPTY_NAMESPACE, 'lang')
        self.__dict__['_lang'] = lang and AttributeValueTemplate.AttributeValueTemplate(lang) or None
        letter_value = self.getAttributeNS(EMPTY_NAMESPACE, 'letter-value')
        self.__dict__['_letter_value'] = letter_value and AttributeValueTemplate.AttributeValueTemplate(letter_value) or None
        grouping_separator = self.getAttributeNS(EMPTY_NAMESPACE, 'grouping-separator')
        self.__dict__['_grouping_separator'] = grouping_separator and AttributeValueTemplate.AttributeValueTemplate(grouping_separator) or None
        grouping_size = self.getAttributeNS(EMPTY_NAMESPACE, 'grouping-size')
        self.__dict__['_grouping_size'] = grouping_size and AttributeValueTemplate.AttributeValueTemplate(grouping_size) or None
        self.__dict__['_nss'] = xml.dom.ext.GetAllNs(self)

        #Prep computations
        if not self._count:
            #FIXME: Handle other node types????
            self._count = '*[name()=name(current())]'
        self._count_pattern = pattern_parser.parsePattern(self._count)
        ancestor_or_self = "ancestor-or-self::node()"
        if self._from:
            ancestor_or_self = ancestor_or_self + '[ancestor::%s]'%(self._from)
        self._ancorself_expr = path_parser.parseExpression(ancestor_or_self)
        if self._value:
            self._value_expr = path_parser.parseExpression(self._value)
            self._sibling_expr = None
            self._count_prior_doc_order_expr = None
        else:
            self._sibling_expr = path_parser.parseExpression('preceding-sibling::node()')
            patterns = pattern_parser.parsePattern(self._count)._patterns
            count_prior_doc_order = ''

            if self._from:
                froms = pattern_parser.parsePattern(self._from)._patterns
                pred = "["
                for fro in froms:
                    pred = pred + 'ancestor::' + repr(fro)
                    if fro != froms[-1]:
                        pred = pred + '|'
                pred = pred + ']'
            for count in patterns:
                if self._from:
                    count_prior_doc_order = count_prior_doc_order + 'ancestor-or-self::' + repr(count) + pred + '|preceding::' +repr(count) + pred
                else:
                    count_prior_doc_order = count_prior_doc_order + 'ancestor-or-self::' + repr(count) + '|preceding::' + repr(count)
                if count != patterns[-1]:
                    count_prior_doc_order = count_prior_doc_order + '|'
                    
            self._count_prior_doc_order_expr = path_parser.parseExpression(count_prior_doc_order)
        return

    def instantiate(self, context, processor, nodeList=None, specList=None):
        if nodeList is None:
            nodeList = []
        if specList is None:
            specList = []

        origState = context.copy()
        context.setNamespaces(self._nss)

        if self._format:
            format = self._format.evaluate(context)
        else:
            format = '1'
        if self._grouping_separator:
            grouping_separator = self._grouping_separator.evaluate(context)
        else:
            grouping_separator = ','
        if self._grouping_size:
            grouping_size = self._grouping_size.evaluate(context)
        else:
            grouping_size = '3'
        if grouping_separator and grouping_size:
            try:
                grouping_size = string.atoi(grouping_size)
            except ValueError:
                raise XsltException(Error.ILLEGAL_NUMBER_GROUPING_SIZE_VALUE)
        else:
            grouping_separator = None
            grouping_size = None

        if self._letter_value:
            letter_value = self._letter_value.evaluate(context)
            if letter_value not in ['alphabetic', 'traditional']:
                raise XsltException(Error.ILLEGAL_NUMBER_LETTER_VALUE_VALUE)

        value = []
        tempState = context.copyNodePosSize()
        if self._value:
            result = self._value_expr.evaluate(context)
            value = [Conversions.NumberValue(result)]

        elif self._level == 'single':
            ancorself_result = self._ancorself_expr.evaluate(context)
            ancorself_result.reverse()
            for node in ancorself_result:
                context.node = node
                if self._count_pattern.match(context, context.node):
                    break

            sibling_result = self._sibling_expr.evaluate(context)
            value = 1
            for node in sibling_result:
                context.node = node
                if self._count_pattern.match(context, context.node):
                    value = value + 1
            value = [value]

        elif self._level == 'multiple':
            ancorself_result = self._ancorself_expr.evaluate(context)
            ancorself_result.reverse()

            count_result = []
            for node in ancorself_result:
                context.node = node
                if self._count_pattern.match(context, context.node):
                    count_result.append(node)
            context.setNodePosSize(tempState)
            value = []
            for node in count_result:
                context.node = node
                sibling_result = self._sibling_expr.evaluate(context)
                lvalue = 1
                for node in sibling_result:
                    context.node = node
                    if self._count_pattern.match(context, context.node):
                        lvalue = lvalue + 1
                value.insert(0, lvalue)

        elif self._level == 'any':
            count_result = self._count_prior_doc_order_expr.evaluate(context)
            value = [len(count_result)]
        context.setNodePosSize(tempState)

        format_tokens = []
        format_separators = []
        re_groups = g_formatToken.findall(format)
        if not re_groups:
            raise XsltException(Error.ILLEGAL_NUMBER_FORMAT_VALUE)
        pre_string = re_groups[0][0]
        post_string = re_groups[-1][2]
        for group in re_groups:
            format_tokens.append(group[1])
            format_separators.append(group[2])
        format_separators = ['.'] + format_separators[:-1]
        
        result = pre_string
        curr_index = 0
        lft = len(format_tokens)
        lfs = len(format_separators)
        for number in value:
            if curr_index: result = result + curr_sep
            if curr_index < lft:
                curr_ft = format_tokens[curr_index]
                curr_sep = format_separators[curr_index]
                curr_index = curr_index + 1
            else:
                curr_ft = format_tokens[-1]
                curr_sep = format_separators[-1]
            numstr = str(number)
            if curr_ft[-1] == '1':
                subresult = Group(
                    '0'*(len(curr_ft)-len(numstr))+numstr,
                    grouping_size,
                    grouping_separator
                    )
                result = result + subresult
            elif curr_ft == 'A':
                digits = Base26(number)
                #FIXME: faster with reduce
                for dig in digits:
                    result = result + chr(ord('A') + dig - 1)
            elif curr_ft == 'a':
                digits = Base26(number)
                for dig in digits:
                    result = result + chr(ord('a') + dig - 1)
            elif curr_ft == 'I':
                result = result + Roman.IToRoman(number)
            elif curr_ft == 'i':
                result = result + string.lower(Roman.IToRoman(number))
            else:
                raise XsltException(Error.ILLEGAL_NUMBER_FORMAT_VALUE)
        processor.writers[-1].text(result + post_string)
        context.set(origState)
        return (context,)

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         new_state = (base_state, self._nss, self._level, self._count,
                      self._from, self._value, self._format, self._lang,
                      self._letter_value, self._grouping_separator,
                      self._grouping_size, self._value_expr,
                      self._sibling_expr, self._count_prior_doc_order_expr,
                      self._count_pattern, self._ancorself_expr)
         return new_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state[0])
        self._nss = state[1]
        self._level = state[2]
        self._count = state[3]
        self._from = state[4]
        self._value = state[5]
        self._format = state[6]
        self._lang = state[7]
        self._letter_value = state[8]
        self._grouping_separator = state[9]
        self._grouping_size = state[10]
        self._value_expr = state[11]
        self._sibling_expr = state[12]
        self._count_prior_doc_order_expr = state[13]
        self._count_pattern = state[14]
        self._ancorself_expr = state[15]
        return


def Base26(n):
    #FIXME: There must be an easier/faster way in Python
    n = int(n)
    result = []
    factor = 1
    while factor < n: factor = factor * 26
    factor = factor / 26
    while n >= 26:
        digit = n / factor
        result.append(digit)
        n = n - factor * digit
        factor = factor / 26
    result.append(n)
    return result


def Group(numstr, size, sep):
    if not sep:
        return numstr
    result = ''
    start_seg = 0
    end_seg = len(numstr) % size
    while end_seg <= len(numstr):
        if end_seg:
            if end_seg == len(numstr):
                result = result + numstr[start_seg:end_seg]
            else:
                result = result + numstr[start_seg:end_seg] + sep
        start_seg = end_seg
        end_seg = end_seg + size
    return result


##Note: emacs can uncomment the ff automatically.

##To: xsl-list@mulberrytech.com
##Subject: Re: number format test
##From: MURAKAMI Shinyu <murakami@nadita.com>
##Date: Thu, 3 Aug 2000 01:18:10 +0900 (Wed 10:18 MDT)

##Kay Michael <Michael.Kay@icl.com> wrote:
##>> 5. Saxon
##>>   - Fullwidth 1 (#xff11) are supported.
##>>   - Hiragana/Katakana/Kanji format generates incorrect result.
##>>     (Unicode codepoint order, such as #x3042, #x3043, #x3044,...)
##>>     useless and trouble with Non-European style processing.
##>>     fix it please!!
##>
##>If you could tell me what the correct sequence is, I'll be happy to include
##>it. Help me please!


##XSLT 1.0 spec says:

##    7.7.1 Number to String Conversion Attributes
##    ...

##    - Any other format token indicates a numbering sequence that starts
##      with that token.  If an implementation does not support a numbering
##      sequence that starts with that token, it must use a format token of 1.

##The last sentence is important.  ...it must use a format token of 1.

##If Saxon will support... the following are Japanese Hiragana/Katakana sequences
##-- modern(A...) and traditional(I...) -- and Kanji(CJK ideographs) numbers.

##format="&#x3042;" (Hiragana A)
##&#x3042;&#x3044;&#x3046;&#x3048;&#x304a;&#x304b;&#x304d;&#x304f;&#x3051;&#x3053;
##&#x3055;&#x3057;&#x3059;&#x305b;&#x305d;&#x305f;&#x3061;&#x3064;&#x3066;&#x3068;
##&#x306a;&#x306b;&#x306c;&#x306d;&#x306e;&#x306f;&#x3072;&#x3075;&#x3078;&#x307b;
##&#x307e;&#x307f;&#x3080;&#x3081;&#x3082;&#x3084;&#x3086;&#x3088;&#x3089;&#x308a;
##&#x308b;&#x308c;&#x308d;&#x308f;&#x3092;&#x3093;

##format="&#x30a2;" (Katakana A)
##&#x30a2;&#x30a4;&#x30a6;&#x30a8;&#x30aa;&#x30ab;&#x30ad;&#x30af;&#x30b1;&#x30b3;
##&#x30b5;&#x30b7;&#x30b9;&#x30bb;&#x30bd;&#x30bf;&#x30c1;&#x30c4;&#x30c6;&#x30c8;
##&#x30ca;&#x30cb;&#x30cc;&#x30cd;&#x30ce;&#x30cf;&#x30d2;&#x30d5;&#x30d8;&#x30db;
##&#x30de;&#x30df;&#x30e0;&#x30e1;&#x30e2;&#x30e4;&#x30e6;&#x30e8;&#x30e9;&#x30ea;
##&#x30eb;&#x30ec;&#x30ed;&#x30ef;&#x30f2;&#x30f3;

##format="&#x3044;" (Hiragana I)
##&#x3044;&#x308d;&#x306f;&#x306b;&#x307b;&#x3078;&#x3068;&#x3061;&#x308a;&#x306c;
##&#x308b;&#x3092;&#x308f;&#x304b;&#x3088;&#x305f;&#x308c;&#x305d;&#x3064;&#x306d;
##&#x306a;&#x3089;&#x3080;&#x3046;&#x3090;&#x306e;&#x304a;&#x304f;&#x3084;&#x307e;
##&#x3051;&#x3075;&#x3053;&#x3048;&#x3066;&#x3042;&#x3055;&#x304d;&#x3086;&#x3081;
##&#x307f;&#x3057;&#x3091;&#x3072;&#x3082;&#x305b;&#x3059;

##format="&#x30a4;" (Katakana I)
##&#x30a4;&#x30ed;&#x30cf;&#x30cb;&#x30db;&#x30d8;&#x30c8;&#x30c1;&#x30ea;&#x30cc;
##&#x30eb;&#x30f2;&#x30ef;&#x30ab;&#x30e8;&#x30bf;&#x30ec;&#x30bd;&#x30c4;&#x30cd;
##&#x30ca;&#x30e9;&#x30e0;&#x30a6;&#x30f0;&#x30ce;&#x30aa;&#x30af;&#x30e4;&#x30de;
##&#x30b1;&#x30d5;&#x30b3;&#x30a8;&#x30c6;&#x30a2;&#x30b5;&#x30ad;&#x30e6;&#x30e1;
##&#x30df;&#x30b7;&#x30f1;&#x30d2;&#x30e2;&#x30bb;&#x30b9;

##format="&#x4e00;" (Kanji 1) (decimal notation)
##&#x4e00;(=1) &#x4e8c;(=2) &#x4e09;(=3) &#x56db;(=4) &#x4e94;(=5)
##&#x516d;(=6) &#x4e03;(=7) &#x516b;(=8) &#x4e5d;(=9) &#x3007;(=0)
##e.g. &#x4e00;&#x3007;(=10)  &#x4e8c;&#x4e94;&#x516d;(=256)
##There are more ideographic(kanji)-number formats, but the above will be sufficient.


##Thanks,
##MURAKAMI Shinyu
##murakami@nadita.com


