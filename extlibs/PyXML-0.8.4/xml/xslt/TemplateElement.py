########################################################################
#
# File Name:   TemplateElement.py
#
#
"""
Implementation of the XSLT Spec template stylesheet element.
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import re, string
from xml.dom import EMPTY_NAMESPACE
import xml.dom.ext
import xml.dom.Element
import xml.xslt
from xml.xpath.Util import ExpandQName
from xml.xslt import XsltElement, XsltException, XPatternParser, Error, XSL_NAMESPACE
from xml.xpath import Util

#FIXME: We don't handle the priority rules rightly for templates with matches of the form a|b|c.  see spec 5.5

class TemplateElement(XsltElement):
    legalAttrs = ('match', 'mode', 'priority', 'name')

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE, localName='template', prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)


    def setup(self):
        self.__dict__['_nss'] = xml.dom.ext.GetAllNs(self)
        self.__dict__['_match'] = self.getAttributeNS(EMPTY_NAMESPACE, 'match')
        mode_attr = self.getAttributeNS(EMPTY_NAMESPACE, 'mode')
        if not mode_attr:
            self.__dict__['_mode'] = None
        else:
            split_name = Util.ExpandQName(
                mode_attr,
                namespaces=self._nss
                )
            self.__dict__['_mode'] = split_name
        name_attr = self.getAttributeNS(EMPTY_NAMESPACE, 'name')
        split_name = Util.ExpandQName(
            name_attr,
            namespaces=self._nss
            )
        self.__dict__['_name'] = split_name

        self.__dict__['_params'] = []
        self.__dict__['_elements'] = []
        for child in self.childNodes:
            if child.namespaceURI == XSL_NAMESPACE:
                if child.localName == 'param':
                    self.__dict__['_params'].append(child)
                elif child.localName in ['choose', 'if']:
                    self.__dict__['_elements'].append((1, child))
                else:
                    self.__dict__['_elements'].append((0, child))
            else:
                self.__dict__['_elements'].append((0, child))

        #A list of tuples
        #(pattern,qmatch,priority)
        #either pattern or qmatch will be present but not both
        self.__dict__['_patternInfo'] = []

        if self._match:
            priority = self.getAttributeNS(EMPTY_NAMESPACE, 'priority') or None
            if priority is not None:
                try:
                    priority = float(priority)
                except:
                    raise XsltException(Error.ILLEGAL_TEMPLATE_PRIORITY)
            parser = XPatternParser.XPatternParser()
            shortcuts = parser.parsePattern(self._match).getMatchShortcuts()
            for pattern, (shortcut, extra_arg) in shortcuts:
                if priority is None:
                    tpl_priority = pattern.priority
                else:
                    tpl_priority = priority
                self.__dict__['_patternInfo'].append((shortcut,
                                                      extra_arg,
                                                      tpl_priority))
        
    def getMatchInfo(self):
        return (self._patternInfo,self._mode,self._nss)

    def instantiate(self, context, processor, params=None, new_level=1):

        params = params or {}

        #NOTE Don't reset the context
        context.setNamespaces(self._nss)

        origVars = context.varBindings.copy()

        # Set the parameter list
        for param in self._params:
            value = params.get(param._name)
            if value is not None:
                context.varBindings[param._name] = value
            else:
                context = param.instantiate(context, processor)[0]

        rec_tpl_params = None
        for (recurse,child) in self._elements:
            if recurse:
                context, rec_tpl_params = child.instantiate(context,
                                                            processor,
                                                            new_level)
            else:
                context = child.instantiate(context, processor)[0]

        context.varBindings = origVars
        return (context, rec_tpl_params)

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         new_state = (base_state, self._nss, self._name, self._mode,
                      self._patternInfo, self._match, self._params,
                      self._elements)
         return new_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state[0])
        self._nss = state[1]
        self._name = state[2]
        self._mode = state[3]
        self._patternInfo = state[4]
        self._match = state[5]
        self._params = state[6]
        self._elements = state[7]
        return

    def mergeUnbalancedPipes(self, patterns):
        ctr = 0
        while ctr < len(patterns)-1:
            if string.count(patterns[ctr],'[') != string.count(patterns[ctr], ']'):
                patterns[ctr] = patterns[ctr] + '|' +patterns[ctr+1]
            else:
                ctr = ctr + 1
        patterns = map(lambda x:string.strip(x), patterns)
        return patterns
