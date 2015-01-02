########################################################################
#
# File Name:            Stylesheet.py
#
#
"""
Implement all the stylesheet internals
WWW: http://4suite.com/4XSLT        e-mail: support@4suite.com

Copyright (c) 1999-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""

import string, types
from xml.dom import EMPTY_NAMESPACE
import xml.dom.ext
from xml import xpath, xslt
from xml.dom import Node
from xml.dom.NodeFilter import NodeFilter
from xml.xslt import XsltElement, XsltException, InternalException, Error
from xml.xslt import XPatternParser, XsltContext
from xml.xslt import XSL_NAMESPACE, OutputParameters, ReleaseNode
from xml.xpath import CoreFunctions, Util, XPathParser, Conversions


class PatternInfo:
    """Indexes into the tuple for pattern information"""
    PATTERN = 0
    AXIS_TYPE = 1
    PRIORITY = 2
    MODE = 3
    NSS = 4
    TEMPLATE = 5

SPECIAL_RE_CHARS = ['.', '^', '$', '*', '+', '?']


def MatchTree(patterns, context):
    '''Select all nodes from node on down that match the pattern'''
    matched = map(lambda x, c=context, n=context.node: [n]*x.match(c,n),
                  patterns)
    counter = 1
    size = len(context.node.childNodes)
    origState = context.copyNodePosSize()
    for child in context.node.childNodes:
        context.setNodePosSize((child, counter, size))
        map(lambda x, y: x.extend(y), matched, MatchTree(patterns, context))
        context.setNodePosSize(origState)
        counter = counter + 1
    if context.node.nodeType == Node.ELEMENT_NODE:
        counter = 1
        size = len(context.node.attributes)
        for attr in context.node.attributes.values():
            context.setNodePosSize((attr, counter, size))
            map(lambda x, y: x.extend(y),
                matched, MatchTree(patterns, context))
            context.setNodePosSize(origState)
            counter = counter + 1
    return matched


class StylesheetElement(XsltElement):
    legalAttrs = ('id', 'extension-element-prefixes',
                  'exclude-result-prefixes', 'version')

    def __init__(self, doc, uri=xml.xslt.XSL_NAMESPACE, localName='stylesheet',
                 prefix='xsl', baseUri=''):
        XsltElement.__init__(self, doc, uri, localName, prefix, baseUri)
        self._imports = []
        self.extensionNss = []
        self._primedContext = None
        self._lres = []
        return

    def _updateKeys(self, doc, processor):
        context = XsltContext.XsltContext(doc, 1, 1,
                                          processorNss=self.namespaces,
                                          processor=processor)
        patterns = map(lambda x: x[1], self._kelems)
        if not patterns:
            return
        match_lists = MatchTree(patterns, context)
        ctr = 0
        for (name, match_pattern, use_expr) in self._kelems:
            match_list = match_lists[ctr]
            if not self.keys.has_key(name):
                self.keys[name] = {}
            for node in match_list:
                context.stylesheet = self
                origState = context.copy()
                context.node = node
                key_value_list = use_expr.evaluate(context)
                #NOTE: use attrs can't contain var refs, so result can't
                #be RTF So use CoreFunc StringValue, not ExtFunc version
                if type(key_value_list) != type([]):
                    key_value_list = [key_value_list]
                for obj in key_value_list:
                    keystr = Conversions.StringValue(obj)
                    if not self.keys[name].has_key(keystr):
                        self.keys[name][keystr] = []
                    self.keys[name][keystr].append(node)
                context.set(origState)
            ctr = ctr + 1
        context.release()
        return

    def setup(self):
        '''
        Called only once, at the first initialization
        '''
        self.namespaces = xml.dom.ext.GetAllNs(self)
        self.spaceRules = {}
        self._topLevelVarNodes = {}
        self.namespaceAliases = ({}, {})
        self.decimalFormats = {'': ('.', ',', 'Infinity', '-', 'NaN', '%', '?', '0', '#', ';')}
        self.keys = {}
        self.outputParams = OutputParameters()
        excluded_prefixes = self.getAttributeNS(EMPTY_NAMESPACE, 'exclude-result-prefixes')
        self.excludedNss = []
        if excluded_prefixes:
            excluded_prefixes = string.splitfields(excluded_prefixes)
            for prefix in excluded_prefixes:
                if prefix == '#default': prefix = ''
                self.excludedNss.append(self.namespaces[prefix])
        self._setupNamespaceAliases()
        self._setupChildNodes()
        self._setupDecimalFormats()
        self._setupWhitespaceRules()
        self._setupOutput()
        self._setupTemplates()
        self._setupKeys()
        self._setupTopLevelVarParams()
        return

    def _setupNamespaceAliases(self):
        #Namespace aliases
        ns_aliases = filter(lambda x: x.nodeType == Node.ELEMENT_NODE and (x.namespaceURI, x.localName) == (XSL_NAMESPACE, 'namespace-alias'), self.childNodes)
        for nsa in ns_aliases:
            stylesheet_prefix = nsa.getAttributeNS(EMPTY_NAMESPACE, 'stylesheet-prefix')
            result_prefix = nsa.getAttributeNS(EMPTY_NAMESPACE, 'result-prefix')
            if not (stylesheet_prefix and result_prefix):
                raise XsltException(Error.INVALID_NAMESPACE_ALIAS)
            if stylesheet_prefix == '#default':
                stylesheet_prefix == ''
            if result_prefix == '#default':
                result_prefix == ''
            sty_ns = self.namespaces[stylesheet_prefix]
            res_ns = self.namespaces[result_prefix]
            self.namespaceAliases[0][stylesheet_prefix] = result_prefix
            self.namespaceAliases[1][sty_ns] = res_ns
        return

    def _setupChildNodes(self):
        snit = self.ownerDocument.createNodeIterator(self, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT, None,0)
        curr_node = snit.nextNode()
        curr_node = snit.nextNode()
        while curr_node:
            try:
                curr_node.setup()
            except (xpath.SyntaxException, xpath.InternalException, xslt.SyntaxException, xslt.InternalException), e:
                #import traceback
                #traceback.print_exc(1000)
                if not hasattr(e, 'stylesheetUri'):
                    e.stylesheetUri = curr_node.baseUri
                raise e
            curr_node = snit.nextNode()
        return

    def _setupDecimalFormats(self):
        dec_formats = filter(lambda x: x.nodeType == Node.ELEMENT_NODE and (x.namespaceURI, x.localName) == (XSL_NAMESPACE, 'decimal-format'), self.childNodes)
        for dc in dec_formats:
            format_settings = (
                (dc.getAttributeNS(EMPTY_NAMESPACE, 'decimal-separator') or '.'),
                (dc.getAttributeNS(EMPTY_NAMESPACE, 'grouping-separator') or ','),
                (dc.getAttributeNS(EMPTY_NAMESPACE, 'infinity') or 'Infinity'),
                (dc.getAttributeNS(EMPTY_NAMESPACE, 'minus-sign') or '-'),
                (dc.getAttributeNS(EMPTY_NAMESPACE, 'NaN') or 'NaN'),
                (dc.getAttributeNS(EMPTY_NAMESPACE, 'percent') or '%'),
                (dc.getAttributeNS(EMPTY_NAMESPACE, 'per-mille') or '?'),
                (dc.getAttributeNS(EMPTY_NAMESPACE, 'zero-digit') or '0'),
                (dc.getAttributeNS(EMPTY_NAMESPACE, 'digit') or '#'),
                (dc.getAttributeNS(EMPTY_NAMESPACE, 'pattern-separator') or ';')
                )
            nfs = []
            for fc in format_settings:
                if fc in SPECIAL_RE_CHARS:
                    nfs.append('\\'+fc)
                else:
                    nfs.append(fc)
            name = dc.getAttributeNS(EMPTY_NAMESPACE, 'name')
            name = name and Util.ExpandQName(name, dc)
            self.decimalFormats[name] = tuple(nfs)
        return

    def _setupWhitespaceRules(self):
        #Whitespace rules
        space_rules = filter(lambda x: x.nodeType == Node.ELEMENT_NODE and (x.namespaceURI, x.localName) in [(XSL_NAMESPACE, 'preserve-space'), (XSL_NAMESPACE, 'strip-space')], self.childNodes)
        for sr in space_rules:
            args = string.splitfields(sr.getAttributeNS(EMPTY_NAMESPACE, 'elements'))
            for an_arg in args:
                #FIXME: watch out!  ExpandQName doesn't handle ns defaulting
                split_name = Util.ExpandQName(an_arg, sr)
                self.spaceRules[split_name] = string.splitfields(sr.localName, '-')[0]
        return

    def _setupOutput(self):
        #Output
        output = filter(lambda x: x.nodeType == Node.ELEMENT_NODE and (x.namespaceURI, x.localName) == (XSL_NAMESPACE, 'output'), self.childNodes)
        for out in output:
            method = out.getAttributeNS(EMPTY_NAMESPACE, 'method')
            if method: self.outputParams.method = method
            version = out.getAttributeNS(EMPTY_NAMESPACE, 'version')
            if version: self.outputParams.version = version
            encoding = out.getAttributeNS(EMPTY_NAMESPACE, 'encoding')
            if encoding: self.outputParams.encoding = encoding
            omit_xml_decl = out.getAttributeNS(EMPTY_NAMESPACE, 'omit-xml-declaration')
            if omit_xml_decl: self.outputParams.omitXmlDeclaration = omit_xml_decl
            standalone = out.getAttributeNS(EMPTY_NAMESPACE, 'standalone')
            if standalone: self.outputParams.standalone = standalone
            doctype_system = out.getAttributeNS(EMPTY_NAMESPACE, 'doctype-system')
            if doctype_system: self.outputParams.doctypeSystem = doctype_system
            doctype_public = out.getAttributeNS(EMPTY_NAMESPACE, 'doctype-public')
            if doctype_public: self.outputParams.doctypePublic = doctype_public
            media_type = out.getAttributeNS(EMPTY_NAMESPACE, 'media-type')
            if media_type: self.outputParams.mediaType = media_type
            #cdata_sec_elem = out.getAttributeNS(EMPTY_NAMESPACE, 'cdata-section-elements')
            self.outputParams.cdataSectionElements = []
            qnames = string.splitfields(out.getAttributeNS(EMPTY_NAMESPACE, 'cdata-section-elements'))
            for qname in qnames:
                self.outputParams.cdataSectionElements.append(Util.ExpandQName(qname, namespaces=self.namespaces))
            indent = out.getAttributeNS(EMPTY_NAMESPACE, 'indent')
            if indent: self.outputParams.indent = indent
        return

    def _setupTemplates(self):
        templates = filter(lambda x: x.nodeType == Node.ELEMENT_NODE and (x.namespaceURI, x.localName) == (XSL_NAMESPACE, 'template'), self.childNodes)

        #Preprocess all of the templates with names
        match_tpls = filter(lambda x: x._name != '', templates)
        self._call_templates = {}
        for m in match_tpls:
            if not self._call_templates.has_key(m._name):
                self._call_templates[m._name] = m

        #Preprocess the patterns from all templates
        patterns = []
        for tpl in templates:
            (patternInfo, mode, nss) = tpl.getMatchInfo()
            for pi in patternInfo:
                patterns.append(pi+(mode, nss, tpl))

        patterns.reverse()
        patterns.sort(lambda x, y:
                      cmp(y[PatternInfo.PRIORITY], x[PatternInfo.PRIORITY]))
        patternDict = {}
        for p in patterns:
            m = p[PatternInfo.MODE]
            if not patternDict.has_key(m):
                patternDict[m] = []
            patternDict[m].append(p)

        self._patterns = patternDict
        return

    def _setupKeys(self):
        self._kelems = []
        pattern_parser = XPatternParser.XPatternParser()
        path_parser = XPathParser.XPathParser()
        kelems = filter(lambda x: x.nodeType == Node.ELEMENT_NODE and (x.namespaceURI, x.localName) == (XSL_NAMESPACE, 'key'), self.childNodes)
        for kelem in kelems:
            name = Util.ExpandQName(kelem.getAttributeNS(EMPTY_NAMESPACE, 'name'), kelem)
            match = kelem.getAttributeNS(EMPTY_NAMESPACE, 'match')
            match_pattern = pattern_parser.parsePattern(match)
            use = kelem.getAttributeNS(EMPTY_NAMESPACE, 'use')
            use_expr = path_parser.parseExpression(use)
            self._kelems.append((name, match_pattern, use_expr))

        self.reset()
        return

    def _setupTopLevelVarParams(self):
        #Is there a more efficient way to zip two sequences into a dict?
        vars = filter(lambda x: x.nodeType == Node.ELEMENT_NODE and x.namespaceURI == XSL_NAMESPACE and x.localName == 'variable', self.childNodes)
        self._topVariables = {}
        for var in vars:
            #FIXME: First check multiple variable errors
            self._topVariables[var._name] = var
        params = filter(lambda x: x.nodeType == Node.ELEMENT_NODE and x.namespaceURI == XSL_NAMESPACE and x.localName == 'param', self.childNodes)
        for param in params:
            #FIXME: First check multiple variable errors
            self._topVariables[param._name] = param
        return

    def newSource(self, doc, processor):
        """
        Called whenever there's a new source document registed to the processor
        """
        self._updateKeys(doc, processor)
        return

    def reset(self):
        """
        Called whenever the processor is reset, i.e. after each run
        """
        self.keys = {}
        if self._primedContext:
            self._primedContext.release()
            self._primedContext = None
        return

    def _fixupAliases(self):
        for lre in self._lres:
            lre.fixupAliases()
        return

    def processImports(self, contextNode, processor, topLevelParams):
        #Import precedence rules can be taken care of by having parent
        self._imports = filter(lambda x: x.nodeType == Node.ELEMENT_NODE and (x.namespaceURI, x.localName) == (XSL_NAMESPACE, 'import'), self.childNodes)
        #Style-sheet dictionaries override imported values
        for imp in self._imports:
            imp.setup()
            #FIXME: Extension elements?

            imp.stylesheet = processor._styReader.fromUri(imp.href, baseUri=imp.baseUri)
            sheet = imp.stylesheet
            sheet.processImports(contextNode, processor, topLevelParams)
            sheet.prime(contextNode, processor, topLevelParams)
            self.spaceRules.update(sheet.spaceRules)
            self.namespaceAliases[0].update(sheet.namespaceAliases[0])
            self.namespaceAliases[1].update(sheet.namespaceAliases[1])
        self._fixupAliases()
        return

    def _computeVar(self, vname, context, processed, deferred,
                    overriddenParams, topLevelParams, processor):
        vnode = self._topVariables[vname]
        if vnode in deferred:
            raise XsltException(Error.CIRCULAR_VAR, vname[0], vname[1])
        if vnode in processed:
            return
        if vnode.localName[0] == 'p':
            if overriddenParams.has_key(vname):
                context.varBindings[vname] = overriddenParams[vname]
            else:
                try:
                    context = vnode.instantiate(context, processor)[0]
                except xpath.RuntimeException, e:
                    deferred.append(vnode)
                    self._computeVar((e.args[0], e.args[1]), context,
                                     processed, deferred, overriddenParams,
                                     topLevelParams, processor)
                    deferred.remove(vnode)
                    context = vnode.instantiate(context, processor)[0]
                #Set up so that later stylesheets will get overridden by
                #parameter values set in higher-priority stylesheets
                topLevelParams[vname] = context.varBindings[vname]
        else:
            try:
                context = vnode.instantiate(context, processor)[0]
            except xpath.RuntimeException, e:
                deferred.append(vnode)
                self._computeVar((e.args[0], e.args[1]), context,
                                 processed, deferred, overriddenParams,
                                 topLevelParams, processor)
                deferred.remove(vnode)
                context = vnode.instantiate(context, processor)[0]
        processed.append(vnode)
        return
    
    def prime(self, contextNode, processor, topLevelParams):
        self._primedContext = context = XsltContext.XsltContext(contextNode.ownerDocument, 1, 1, processorNss=self.namespaces, stylesheet=self, processor=processor)
        self._docReader = processor._docReader

        #Attribute sets
        attribute_sets = filter(lambda x: x.nodeType == Node.ELEMENT_NODE and (x.namespaceURI, x.localName) == (XSL_NAMESPACE, 'attribute-set'), self.childNodes)
        for as in attribute_sets:
            as.instantiate(context, processor)
        overridden_params = {}
        for k in topLevelParams.keys():
            if type(k) != types.TupleType:
                try:
                    split_name = Util.ExpandQName(k, namespaces=context.processorNss)
                except KeyError:
                    continue
            else:
                split_name = k
            overridden_params[split_name] = topLevelParams[k]
        for vname in self._topVariables.keys():
            self._computeVar(vname, context, [], [], overridden_params,
                             topLevelParams, processor)
        self._primedContext = context
        #Note: key expressions can't have var refs, so we needn't worry about imports
        self._updateKeys(contextNode, processor)
        for imp in self._imports:
            self._primedContext.varBindings.update(imp.stylesheet._primedContext.varBindings)
        return topLevelParams


    ########################## Run-time methods ########################
    
    def getNamedTemplates(self):
        templates = {}
        for name,tpl in self._call_templates.items():
            templates[name] = (self, tpl)

        for imported in self._imports:
            imp_tpl = imported.stylesheet.getNamedTemplates()
            for name, (sty, tpl) in imp_tpl.items():
                if not templates.has_key(name):
                    templates[name] = (sty, tpl)
        return templates

    def getTopLevelVariables(self):
        return self._primedContext.varBindings.copy()

    def applyTemplates(self, context, mode, processor, params=None):
        params = params or {}
        origState = context.copyStylesheet()
        context.setStylesheet((self._primedContext.varBindings,self.namespaces, self))
        #Set the current node for this template application
        context.currentNode = context.node

        matched = 1
        for patternInfo in self._patterns.get(mode,[]):
            context.processorNss = patternInfo[PatternInfo.NSS]
            pattern = patternInfo[PatternInfo.PATTERN]
            if pattern.match(context, context.node, patternInfo[PatternInfo.AXIS_TYPE]):
                patternInfo[PatternInfo.TEMPLATE].instantiate(context, processor, params)
                break
        else:
            for imported in self._imports:
                if imported.stylesheet.applyTemplates(context, mode,
                                                      processor, params):
                    break
            else:
                matched = 0

        context.setStylesheet(origState)
        return matched

    def applyImports(self, context, mode, processor, params=None):
        params = params or {}
        for imp in self._imports:
            matched = imp.stylesheet.applyTemplates(context, mode, processor, params)
            if matched: return 1
        return 0

    def callTemplate(self, processor, name, context, params, new_level=1):
        vars = self._primedContext.varBindings.copy()
        vars.update(params)

        origState = context.copyStylesheet()
        context.setStylesheet((vars, self.namespaces, self))
        
        matched = 0
        rec_tpl_params = None

        tpl = self._call_templates.get(name)

        if tpl:
            rec_tpl_params = tpl.instantiate(context, processor, params, new_level)[1]
        else:
            for child in self._imports:
                (matched, rec_tpl_params) = child.stylesheet.callTemplate(processor, name, context, params, new_level)
                if matched: break

        context.setStylesheet(origState)
        
        return (matched, rec_tpl_params)

    def reclaim(self):
        self.__dict__['_primedContext'] = None
        for imp in self._imports:
            imp.stylesheet.reclaim()
            ReleaseNode(imp.stylesheet.ownerDocument)
        self.namespaces = xml.dom.ext.GetAllNs(self)
        self.spaceRules = {}
        self.namespaceAliases = ({}, {})
        self.decimalFormats = {'': ('.', ',', 'Infinity', '-', 'NaN', '%', '?', '0', '#', ';')}
        self.keys = {}
        self.outputParams = OutputParameters()
        excluded_prefixes = self.getAttributeNS(EMPTY_NAMESPACE, 'exclude-result-prefixes')
        self.excludedNss = []
        self._lres = []
        return

    def __getinitargs__(self):
        return (None, self.namespaceURI, self.localName, self.prefix,
                self.baseUri)

    def __getstate__(self):
         base_state = XsltElement.__getstate__(self)
         new_state = (base_state, self.namespaces, self.spaceRules,
                      self.namespaceAliases, self.decimalFormats,
                      self.keys, self.outputParams, self.excludedNss,
                      self._patterns, self._call_templates, self._kelems, self.extensionNss,
                      self._topVariables)
         return new_state

    def __setstate__(self, state):
        XsltElement.__setstate__(self, state[0])
        self.namespaces = state[1]
        self.spaceRules = state[2]
        self.namespaceAliases = state[3]
        self.decimalFormats = state[4]
        self.keys = state[5]
        self.outputParams = state[6]
        self.excludedNss = state[7]
        self._patterns = state[8]
        self._call_templates = state[9]
        self._kelems = state[10]
        self.extensionNss = state[11]
        self._topVariables = state[12]
        return

