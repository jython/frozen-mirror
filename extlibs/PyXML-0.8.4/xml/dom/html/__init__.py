HTML_4_STRICT_INLINE = ['TT', 'I', 'B', 'BIG', 'SMALL', 'EM', 'STRONG', 'DFN', 'CODE', 'SAMP', 'KBD', 'VAR', 'CITE', 'ABBR', 'ACRONYM', 'A', 'IMG', 'OBJECT', 'SCRIPT', 'MAP', 'Q', 'SUB', 'SUP' 'SPAN', 'BDO', 'INPUT', 'SELECT', 'TEXTAREA', 'LABEL', 'BUTTON']

HTML_4_TRANSITIONAL_INLINE = ['TT', 'I', 'B', 'U', 'S', 'STRIKE', 'BIG', 'SMALL', 'EM', 'STRONG', 'DFN', 'CODE', 'SAMP', 'KBD', 'VAR', 'CITE', 'ABBR', 'ACRONYM', 'A', 'IMG', 'APPLET', 'OBJECT', 'FONT', 'BASEFONT', 'SCRIPT', 'MAP', 'Q', 'SUB', 'SUP', 'SPAN', 'BDO', 'IFRAME', 'INPUT', 'SELECT', 'TEXTAREA', 'LABEL', 'BUTTON']

HTML_FORBIDDEN_END = ['AREA', 'BASE', 'BASEFONT', 'BR', 'COL', 'FRAME', 'HR', 'IMG', 'INPUT', 'ISINDEX', 'LINK', 'META', 'PARAM']

HTML_OPT_END = ['BODY', 'COLGROUP', 'DD', 'DT', 'HEAD', 'HTML', 'LI', 'OPTION', 'P', 'TBODY', 'TD', 'TFOOT', 'TH', 'THEAD', 'TR']

#FIXME: map attrs to the tags that use them
HTML_BOOLEAN_ATTRS = ['CHECKED', 'COMPACT', 'DECLARE', 'DEFER', 'DISABLED', 'ISMAP', 'MULTIPLE', 'NOHREF', 'NORESIZE', 'NOSHADE', 'NOWRAP', 'READONLY', 'SELECTED']

HTML_CHARACTER_ENTITIES = {
    # Sect 24.2 -- ISO 8859-1
    160: 'nbsp',
    161: 'iexcl',
    162: 'cent',
    163: 'pound',
    164: 'curren',
    165: 'yen',
    166: 'brvbar',
    167: 'sect',
    168: 'uml',
    169: 'copy',
    170: 'ordf',
    171: 'laquo',
    172: 'not',
    173: 'shy',
    174: 'reg',
    175: 'macr',
    176: 'deg',
    177: 'plusmn',
    178: 'sup2',
    179: 'sup3',
    180: 'acute',
    181: 'micro',
    182: 'para',
    183: 'middot',
    184: 'cedil',
    185: 'sup1',
    186: 'ordm',
    187: 'raquo',
    188: 'frac14',
    189: 'frac12',
    190: 'frac34',
    191: 'iquest',
    192: 'Agrave',
    193: 'Aacute',
    194: 'Acirc',
    195: 'Atilde',
    196: 'Auml',
    197: 'Aring',
    198: 'AElig',
    199: 'Ccedil',
    200: 'Egrave',
    201: 'Eacute',
    202: 'Ecirc',
    203: 'Euml',
    204: 'Igrave',
    205: 'Iacute',
    206: 'Icirc',
    207: 'Iuml',
    208: 'ETH',
    209: 'Ntilde',
    210: 'Ograve',
    211: 'Oacute',
    212: 'Ocirc',
    213: 'Otilde',
    214: 'Ouml',
    215: 'times',
    216: 'Oslash',
    217: 'Ugrave',
    218: 'Uacute',
    219: 'Ucirc',
    220: 'Uuml',
    221: 'Yacute',
    222: 'THORN',
    223: 'szlig',
    224: 'agrave',
    225: 'aacute',
    226: 'acirc',
    227: 'atilde',
    228: 'auml',
    229: 'aring',
    230: 'aelig',
    231: 'ccedil',
    232: 'egrave',
    233: 'eacute',
    234: 'ecirc',
    235: 'euml',
    236: 'igrave',
    237: 'iacute',
    238: 'icirc',
    239: 'iuml',
    240: 'eth',
    241: 'ntilde',
    242: 'ograve',
    243: 'oacute',
    244: 'ocirc',
    245: 'otilde',
    246: 'ouml',
    247: 'divide',
    248: 'oslash',
    249: 'ugrave',
    250: 'uacute',
    251: 'ucirc',
    252: 'uuml',
    253: 'yacute',
    254: 'thorn',
    255: 'yuml',

    # Sect 24.3 -- Symbols, Mathematical Symbols, and Greek Letters
    # Latin Extended-B
    402: 'fnof',
    # Greek
    913: 'Alpha',
    914: 'Beta',
    915: 'Gamma',
    916: 'Delta',
    917: 'Epsilon',
    918: 'Zeta',
    919: 'Eta',
    920: 'Theta',
    921: 'Iota',
    922: 'Kappa',
    923: 'Lambda',
    924: 'Mu',
    925: 'Nu',
    926: 'Xi',
    927: 'Omicron',
    928: 'Pi',
    929: 'Rho',
    931: 'Sigma',
    932: 'Tau',
    933: 'Upsilon',
    934: 'Phi',
    935: 'Chi',
    936: 'Psi',
    937: 'Omega',
    945: 'alpha',
    946: 'beta',
    947: 'gamma',
    948: 'delta',
    949: 'epsilon',
    950: 'zeta',
    951: 'eta',
    952: 'theta',
    953: 'iota',
    954: 'kappa',
    955: 'lambda',
    956: 'mu',
    957: 'nu',
    958: 'xi',
    959: 'omicron',
    960: 'pi',
    961: 'rho',
    962: 'sigmaf',
    963: 'sigma',
    964: 'tau',
    965: 'upsilon',
    966: 'phi',
    967: 'chi',
    968: 'psi',
    969: 'omega',
    977: 'thetasym',
    978: 'upsih',
    982: 'piv',
    # General Punctuation
    8226: 'bull',      # bullet
    8230: 'hellip',    # horizontal ellipsis
    8242: 'prime',     # prime (minutes/feet)
    8243: 'Prime',     # double prime (seconds/inches)
    8254: 'oline',     # overline (spacing overscore)
    8250: 'frasl',     # fractional slash
    # Letterlike Symbols
    8472: 'weierp',    # script capital P (power set/Weierstrass p)
    8465: 'image',     # blackletter capital I (imaginary part)
    8476: 'real',      # blackletter capital R (real part)
    8482: 'trade',     # trademark
    8501: 'alefsym',   # alef symbol (first transfinite cardinal)
    # Arrows
    8592: 'larr',      # leftwards arrow
    8593: 'uarr',      # upwards arrow
    8594: 'rarr',      # rightwards arrow
    8595: 'darr',      # downwards arrow
    8596: 'harr',      # left right arrow
    8629: 'crarr',     # downwards arrow with corner leftwards (carriage return)
    8656: 'lArr',      # leftwards double arrow
    8657: 'uArr',      # upwards double arrow
    8658: 'rArr',      # rightwards double arrow
    8659: 'dArr',      # downwards double arrow
    8660: 'hArr',      # left right double arrow
    # Mathematical Operators
    8704: 'forall',    # for all
    8706: 'part',      # partial differential
    8707: 'exist',     # there exists
    8709: 'empty',     # empty set, null set, diameter
    8711: 'nabla',     # nabla, backward difference
    8712: 'isin',      # element of
    8713: 'notin',     # not an element of
    8715: 'ni',        # contains as member
    8719: 'prod',      # n-ary product, product sign
    8721: 'sum',       # n-ary sumation
    8722: 'minus',     # minus sign
    8727: 'lowast',    # asterisk operator
    8730: 'radic',     # square root, radical sign
    8733: 'prop',      # proportional to
    8734: 'infin',     # infinity
    8736: 'ang',       # angle
    8743: 'and',       # logical and, wedge
    8744: 'or',        # logical or, vee
    8745: 'cap',       # intersection, cap
    8746: 'cup',       # union, cup
    8747: 'int',       # integral
    8756: 'there4',    # therefore
    8764: 'sim',       # tilde operator, varies with, similar to
    8773: 'cong',      # approximately equal to
    8776: 'asymp',     # almost equal to, asymptotic to
    8800: 'ne',        # not equal to
    8801: 'equiv',     # identical to
    8804: 'le',        # less-than or equal to
    8805: 'ge',        # greater-than or equal to
    8834: 'sub',       # subset of
    8835: 'sup',       # superset of
    8836: 'nsub',      # not subset of
    8838: 'sube',      # subset of or equal to
    8839: 'supe',      # superset of or equal to
    8853: 'oplus',     # circled plus, direct sum
    8855: 'otimes',    # circled times, vector product
    8869: 'perp',      # up tack, orthogonal to, perpendicular
    8901: 'sdot',      # dot operator
    8968: 'lceil',     # left ceiling, apl upstile
    8969: 'rceil',     # right ceiling
    8970: 'lfloor',    # left floor, apl downstile
    8971: 'rfloor',    # right floor
    9001: 'lang',      # left-pointing angle bracket, bra
    9002: 'rang',      # right-pointing angle bracket, ket
    9674: 'loz',       # lozenge
    # Miscellaneous Symbols
    9824: 'spades',
    9827: 'clubs',
    9829: 'hearts',
    9830: 'diams',

    # Sect 24.4 -- Markup Significant and Internationalization
    # Latin Extended-A
    338: 'OElig',      # capital ligature OE
    339: 'oelig',      # small ligature oe
    352: 'Scaron',     # capital S with caron
    353: 'scaron',     # small s with caron
    376: 'Yuml',       # capital Y with diaeresis
    # Spacing Modifier Letters
    710: 'circ',       # circumflexx accent
    732: 'tidle',      # small tilde
    # General Punctuation
    8194: 'ensp',      # en space
    8195: 'emsp',      # em space
    8201: 'thinsp',    # thin space
    8204: 'zwnj',      # zero-width non-joiner
    8205: 'zwj',       # zero-width joiner
    8206: 'lrm',       # left-to-right mark
    8207: 'rlm',       # right-to-left mark
    8211: 'ndash',     # en dash
    8212: 'mdash',     # em dash
    8216: 'lsquo',     # left single quotation mark
    8217: 'rsquo',     # right single quotation mark
    8218: 'sbquo',     # single low-9 quotation mark
    8220: 'ldquo',     # left double quotation mark
    8221: 'rdquo',     # right double quotation mark
    8222: 'bdquo',     # double low-9 quotation mark
    8224: 'dagger',    # dagger
    8225: 'Dagger',    # double dagger
    8240: 'permil',    # per mille sign
    8249: 'lsaquo',    # single left-pointing angle quotation mark
    8250: 'rsaquo',    # single right-pointing angle quotation mark
    8364: 'euro',      # euro sign
    }

HTML_NAME_ALLOWED = ['A',
                     'APPLET',
                     'BUTTON',
                     'FORM',
                     'FRAME',
                     'IFRAME',
                     'IMG',
                     'INPUT',
                     'MAP',
                     'META',
                     'OBJECT',
                     'PARAM',
                     'SELECT',
                     'TEXTAREA']

# xhtml DTD

HTML_DTD = {
    'col': [],
    'u': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'p': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'caption': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'q': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'i': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'textarea': ['#PCDATA'],
    'center': ['#PCDATA', 'a', 'abbr', 'acronym', 'address', 'applet', 'b', 'basefont', 'bdo', 'big', 'blockquote', 'br', 'button', 'center', 'cite', 'code', 'del', 'dfn', 'dir', 'div', 'dl', 'em', 'fieldset', 'font', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'iframe', 'img', 'input', 'ins', 'isindex', 'kbd', 'label', 'map', 'menu', 'noframes', 'noscript', 'object', 'ol', 'p', 'pre', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'table', 'textarea', 'tt', 'u', 'ul', 'var'],
    'script': ['#PCDATA'],
    'ol': ['li'],
    'a': ['#PCDATA', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'legend': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'strong': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'address': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'br': [],
    'base': [],
    'object': ['#PCDATA', 'a', 'abbr', 'acronym', 'address', 'applet', 'b', 'basefont', 'bdo', 'big', 'blockquote', 'br', 'button', 'center', 'cite', 'code', 'del', 'dfn', 'dir', 'div', 'dl', 'em', 'fieldset', 'font', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'iframe', 'img', 'input', 'ins', 'isindex', 'kbd', 'label', 'map', 'menu', 'noframes', 'noscript', 'object', 'ol', 'p', 'param', 'pre', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'table', 'textarea', 'tt', 'u', 'ul', 'var'],
    'basefont': [],
    'map': ['address', 'area', 'blockquote', 'center', 'del', 'dir', 'div', 'dl', 'fieldset', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'ins', 'isindex', 'menu', 'noframes', 'noscript', 'ol', 'p', 'pre', 'script', 'table', 'ul'],
    'body': ['#PCDATA', 'a', 'abbr', 'acronym', 'address', 'applet', 'b', 'basefont', 'bdo', 'big', 'blockquote', 'br', 'button', 'center', 'cite', 'code', 'del', 'dfn', 'dir', 'div', 'dl', 'em', 'fieldset', 'font', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'iframe', 'img', 'input', 'ins', 'isindex', 'kbd', 'label', 'map', 'menu', 'noframes', 'noscript', 'object', 'ol', 'p', 'pre', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'table', 'textarea', 'tt', 'u', 'ul', 'var'],
    'samp': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'dl': ['dd', 'dt'],
    'acronym': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'html': ['body', 'frameset', 'head'],
    'em': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'label': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'tbody': ['tr'],
    'bdo': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'sub': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'meta': [],
    'ins': ['#PCDATA', 'a', 'abbr', 'acronym', 'address', 'applet', 'b', 'basefont', 'bdo', 'big', 'blockquote', 'br', 'button', 'center', 'cite', 'code', 'del', 'dfn', 'dir', 'div', 'dl', 'em', 'fieldset', 'font', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'iframe', 'img', 'input', 'ins', 'isindex', 'kbd', 'label', 'map', 'menu', 'noframes', 'noscript', 'object', 'ol', 'p', 'pre', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'table', 'textarea', 'tt', 'u', 'ul', 'var'],
    'frame': [],
    's': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'title': ['#PCDATA'],
    'frameset': ['frame', 'frameset', 'noframes'],
    'pre': ['#PCDATA', 'a', 'abbr', 'acronym', 'b', 'bdo', 'br', 'button', 'cite', 'code', 'dfn', 'em', 'i', 'input', 'kbd', 'label', 'map', 'q', 's', 'samp', 'select', 'span', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'dir': ['li'],
    'div': ['#PCDATA', 'a', 'abbr', 'acronym', 'address', 'applet', 'b', 'basefont', 'bdo', 'big', 'blockquote', 'br', 'button', 'center', 'cite', 'code', 'del', 'dfn', 'dir', 'div', 'dl', 'em', 'fieldset', 'font', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'iframe', 'img', 'input', 'ins', 'isindex', 'kbd', 'label', 'map', 'menu', 'noframes', 'noscript', 'object', 'ol', 'p', 'pre', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'table', 'textarea', 'tt', 'u', 'ul', 'var'],
    'small': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'iframe': ['#PCDATA', 'a', 'abbr', 'acronym', 'address', 'applet', 'b', 'basefont', 'bdo', 'big', 'blockquote', 'br', 'button', 'center', 'cite', 'code', 'del', 'dfn', 'dir', 'div', 'dl', 'em', 'fieldset', 'font', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'iframe', 'img', 'input', 'ins', 'isindex', 'kbd', 'label', 'map', 'menu', 'noframes', 'noscript', 'object', 'ol', 'p', 'pre', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'table', 'textarea', 'tt', 'u', 'ul', 'var'],
    'del': ['#PCDATA', 'a', 'abbr', 'acronym', 'address', 'applet', 'b', 'basefont', 'bdo', 'big', 'blockquote', 'br', 'button', 'center', 'cite', 'code', 'del', 'dfn', 'dir', 'div', 'dl', 'em', 'fieldset', 'font', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'iframe', 'img', 'input', 'ins', 'isindex', 'kbd', 'label', 'map', 'menu', 'noframes', 'noscript', 'object', 'ol', 'p', 'pre', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'table', 'textarea', 'tt', 'u', 'ul', 'var'],
    'applet': ['#PCDATA', 'a', 'abbr', 'acronym', 'address', 'applet', 'b', 'basefont', 'bdo', 'big', 'blockquote', 'br', 'button', 'center', 'cite', 'code', 'del', 'dfn', 'dir', 'div', 'dl', 'em', 'fieldset', 'font', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'iframe', 'img', 'input', 'ins', 'isindex', 'kbd', 'label', 'map', 'menu', 'noframes', 'noscript', 'object', 'ol', 'p', 'param', 'pre', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'table', 'textarea', 'tt', 'u', 'ul', 'var'],
    'ul': ['li'],
    'isindex': [],
    'button': ['#PCDATA', 'abbr', 'acronym', 'address', 'applet', 'b', 'basefont', 'bdo', 'big', 'blockquote', 'br', 'center', 'cite', 'code', 'del', 'dfn', 'dir', 'div', 'dl', 'em', 'font', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img', 'ins', 'kbd', 'map', 'menu', 'noframes', 'noscript', 'object', 'ol', 'p', 'pre', 'q', 's', 'samp', 'script', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'table', 'tt', 'u', 'ul', 'var'],
    'colgroup': ['col'],
    'b': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'table': ['caption', 'col', 'colgroup', 'tbody', 'tfoot', 'thead', 'tr'],
    'dt': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'optgroup': ['option'],
    'abbr': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'link': [],
    'h4': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'dd': ['#PCDATA', 'a', 'abbr', 'acronym', 'address', 'applet', 'b', 'basefont', 'bdo', 'big', 'blockquote', 'br', 'button', 'center', 'cite', 'code', 'del', 'dfn', 'dir', 'div', 'dl', 'em', 'fieldset', 'font', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'iframe', 'img', 'input', 'ins', 'isindex', 'kbd', 'label', 'map', 'menu', 'noframes', 'noscript', 'object', 'ol', 'p', 'pre', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'table', 'textarea', 'tt', 'u', 'ul', 'var'],
    'big': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'hr': [],
    'form': ['#PCDATA', 'a', 'abbr', 'acronym', 'address', 'applet', 'b', 'basefont', 'bdo', 'big', 'blockquote', 'br', 'button', 'center', 'cite', 'code', 'del', 'dfn', 'dir', 'div', 'dl', 'em', 'fieldset', 'font', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'iframe', 'img', 'input', 'ins', 'isindex', 'kbd', 'label', 'map', 'menu', 'noframes', 'noscript', 'object', 'ol', 'p', 'pre', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'table', 'textarea', 'tt', 'u', 'ul', 'var'],
    'option': ['#PCDATA'],
    'fieldset': ['#PCDATA', 'a', 'abbr', 'acronym', 'address', 'applet', 'b', 'basefont', 'bdo', 'big', 'blockquote', 'br', 'button', 'center', 'cite', 'code', 'del', 'dfn', 'dir', 'div', 'dl', 'em', 'fieldset', 'font', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'iframe', 'img', 'input', 'ins', 'isindex', 'kbd', 'label', 'legend', 'map', 'menu', 'noframes', 'noscript', 'object', 'ol', 'p', 'pre', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'table', 'textarea', 'tt', 'u', 'ul', 'var'],
    'blockquote': ['#PCDATA', 'a', 'abbr', 'acronym', 'address', 'applet', 'b', 'basefont', 'bdo', 'big', 'blockquote', 'br', 'button', 'center', 'cite', 'code', 'del', 'dfn', 'dir', 'div', 'dl', 'em', 'fieldset', 'font', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'iframe', 'img', 'input', 'ins', 'isindex', 'kbd', 'label', 'map', 'menu', 'noframes', 'noscript', 'object', 'ol', 'p', 'pre', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'table', 'textarea', 'tt', 'u', 'ul', 'var'],
    'head': ['base', 'isindex', 'link', 'meta', 'object', 'script', 'style', 'title'],
    'thead': ['tr'],
    'cite': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'td': ['#PCDATA', 'a', 'abbr', 'acronym', 'address', 'applet', 'b', 'basefont', 'bdo', 'big', 'blockquote', 'br', 'button', 'center', 'cite', 'code', 'del', 'dfn', 'dir', 'div', 'dl', 'em', 'fieldset', 'font', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'iframe', 'img', 'input', 'ins', 'isindex', 'kbd', 'label', 'map', 'menu', 'noframes', 'noscript', 'object', 'ol', 'p', 'pre', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'table', 'textarea', 'tt', 'u', 'ul', 'var'],
    'input': [],
    'var': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'th': ['#PCDATA', 'a', 'abbr', 'acronym', 'address', 'applet', 'b', 'basefont', 'bdo', 'big', 'blockquote', 'br', 'button', 'center', 'cite', 'code', 'del', 'dfn', 'dir', 'div', 'dl', 'em', 'fieldset', 'font', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'iframe', 'img', 'input', 'ins', 'isindex', 'kbd', 'label', 'map', 'menu', 'noframes', 'noscript', 'object', 'ol', 'p', 'pre', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'table', 'textarea', 'tt', 'u', 'ul', 'var'],
    'tfoot': ['tr'],
    'dfn': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'li': ['#PCDATA', 'a', 'abbr', 'acronym', 'address', 'applet', 'b', 'basefont', 'bdo', 'big', 'blockquote', 'br', 'button', 'center', 'cite', 'code', 'del', 'dfn', 'dir', 'div', 'dl', 'em', 'fieldset', 'font', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'iframe', 'img', 'input', 'ins', 'isindex', 'kbd', 'label', 'map', 'menu', 'noframes', 'noscript', 'object', 'ol', 'p', 'pre', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'table', 'textarea', 'tt', 'u', 'ul', 'var'],
    'param': [],
    'tr': ['td', 'th'],
    'tt': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'menu': ['li'],
    'area': [],
    'img': [],
    'span': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'style': [],
    'noscript': ['#PCDATA', 'a', 'abbr', 'acronym', 'address', 'applet', 'b', 'basefont', 'bdo', 'big', 'blockquote', 'br', 'button', 'center', 'cite', 'code', 'del', 'dfn', 'dir', 'div', 'dl', 'em', 'fieldset', 'font', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'iframe', 'img', 'input', 'ins', 'isindex', 'kbd', 'label', 'map', 'menu', 'noframes', 'noscript', 'object', 'ol', 'p', 'pre', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'table', 'textarea', 'tt', 'u', 'ul', 'var'],
    'noframes': ['#PCDATA', 'a', 'abbr', 'acronym', 'address', 'applet', 'b', 'basefont', 'bdo', 'big', 'blockquote', 'br', 'button', 'center', 'cite', 'code', 'del', 'dfn', 'dir', 'div', 'dl', 'em', 'fieldset', 'font', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'iframe', 'img', 'input', 'ins', 'isindex', 'kbd', 'label', 'map', 'menu', 'noframes', 'noscript', 'object', 'ol', 'p', 'pre', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'table', 'textarea', 'tt', 'u', 'ul', 'var'],
    'select': ['optgroup', 'option'],
    'font': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'strike': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'sup': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'h5': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'kbd': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'h6': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'h1': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'h3': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'h2': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var'],
    'code': ['#PCDATA', 'a', 'abbr', 'acronym', 'applet', 'b', 'basefont', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'map', 'noscript', 'object', 'q', 's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'textarea', 'tt', 'u', 'var']
    }

from xml.dom.html import HTMLDOMImplementation

htmlImplementation = HTMLDOMImplementation.HTMLDOMImplementation()


#FIXME: all of this can be made much more efficient.  Maybe when we leave Python 1.x behind
try:
    #The following stanza courtesy Martin von Loewis
    import codecs # Python 1.6+ only
    from types import UnicodeType
    def utf8_to_code(text, encoding):
        encoder = codecs.lookup(encoding)[0] # encode,decode,reader,writer
        if type(text) is not UnicodeType:
            text = unicode(text, "utf-8")
        return encoder(text)[0] # result,size

    def ConvertChar(m):
        return '&'+HTML_CHARACTER_ENTITIES[ord(m.group())]+';'

    def UseHtmlCharEntities(text):
        if type(text) is not UnicodeType:
            text = unicode(text, "utf-8")
        new_text, num_subst = re.subn(g_htmlUniCharEntityPattern, ConvertChar,
                                      text)
        return new_text

except ImportError:
    from xml.unicode.iso8859 import wstring
    wstring.install_alias('ISO-8859-1', 'ISO_8859-1:1987')

    def utf8_to_code(text, encoding):
        encoding = string.upper(encoding)
        if encoding == 'UTF-8':
            return text
        #Note: Pass through to wstrop.  This means we don't play nice and
        #Escape characters that are not in the target encoding.
        ws = wstring.from_utf8(text)
        text = ws.encode(encoding)
        #This version would skip all untranslatable chars: see wstrop.c
        #text = ws.encode(encoding, 1)
        return text

    def ConvertChar(m):
        char = ((int(ord(m.group(1))) & 0x03) << 6) | (int(ord(m.group(2))) & 0x3F)
        if HTML_CHARACTER_ENTITIES.has_key(char):
            return '&'+HTML_CHARACTER_ENTITIES[char]+';'
        else:
            return m.group()

    def UseHtmlCharEntities(text):
        new_text, num_subst = re.subn(g_utf8TwoBytePattern, ConvertChar, text)
        return new_text


import re, string
g_xmlIllegalCharPattern = re.compile('[\x01-\x08\x0B-\x0D\x0E-\x1F\x80-\xFF]')
g_numCharEntityPattern = re.compile('&#(\d+);')
g_utf8TwoBytePattern = re.compile('([\xC0-\xC3])([\x80-\xBF])')
g_htmlUniCharEntityPattern = re.compile('[\xa0-\xff]')
g_cdataCharPattern = re.compile('[&<]|]]>')
g_charToEntity = {
        '&': '&amp;',
        '<': '&lt;',
        ']]>': ']]&gt;',
        }


def TranslateHtmlCdata(characters, encoding='UTF-8', prev_chars=''):
    #Translate numerical char entity references with HTML entity equivalents
    new_string, num_subst = re.subn(
        g_cdataCharPattern,
        lambda m, d=g_charToEntity: d[m.group()],
        characters
        )
    if prev_chars[-2:] == ']]' and new_string[0] == '>':
        new_string = '&gt;' + new_string[1:]
    new_string = UseHtmlCharEntities(new_string)
    try:
        new_string = utf8_to_code(new_string, encoding)
    except:
        #FIXME: This is a work-around, contributed by Mike Brown, that
        #Deals with escaping output, until we have XML/HTML aware codecs
        tmp_new_string = ""
        for c in new_string:
            try:
                new_c = utf8_to_code(c, encoding)
            except:
                new_c = '&#%i;'%ord(c)
            tmp_new_string = tmp_new_string + new_c
        new_string = tmp_new_string
    #new_string, num_subst = re.subn(g_xmlIllegalCharPattern, lambda m: '&#%i;'%ord(m.group()), new_string)
    #Note: use decimal char entity rep because some browsers are broken
    return new_string


SECURE_HTML_ELEMS = ["A", "P", "BR", "B", "I", "DIV", "STRONG", "EM", "BLOCKQUOTE", "UL", "OL", "LI", "DL", "DD", "DT", "TT"]
