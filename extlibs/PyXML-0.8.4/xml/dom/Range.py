########################################################################
#
# File Name:            Range.py
#
#
"""
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


from xml.dom import InvalidStateErr
from xml.dom import InvalidNodeTypeErr
from xml.dom import BadBoundaryPointsErr
from xml.dom import IndexSizeErr
from xml.dom import WrongDocumentErr

from xml.dom import Node


class Range:
    readOnly =['startContainer',
               'startOffset',
               'endContainer',
               'endOffset',
               'collapsed',
               'commonAncestorContainer',
               ]

    POSITION_EQUAL = 1
    POSITION_LESS_THAN = 2
    POSITION_GREATER_THAN = 3

    START_TO_START = 0
    START_TO_END = 1
    END_TO_END = 2
    END_TO_START = 3

    def __init__(self,ownerDocument):
        self._ownerDocument = ownerDocument

        self.__dict__['startContainer'] = ownerDocument
        self.__dict__['startOffset'] = 0
        self.__dict__['endContainer'] = ownerDocument
        self.__dict__['endOffset'] = 0
        self.__dict__['collapsed'] = 1
        self.__dict__['commonAncestorContainer'] = ownerDocument

        self.__dict__['detached'] = 0



    def __setattr__(self,name,value):
        if name in self.readOnly:
            raise AttributeError, name
        self.__dict__[name] = value

    def __getattr__(self,name):
        if name in self.readOnly:
            #Means we are detached
            raise InvalidStateErr()
        raise AttributeError, name





    def cloneContents(self):
        """Clone the contents defined by this range"""

        if self.detached:
            raise InvalidStateErr()

        df = self._ownerDocument.createDocumentFragment()

        if self.startContainer == self.endContainer:
            if self.startOffset == self.endOffset:
                return df
            if self.startContainer.nodeType in [Node.TEXT_NODE,
                                                Node.COMMENT_NODE,
                                                Node.PROCESSING_INSTRUCTION_NODE]:
                #Adjust the character data
                data = self.startContainer.substringData(self.startOffset,1+self.endOffset-self.startOffset)
                tx = self._ownerDocument.createTextNode(data)
                df.appendChild(tx)

            else:
                #Clone a set number of children
                numDel = self.endOffset - self.startOffset+1
                for ctr in range(numDel):
                    c = self.startContainer.childNodes[self.startOffset+ctr].cloneNode(1)
                    df.appendChild(c)

        elif self.startContainer == self.commonAncestorContainer:
            #Clone up the endContainer
            #From the start to the end
            lastKids = []
            copyData = None
            if self.endContainer.nodeType in [Node.TEXT_NODE,
                                              Node.COMMENT_NODE,
                                              Node.PROCESSING_INSTRUCTION_NODE]:
                #Adjust the character data
                copyData = self.endContainer.substringData(0,self.endOffset)
            else:
                numDel = self.endOffset
                for ctr in range(numDel):
                    lastKids.append(self.endContainer.childNodes[ctr].cloneNode(1))

            cur = self.endContainer
            while cur.parentNode != self.commonAncestorContainer:

                #Clone all of the way up
                newCur = cur.cloneNode(0)
                if copyData:
                    newCur.data = copyData
                    copyData = None
                for k in lastKids:
                    newCur.appendChild(k)

                lastKids = []
                index = cur.parentNode.childNodes.index(cur)
                for ctr in range(index):
                    lastKids.append(cur.parentNode.childNodes[ctr].cloneNode(1))
                lastKids.append(newCur)
                cur = cur.parentNode

            newEnd = cur.cloneNode(0)
            for k in lastKids:
                newEnd.appendChild(k)

            endAncestorChild = cur

            #Extract up to the ancestor of end
            for c in self.startContainer.childNodes:
                if c == endAncestorChild:
                    break
                df.appendChild(c.cloneNode(1))
            df.appendChild(newEnd)

        elif self.endContainer == self.commonAncestorContainer:
            lastKids = []
            copyData = None
            if self.startContainer.nodeType in [Node.TEXT_NODE,
                                                Node.COMMENT_NODE,
                                                Node.PROCESSING_INSTRUCTION_NODE]:
                #Adjust the character data

                copyData = self.startContainer.substringData(self.startOffset,1+len(self.startContainer.data)-self.startOffset)
            else:
                numDel = len(self.startContainer.childNodes) - self.startOffset
                for ctr in range(numDel):
                    c = self.startContainer.childNodes[self.startOffset+ctr].cloneNode(1)
                    lastKids.append(c)

            cur = self.startContainer
            while cur.parentNode != self.commonAncestorContainer:
                #Clone all of the way up
                newCur = cur.cloneNode(0)
                if copyData:
                    newCur.data = copyData
                    copyData = None
                for k in lastKids:
                    newCur.appendChild(k)
                lastKids = [newCur]

                index = cur.parentNode.childNodes.index(cur)
                for ctr in range(index+1,len(cur.parentNode.childNodes)):
                    lastKids.append(cur.parentNode.childNodes[ctr].cloneNode(1))
                cur = cur.parentNode

            startAncestorChild = cur
            newStart = cur.cloneNode(0)
            for k in lastKids:
                newStart.appendChild(k)

            df.appendChild(newStart)


            #Extract up to the ancestor of start
            startAncestorChild = cur
            startIndex = self.endContainer.childNodes.index(cur)
            lastAdded = None
            for ctr in range(startIndex+1,self.endOffset+1):
                c = self.endContainer.childNodes[ctr].cloneNode(1)
                df.insertBefore(c,lastAdded)
                lastAdded = c

        else:
            #From the start to the end
            lastStartKids = []
            startCopyData = None
            if self.startContainer.nodeType in [Node.TEXT_NODE,
                                                Node.COMMENT_NODE,
                                                Node.PROCESSING_INSTRUCTION_NODE]:
                #Adjust the character data

                startCopyData = self.startContainer.substringData(self.startOffset,1+len(self.startContainer.data)-self.startOffset)
            else:
                numDel = len(self.startContainer.childNodes) - self.startOffset
                for ctr in range(numDel):
                    c = self.startContainer.childNodes[self.startOffset+ctr].cloneNode(1)
                    lastStartKids.append(c)

            cur = self.startContainer
            while cur.parentNode != self.commonAncestorContainer:
                #Clone all of the way up
                newCur = cur.cloneNode(0)
                if startCopyData:
                    newCur.data = startCopyData
                    startCopyData = None
                for k in lastStartKids:
                    newCur.appendChild(k)
                lastStartKids = [newCur]


                index = cur.parentNode.childNodes.index(cur)
                for ctr in range(index+1,len(cur.parentNode.childNodes)):
                    lastStartKids.append(cur.parentNode.childNodes[ctr].cloneNode(1))
                cur = cur.parentNode

            startAncestorChild = cur

            newStart = cur.cloneNode(0)
            for k in lastStartKids:
                newStart.appendChild(k)

            df.appendChild(newStart)


            lastEndKids = []
            endCopyData = None
            #Delete up the endContainer
            #From the start to the end
            if self.endContainer.nodeType in [Node.TEXT_NODE,
                                              Node.COMMENT_NODE,
                                              Node.PROCESSING_INSTRUCTION_NODE]:
                #Adjust the character data
                endCopyData = self.endContainer.substringData(0,self.endOffset)
            else:
                numDel = self.endOffset
                for ctr in range(numDel):
                    c = self.endContainer.childNodes[ctr].cloneNode(1)
                    lastEndKids.append(c)

            cur = self.endContainer
            while cur.parentNode != self.commonAncestorContainer:
                newCur = cur.cloneNode(0)
                if endCopyData:
                    newCur.data = endCopyData
                    endCopyData = None
                for k in lastEndKids:
                    newCur.appendChild(k)

                lastEndKids = []
                index = cur.parentNode.childNodes.index(cur)
                for ctr in range(index):
                    lastEndKids.append(cur.parentNode.childNodes[ctr].cloneNode(1))
                lastEndKids.append(newCur)
                cur = cur.parentNode

            endAncestorChild = cur

            newEnd = cur.cloneNode(0)
            for k in lastEndKids:
                newEnd.appendChild(k)


            cur = startAncestorChild
            #Extract everything between us
            startIndex = startAncestorChild.parentNode.childNodes.index(startAncestorChild)
            endIndex = endAncestorChild.parentNode.childNodes.index(endAncestorChild)
            for ctr in range(startIndex+1,endIndex):
                c = startAncestorChild.parentNode.childNodes[ctr]
                df.appendChild(c.cloneNode(1))
            df.appendChild(newEnd)


        #Adjust the containers
        #FIXME What the heck is the spec talking about??
        self.__dict__['endContainer'] = self.startContainer
        self.__dict__['endOffset'] = self.startContainer
        self.__dict__['commonAncestorContainer'] = self.startContainer
        self.__dict__['collapsed'] = 1



        return df


    def cloneRange(self):
        if self.detached:
            raise InvalidStateErr()

        newRange = Range(self._ownerDocument)
        newRange.setStart(self.startContainer,self.startOffset)
        newRange.setEnd(self.endContainer,self.endOffset)
        return newRange

    def collapse(self,toStart):
        """Collapse the range"""
        if self.detached:
            raise InvalidStateErr()

        if toStart:
            self.__dict__['endContainer'] = self.startContainer
            self.__dict__['endOffset'] = self.startOffset
        else:
            self.__dict__['startContainer'] = self.endContainer
            self.__dict__['startOffset'] = self.endOffset

        self.__dict__['collapsed'] = 1
        self.__dict__['commonAncestorContainer'] = self.startContainer


    def compareBoundaryPoints(self,how,sourceRange):
        if self.detached:
            raise InvalidStateErr()

        if not hasattr(sourceRange,'_ownerDocument') or sourceRange._ownerDocument != self._ownerDocument or not isinstance(sourceRange,Range):
            raise WrongDocumentErr()

        if how == self.START_TO_START:
            ac = self.startContainer
            ao = self.startOffset
            bc = sourceRange.startContainer
            bo = sourceRange.startOffset
        elif how == self.START_TO_END:
            ac = self.startContainer
            ao = self.startOffset
            bc = sourceRange.endContainer
            bo = sourceRange.endOffset
        elif how == self.END_TO_END:
            ac = self.endContainer
            ao = self.endOffset
            bc = sourceRange.endContainer
            bo = sourceRange.endOffset
        elif how == self.END_TO_START:
            ac = self.endContainer
            ao = self.endOffset
            bc = sourceRange.startContainer
            bo = sourceRange.startOffset
        else:
            raise TypeError, how

        pos = self.__comparePositions(ac,ao,bc,bo)
        if pos == self.POSITION_EQUAL:
            return 0
        elif pos == self.POSITION_LESS_THAN:
            return -1
        return 1

    def deleteContents(self):
        """Delete the contents defined by this range"""


        #NOTE Use 4DOM ReleaseNode cause it is interface safe
        from xml.dom.ext import ReleaseNode

        if self.detached:
            raise InvalidStateErr()

        if self.startContainer == self.endContainer:
            if self.startOffset == self.endOffset:
                return
            if self.startContainer.nodeType in [Node.TEXT_NODE,
                                                Node.COMMENT_NODE,
                                                Node.PROCESSING_INSTRUCTION_NODE]:
                #Adjust the character data
                self.startContainer.deleteData(self.startOffset,1+self.endOffset-self.startOffset)

            else:
                #Delete a set number of children
                numDel = self.endOffset - self.startOffset+1
                for ctr in range(numDel):
                    c = self.startContainer.removeChild(self.startContainer.childNodes[self.startOffset])
                    ReleaseNode(c)

            self.__dict__['endContainer'] = self.startContainer
            self.__dict__['endOffset'] = self.endContainer
            self.__dict__['commonAncestorContainer'] = self.endContainer
            self.__dict__['collapsed'] = 1

        elif self.startContainer == self.commonAncestorContainer:
            #Delete up the endContainer
            #From the start to the end
            if self.endContainer.nodeType in [Node.TEXT_NODE,
                                              Node.COMMENT_NODE,
                                              Node.PROCESSING_INSTRUCTION_NODE]:
                #Adjust the character data
                self.endContainer.deleteData(0,self.endOffset)
            else:
                numDel = self.endOffset
                for ctr in range(numDel):
                    c = self.endContainer.removeChild(self.endContainer.childNodes[0])
                    ReleaseNode(c)

            cur = self.endContainer
            while cur.parentNode != self.commonAncestorContainer:
                while cur.previousSibling:
                    c = cur.parentNode.removeChild(cur.previousSibling)
                    ReleaseNode(c)
                cur = cur.parentNode

            #Delete up to the ancestor of end
            endAncestorChild = cur
            while self.startContainer.firstChild != endAncestorChild:
                c = self.startContainer.removeChild(self.startContainer.firstChild)
                ReleaseNode(c)
        elif self.endContainer == self.commonAncestorContainer:
            if self.startContainer.nodeType in [Node.TEXT_NODE,
                                                Node.COMMENT_NODE,
                                                Node.PROCESSING_INSTRUCTION_NODE]:
                #Adjust the character data
                self.startContainer.deleteData(self.startOffset,1+len(self.startContainer.data)-self.startOffset)
            else:
                numDel = len(self.startContainer.childNodes) - self.startOffset
                for ctr in range(numDel):
                    c = self.startContainer.removeChild(self.startContainer.childNodes[self.startOffset])
                    ReleaseNode(c)

            cur = self.startContainer
            while cur.parentNode != self.commonAncestorContainer:
                while cur.nextSibling:
                    c = cur.parentNode.removeChild(cur.nextSibling)
                    ReleaseNode(c)
                cur = cur.parentNode

            startAncestorChild = cur

            #Delete up to the ancestor of start
            startAncestorChild = cur
            startIndex = self.endContainer.childNodes.index(cur)
            numDel = self.endOffset - startIndex
            for ctr in range(numDel):
                c = self.endContainer.removeChild(startAncestorChild.nextSibling)
                ReleaseNode(c)

        else:
            #From the start to the end
            if self.startContainer.nodeType in [Node.TEXT_NODE,
                                                Node.COMMENT_NODE,
                                                Node.PROCESSING_INSTRUCTION_NODE]:
                #Adjust the character data
                self.startContainer.deleteData(self.startOffset,1+len(self.startContainer.data)-self.startOffset)
            else:
                numDel = len(self.startContainer.childNodes) - self.startOffset
                for ctr in range(numDel):
                    c = self.startContainer.removeChild(self.startContainer.childNodes[self.startOffset])
                    ReleaseNode(c)

            cur = self.startContainer
            while cur.parentNode != self.commonAncestorContainer:
                while cur.nextSibling:
                    c = cur.parentNode.removeChild(cur.nextSibling)
                    ReleaseNode(c)
                cur = cur.parentNode

            startAncestorChild = cur
            #Delete up the endContainer
            #From the start to the end
            if self.endContainer.nodeType in [Node.TEXT_NODE,
                                              Node.COMMENT_NODE,
                                              Node.PROCESSING_INSTRUCTION_NODE]:
                #Adjust the character data
                self.endContainer.deleteData(0,self.endOffset)
            else:
                numDel = self.endOffset
                for ctr in range(numDel):
                    c = self.endContainer.removeChild(self.endContainer.childNodes[0])
                    ReleaseNode(c)

            cur = self.endContainer
            while cur.parentNode != self.commonAncestorContainer:
                while cur.previousSibling:
                    c = cur.parentNode.removeChild(cur.previousSibling)
                    ReleaseNode(c)
                cur = cur.parentNode

            endAncestorChild = cur

            cur = startAncestorChild
            #Delete everything between us
            while cur.nextSibling != endAncestorChild:
                c = cur.parentNode.removeChild(cur.nextSibling)
                ReleaseNode(c)

        #Adjust the containers
        #FIXME What the heck is the spec talking about??
        self.__dict__['endContainer'] = self.startContainer
        self.__dict__['endOffset'] = self.startContainer
        self.__dict__['commonAncestorContainer'] = self.startContainer
        self.__dict__['collapsed'] = 1

        return None

    def detach(self):
        self.detached = 1
        del self.startContainer
        del self.endContainer
        del self.startOffset
        del self.endOffset
        del self.collapsed
        del self.commonAncestorContainer

    def extractContents(self):
        """Extract the contents defined by this range"""


        if self.detached:
            raise InvalidStateErr()

        df = self._ownerDocument.createDocumentFragment()

        if self.startContainer == self.endContainer:
            if self.startOffset == self.endOffset:
                return df
            if self.startContainer.nodeType in [Node.TEXT_NODE,
                                                Node.COMMENT_NODE,
                                                Node.PROCESSING_INSTRUCTION_NODE]:
                #Adjust the character data
                data = self.startContainer.substringData(self.startOffset,1+self.endOffset-self.startOffset)
                self.startContainer.deleteData(self.startOffset,1+self.endOffset-self.startOffset)

                tx = self._ownerDocument.createTextNode(data)
                df.appendChild(tx)

            else:
                #Extrace a set number of children

                numDel = self.endOffset - self.startOffset+1
                for ctr in range(numDel):
                    c = self.startContainer.removeChild(self.startContainer.childNodes[self.startOffset])
                    df.appendChild(c)

        elif self.startContainer == self.commonAncestorContainer:
            #Delete up the endContainer
            #From the start to the end
            lastKids = []
            copyData = None
            #Delete up the endContainer
            #From the start to the end
            if self.endContainer.nodeType in [Node.TEXT_NODE,
                                              Node.COMMENT_NODE,
                                              Node.PROCESSING_INSTRUCTION_NODE]:
                #Adjust the character data
                copyData = self.endContainer.substringData(0,self.endOffset)
                self.endContainer.deleteData(0,self.endOffset)
            else:
                numDel = self.endOffset
                for ctr in range(numDel):
                    c = self.endContainer.removeChild(self.endContainer.childNodes[0])
                    lastKids.append(c)

            cur = self.endContainer
            while cur.parentNode != self.commonAncestorContainer:

                #Clone all of the way up
                newCur = cur.cloneNode(0)
                if copyData:
                    newCur.data = copyData
                    copyData = None
                for k in lastKids:
                    newCur.appendChild(k)
                lastKids = [newCur]

                while cur.previousSibling:
                    c = cur.parentNode.removeChild(cur.previousSibling)
                    lastKids = [c] + lastKids
                cur = cur.parentNode

            newEnd = cur.cloneNode(0)
            for k in lastKids:
                newEnd.appendChild(k)

            endAncestorChild = cur

            #Extract up to the ancestor of end
            while self.startContainer.firstChild != endAncestorChild:
                c = self.startContainer.removeChild(self.startContainer.firstChild)
                df.appendChild(c)
            df.appendChild(newEnd)

        elif self.endContainer == self.commonAncestorContainer:
            lastKids = []
            copyData = None
            if self.startContainer.nodeType in [Node.TEXT_NODE,
                                                Node.COMMENT_NODE,
                                                Node.PROCESSING_INSTRUCTION_NODE]:
                #Adjust the character data

                copyData = self.startContainer.substringData(self.startOffset,1+len(self.startContainer.data)-self.startOffset)
                self.startContainer.deleteData(self.startOffset,1+len(self.startContainer.data)-self.startOffset)
            else:
                numDel = len(self.startContainer.childNodes) - self.startOffset
                for ctr in range(numDel):
                    c = self.startContainer.removeChild(self.startContainer.childNodes[self.startOffset])
                    lastKids.append(c)

            cur = self.startContainer
            while cur.parentNode != self.commonAncestorContainer:
                #Clone all of the way up
                newCur = cur.cloneNode(0)
                if copyData:
                    newCur.data = copyData
                    copyData = None
                for k in lastKids:
                    newCur.appendChild(k)
                lastKids = [newCur]

                while cur.nextSibling:
                    c = cur.parentNode.removeChild(cur.nextSibling)
                    lastKids.append(c)
                cur = cur.parentNode

            startAncestorChild = cur
            newStart = cur.cloneNode(0)
            for k in lastKids:
                newStart.appendChild(k)

            df.appendChild(newStart)


            #Extract up to the ancestor of start
            startAncestorChild = cur
            startIndex = self.endContainer.childNodes.index(cur)
            lastAdded = None
            numDel = self.endOffset - startIndex
            for ctr in range(numDel):
                c = self.endContainer.removeChild(startAncestorChild.nextSibling)
                df.insertBefore(c,lastAdded)
                lastAdded = c

        else:
            #From the start to the end
            lastStartKids = []
            startCopyData = None
            if self.startContainer.nodeType in [Node.TEXT_NODE,
                                                Node.COMMENT_NODE,
                                                Node.PROCESSING_INSTRUCTION_NODE]:
                #Adjust the character data

                startCopyData = self.startContainer.substringData(self.startOffset,1+len(self.startContainer.data)-self.startOffset)
                self.startContainer.deleteData(self.startOffset,1+len(self.startContainer.data)-self.startOffset)
            else:
                numDel = len(self.startContainer.childNodes) - self.startOffset
                for ctr in range(numDel):
                    c = self.startContainer.removeChild(self.startContainer.childNodes[self.startOffset])
                    lastStartKids.append(c)

            cur = self.startContainer
            while cur.parentNode != self.commonAncestorContainer:
                #Clone all of the way up
                newCur = cur.cloneNode(0)
                if startCopyData:
                    newCur.data = startCopyData
                    startCopyData = None
                for k in lastStartKids:
                    newCur.appendChild(k)
                lastStartKids = [newCur]

                while cur.nextSibling:
                    c = cur.parentNode.removeChild(cur.nextSibling)
                    lastStartKids.append(c)
                cur = cur.parentNode

            startAncestorChild = cur

            newStart = cur.cloneNode(0)
            for k in lastStartKids:
                newStart.appendChild(k)
            if startCopyData:
                newStart.data = startCopyData
                startCopyData = None

            df.appendChild(newStart)


            lastEndKids = []
            endCopyData = None
            #Delete up the endContainer
            #From the start to the end
            if self.endContainer.nodeType in [Node.TEXT_NODE,
                                              Node.COMMENT_NODE,
                                              Node.PROCESSING_INSTRUCTION_NODE]:
                #Adjust the character data
                endCopyData = self.endContainer.substringData(0,self.endOffset)
                self.endContainer.deleteData(0,self.endOffset)
            else:
                numDel = self.endOffset
                for ctr in range(numDel):
                    c = self.endContainer.removeChild(self.endContainer.childNodes[0])
                    lastEndKids.append(c)

            cur = self.endContainer
            while cur.parentNode != self.commonAncestorContainer:
                newCur = cur.cloneNode(0)
                if endCopyData:
                    newCur.data = endCopyData
                    endCopyData = None
                for k in lastEndKids:
                    newCur.appendChild(k)
                lastEndKids = [newCur]
                while cur.previousSibling:
                    c = cur.parentNode.removeChild(cur.previousSibling)
                    lastEndKids = [c] + lastEndKids
                cur = cur.parentNode

            endAncestorChild = cur

            newEnd = cur.cloneNode(0)
            for k in lastEndKids:
                newEnd.appendChild(k)
            if endCopyData:
                newEnd.data = endCopyData
                endCopyData = None

            cur = startAncestorChild
            #Extract everything between us
            while cur.nextSibling != endAncestorChild:
                c = cur.parentNode.removeChild(cur.nextSibling)
                df.appendChild(c)
            df.appendChild(newEnd)


        #Adjust the containers
        #FIXME What the heck is the spec talking about??
        self.__dict__['endContainer'] = self.startContainer
        self.__dict__['endOffset'] = self.startOffset
        self.__dict__['commonAncestorContainer'] = self.startContainer
        self.__dict__['collapsed'] = 1



        return df


    def insertNode(self,newNode):
        """Insert a node at the starting point"""

        if self.detached:
            raise InvalidStateErr()

        if newNode.nodeType in [Node.ATTRIBUTE_NODE,
                                Node.ENTITY_NODE,
                                Node.NOTATION_NODE,
                                Node.DOCUMENT_NODE,
                                ]:
            raise InvalidNodeTypeErr()

        if self.startContainer.nodeType == Node.TEXT_NODE:
            #Split the text at the boundary.  Insert the node after this
            otherText = self.startContainer.substringData(self.startOffset,len(self.startContainer.data))
            self.startContainer.deleteData(self.startOffset,len(self.startContainer.data))
            newText = self._ownerDocument.createTextNode(otherText)
            self.startContainer.parentNode.insertBefore(newText,self.startContainer.nextSibling)

            newText.parentNode.insertBefore(newNode,newText)
        elif self.startContainer.nodeType in [Node.COMMENT_NODE,
                                              Node.PROCESSING_INSTRUCTION_NODE]:
            raise HierarchyRequestErr()
        else:
            curNode = self.startContainer.childNodes[self.startOffset]
            self.startContainer.insertBefore(newNode,curNode.nextSibling)



    def selectNode(self,refNode):
        """Select a node"""
        if self.detached:
            raise InvalidStateErr()

        self.__validateRefNode(refNode)

        self.__dict__['startContainer'] = refNode.parentNode
        self.__dict__['endContainer'] = refNode.parentNode


        index = refNode.parentNode.childNodes.index(refNode)
        self.__dict__['startOffset'] = index
        self.__dict__['endOffset'] = index+1

        self.__dict__['collapsed'] = 0
        self.__dict__['commonAncestorContainer'] = refNode.parentNode


    def selectNodeContents(self,refNode):
        """Select a node"""
        if self.detached:
            raise InvalidStateErr()

        self.__validateBoundary(refNode,0)


        self.__dict__['startContainer'] = refNode
        self.__dict__['endContainer'] = refNode


        self.__dict__['startOffset'] = 0
        self.__dict__['endOffset'] = len(refNode.childNodes)

        self.__dict__['collapsed'] = self.startOffset == self.endOffset
        self.__dict__['commonAncestorContainer'] = refNode



    def setEnd(self,parent,offset):
        """Set the ranges end container and offset"""

        #Check for errors
        if self.detached:
            raise InvalidStateErr()

        self.__validateBoundary(parent,offset)

        self.__dict__['endContainer'] = parent
        self.__dict__['endOffset'] = offset

        self.__dict__['collapsed'] = 0

        pos =  self.__comparePositions(parent,offset,self.startContainer,self.startOffset)
        self.__dict__['collapsed'] = (pos == self.POSITION_EQUAL)
        if pos == self.POSITION_LESS_THAN:
            self.__dict__['startContainer'] = parent
            self.__dict__['startOffset'] = offset
            self.__dict__['collapsed'] = 1

        self.__calculateCommonAncestor()

    def setEndAfter(self,node):

        self.__validateRefNode(node)

        cont = node.parentNode
        index = cont.childNodes.index(node)
        self.setEnd(cont,index+1)

    def setEndBefore(self,node):

        self.__validateRefNode(node)

        cont = node.parentNode
        index = cont.childNodes.index(node)
        self.setEnd(cont,index)



    def setStart(self,parent,offset):
        """Set the ranges start container and offset"""

        #Check for errors
        if self.detached:
            raise InvalidStateErr()

        self.__validateBoundary(parent,offset)

        self.__dict__['startContainer'] = parent
        self.__dict__['startOffset'] = offset


        pos = self.__comparePositions(parent,offset,self.endContainer,self.endOffset)
        self.__dict__['collapsed'] = (pos == self.POSITION_EQUAL)

        if pos == self.POSITION_GREATER_THAN:
            self.__dict__['endContainer'] = parent
            self.__dict__['endOffset'] = offset
            self.__dict__['collapsed'] = 1

        self.__calculateCommonAncestor()

    def setStartAfter(self,node):

        self.__validateRefNode(node)

        cont = node.parentNode
        index = cont.childNodes.index(node)
        self.setStart(cont,index+1)

    def setStartBefore(self,node):

        self.__validateRefNode(node)

        cont = node.parentNode
        index = cont.childNodes.index(node)
        self.setStart(cont,index)

    def surroundContents(self,newParent):
        """Surround the range with this node"""
        if self.detached:
            raise InvalidStateErr()

        if newParent.nodeType in [Node.ATTRIBUTE_NODE,
                                  Node.ENTITY_NODE,
                                  Node.DOCUMENT_TYPE_NODE,
                                  Node.NOTATION_NODE,
                                  Node.DOCUMENT_NODE,
                                  Node.DOCUMENT_FRAGMENT_NODE]:
            raise InvalidNodeTypeErr()

        #See is we have element nodes that are partially selected
        if self.startContainer.nodeType not in [Node.TEXT_NODE,
                                                Node.COMMENT_NODE,
                                                Node.PROCESSING_INSTRUCTION_NODE]:
            if self.commonAncestorContainer not in [self.startContainer,self.startContainer.parentNode]:
                #This is partially selected because our parent is not the common ancestor
                raise BadBoundaryPointsErr()
        if self.endContainer.nodeType not in [Node.TEXT_NODE,
                                              Node.COMMENT_NODE,
                                              Node.PROCESSING_INSTRUCTION_NODE]:
            if self.commonAncestorContainer not in [self.endContainer,self.endContainer.parentNode]:
                #This is partially selected because our parent is not the common ancestor
                raise BadBoundaryPointsErr()

        #All good, do the insert
        #Remove children from newPArent
        for c in newParent.childNodes:
            newParent.removeChild(c)

        df = self.extractContents()

        self.insertNode(newParent)

        newParent.appendChild(df)

        self.selectNode(newParent)


    def toString(self):
        if self.detached:
            raise InvalidStateErr()

        df = self.cloneContents()


        res = self.__recurseToString(df)


        from xml.dom.ext import ReleaseNode
        ReleaseNode(df)

        return res

    #Internal Functions#


    def __validateBoundary(self,node,offset):
        """Make sure the node is a legal boundary"""

        if not hasattr(node,'nodeType'):
            raise InvalidNodeTypeErr()


        #Check for proper node type
        curNode = node
        while curNode:
            if curNode.nodeType in [Node.ENTITY_NODE,
                                    Node.NOTATION_NODE,
                                    Node.DOCUMENT_TYPE_NODE,
                                    ]:
                raise InvalidNodeTypeErr()
            curNode = curNode.parentNode

        #Check number of cild units
        if offset < 0:
            raise IndexSizeErr()

        if node.nodeType in [Node.TEXT_NODE,
                             Node.COMMENT_NODE,
                             Node.PROCESSING_INSTRUCTION_NODE]:
            #Child units are characters
            if offset > len(node.data):
                raise IndexSizeErr()
        else:
            if offset > len(node.childNodes):
                raise IndexSizeErr()

    def __validateRefNode(self,node):

        if not hasattr(node,'nodeType'):
            raise InvalidNodeTypeErr()

        cur = node
        while cur.parentNode:
            cur = cur.parentNode
        if cur.nodeType not in [Node.ATTRIBUTE_NODE,
                                Node.DOCUMENT_NODE,
                                Node.DOCUMENT_FRAGMENT_NODE,
                                ]:
            raise InvalidNodeTypeErr()

        if node.nodeType in [Node.DOCUMENT_NODE,
                             Node.DOCUMENT_FRAGMENT_NODE,
                             Node.ATTRIBUTE_NODE,
                             Node.ENTITY_NODE,
                             Node.NOTATION_NODE,
                             ]:

            raise InvalidNodeTypeErr()


    def __comparePositions(self,aContainer,aOffset,bContainer,bOffset):
        """Compare Boundary Positions Section 2.5"""

        if aContainer == bContainer:
            #CASE 1
            if aOffset == bOffset:
                return self.POSITION_EQUAL
            elif aOffset < bOffset:
                return self.POSITION_LESS_THAN
            else:
                return self.POSITION_GREATER_THAN
        #CASE 2
        bAncestors = []
        cur = bContainer
        while cur:
            bAncestors.append(cur)
            cur = cur.parentNode

        for ctr in range(len(aContainer.childNodes)):
            c = aContainer.childNodes[ctr]
            if c in bAncestors:
                if aOffset <= ctr:
                    return self.POSITION_LESS_THAN
                else:
                    return self.POSITION_GREATER_THAN

        #CASE 3
        aAncestors = []
        cur = aContainer
        while cur:
            aAncestors.append(cur)
            cur = cur.parentNode

        for ctr in range(len(bContainer.childNodes)):
            c = bContainer.childNodes[ctr]
            if c in aAncestors:
                if ctr < bOffset:
                    return self.POSITION_LESS_THAN
                else:
                    return self.POSITION_GREATER_THAN



        #CASE 4
        #Check the "Following axis" of A.
        #If B is in the axis, then A is before B

        curr = aContainer
        while curr != aContainer.ownerDocument:
            sibling = curr.nextSibling
            while sibling:
                if curr == bContainer:
                    return self.POSITION_LESS_THAN
                rt = self.__checkDescendants(sibling,bContainer)
                if rt:
                    return self.POSITION_LESS_THAN
                sibling = sibling.nextSibling
            curr = ((curr.nodeType == Node.ATTRIBUTE_NODE) and
                    curr.ownerElement or curr.parentNode)

        #Not in the following, return POSITION_LESS_THAN
        return self.POSITION_GREATER_THAN

    def __checkDescendants(self,sib,b):
        for c in sib.childNodes:
            if c == b: return 1
            if self.__checkDescendants(c,b): return 1
        return 0


    def __calculateCommonAncestor(self):

        if self.startContainer == self.endContainer:
            self.__dict__['commonAncestorContainer'] = self.startContainer

        startAncestors = []
        cur = self.startContainer
        while cur:
            startAncestors.append(cur)
            cur = cur.parentNode

        cur = self.endContainer
        while cur:
            if cur in startAncestors:
                self.__dict__['commonAncestorContainer'] = cur
                return
            cur = cur.parentNode

        #Hmm no ancestor
        raise BadBoundaryPointsErr()


    def __recurseToString(self,node):

        if node.nodeType in [Node.TEXT_NODE,
                             Node.CDATA_SECTION_NODE]:
            return node.data
        else:
            res = ""
            for c in node.childNodes:
                res = res + self.__recurseToString(c)
            return res
