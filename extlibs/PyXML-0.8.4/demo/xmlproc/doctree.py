"""
A very simple tree model for XML documents. Elements are represented as
triples (name, attribute dictionary, content list), and the entire document
is represented by the document element.
"""

import types

from xml.parsers.xmlproc import xmlproc

# --- Tree-building functions

def build_tree(sysid):
    "Builds a doctree and returns it."

    class BuilderApp(xmlproc.Application):
        "The actual tree builder."

        def __init__(self):
            self.root=None
            self.current_stack=[]

        def handle_start_tag(self,name,attrs):
            if self.root==None:
                self.current_stack.append([])
                self.root=(name,attrs,self.current_stack[-1])
            else:
                list=[]
                self.current_stack[-1].append(name,attrs,list)
                self.current_stack.append(list)

        def handle_data(self,data,start,end):
            if self.root!=None:
                self.current_stack[-1].append(data[start:end])

        def handle_end_tag(self,name):
            del self.current_stack[-1]

    builder=BuilderApp()
    parser=xmlproc.XMLProcessor()
    parser.set_application(builder)
    parser.parse_resource(sysid)

    return builder.root

# --- Utility functions

def get_element(parent,child_type_name):
    "Locates the first child element with the given name inside an element."

    for child in parent[2]:
        if type(child)==types.TupleType and child[0]==child_type_name:
            return child

def get_elements(parent,child_type_name):
    "Locates the child elements with the given name inside an element."

    list=[]
    for child in parent[2]:
        if type(child)==types.TupleType and child[0]==child_type_name:
            list.append(child)

    return list

def get_pcdata(parent):
    """Picks out the PCDATA contents of the element, under the assumption
    that all the contents are PCDATA."""

    return parent[2][0]
