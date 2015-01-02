########################################################################
#
# File Name:            Event.py
#
#
"""
Implements DOM level 2 Mutation Events
WWW: http://4suite.com/4DOM         e-mail: support@4suite.com

Copyright (c) 2000 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.com/COPYRIGHT  for license and copyright information
"""


supportedEvents = [
    "DOMSubtreeModified",
    "DOMNodeInserted",
    "DOMNodeRemoved",
    "DOMNodeRemovedFromDocument",
    "DOMNodeInsertedIntoDocument",
    "DOMAttrModified",
    "DOMCharacterDataModified"
    ]

#Event Exception code
UNSPECIFIED_EVENT_TYPE_ERR = 0

class EventException:
    def __init__(self, code):
        self.code = code


class EventTarget:
    """
    """
    def __init__(self):
        self.listeners = {}
        self.capture_listeners = {}
        for etype in supportedEvents:
            self.listeners[etype] = []
            self.capture_listeners[etype] = []

    def addEventListener(self, etype, listener, useCapture):
        if useCapture:
            if listener not in self.capture_listeners[etype]:
                self.capture_listeners[etype].append(listener)
        else:
            if listener not in self.listeners[etype]:
                self.listeners[etype].append(listener)

    def removeEventListener(self, etype, listener, useCapture):
        if useCapture:
           self.capture_listeners[etype].remove(listener)
        else:
           self.listeners[etype].remove(listener)


    def dispatchEvent(self, evt):
        # The actual work is done in the implementing class
        # since EventTarget has no idea of the DOM hierarchy
        pass


class EventListener:
    def __init__(self):
        pass

    def handleEvent(evt):
        pass


class Event:
    CAPTURING_PHASE = 1
    AT_TARGET = 2
    BUBBLING_PHASE = 3

    def __init__(self, eventType):
        self.target = None
        self.currentTarget = None
        self.eventPhase = Event.CAPTURING_PHASE
        self.type = eventType
        self.timeStamp = 0

    def stopPropagation(self):
        self._4dom_propagate = 0

    def preventDefault(self):
        self._4dom_preventDefaultCalled = 1

    def initEvent(self, eventTypeArg, canBubbleArg, cancelableArg):
        self.type = eventTypeArg
        self.bubbles = canBubbleArg
        self.cancelable = cancelableArg
        self._4dom_preventDefaultCalled = 0
        self._4dom_propagate = 1


class MutationEvent(Event):
    #Whether or not the event bubbles
    MODIFICATION = 1
    ADDITION = 2
    REMOVAL = 3
    eventSpec = {
        "DOMSubtreeModified": 1,
        "DOMNodeInserted": 1,
        "DOMNodeRemoved": 1,
        "DOMNodeRemovedFromDocument": 0,
        "DOMNodeInsertedIntoDocument": 0,
        "DOMAttrModified": 1,
        "DOMCharacterDataModified": 1
        }

    def __init__(self, eventType):
        Event.__init__(self,eventType)
        return

    def initMutationEvent(self, eventTypeArg, canBubbleArg, cancelableArg,
                          relatedNodeArg, prevValueArg, newValueArg, attrNameArg):
        Event.initEvent(self,eventTypeArg, canBubbleArg, cancelableArg)
        # FIXME : make these attributes readonly
        self.relatedNode = relatedNodeArg
        self.prevValue = prevValueArg
        self.newValue = newValueArg
        self.attrName = attrNameArg
        #No mutation events are cancelable
        self.cancelable = 0
