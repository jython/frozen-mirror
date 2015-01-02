########################################################################
#
# File Name:            Comment.py
#
#
"""
WWW: http://4suite.org/4DOM         e-mail: support@4suite.org

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""

from xml.dom import Node
from CharacterData import CharacterData

class Comment(CharacterData):
    nodeType = Node.COMMENT_NODE

    def __init__(self,ownerDocument,data):
        CharacterData.__init__(self, ownerDocument, data)
        self.__dict__['__nodeName'] = '#comment'
