# A simple library to convert DOM object structures to SGML or XML output,
# usually for xml2html conversion.

import sys,types,string,StringIO

SKIP=1       # Ignore the element and its contents
STRIP=2      # Ignore the element, but process its contents
ID=3         # Identity transform
MAP=4        # Arg: (elem,hash). Map element to elem, map attrs using hash.

def escape_markup(str):
    """Takes a string and escapes all '<'s and quotes in it with character
    entity references."""
    str=string.replace(str,"<","&#60;")
    return string.replace(str,'"',"&#34;")

def convert(rootnode,spec,writer=sys.stdout):
    """Takes a DOM node, a conversion specification and a file-like object
    to write the converted data to, and performs the actual conversion.
    The spec hashtable must map element names to (action,arg) tuples, where
    action must be one of the constants at the top of this file. arg is only
    used for MAP, where it must be a tuple (elementname,maphash) where the
    elementname is the name of the element to substitute for the original
    one, and maphash is a hashtable that maps attribute names to either the
    attribute name to substitute or a function that takes the attribute value
    and returns the string to replace the entire attr='val' sequence with.
    """

    try:
        (action,arg)=spec[rootnode.GI]
    except KeyError:
        action=STRIP

    if action==SKIP:
        return
    elif action==STRIP:
        pass
    elif action==ID:
        writer.write("<" + rootnode.GI)
        for (name,val) in rootnode.attributes.items():
            writer.write(" %s='%s'" % (name,escape_markup(val)))
        writer.write(">")
    elif action==MAP:
        writer.write("<" + arg[0])
        for (name,val) in rootnode.attributes.items():
            if arg[1].has_key(name):
                map=arg[1][name]
                if type(map)==types.StringType:
                    writer.write(" %s=\"%s\"" % (map,escape_markup(val)))
                else:
                    writer.write(map(escape_markup(val)))

        writer.write(">")

    for child in rootnode.getChildren():
        if child.GI=="#PCDATA":
            writer.write(escape_markup(child.data))
        else:
            convert(child,spec,writer)

    if action==ID:
        writer.write("</%s>" % rootnode.GI)
    elif action==MAP:
        writer.write("</%s>" % arg[0])

def convert_str(rootnode,spec):
    obj=StringIO.StringIO()
    convert(rootnode,spec,obj)
    return obj.getvalue()
