"""A DOM implementation that offers traversal and ranges on top of
minidom, using the 4DOM traversal implementation."""

import minidom

class DOMImplementation(minidom.DOMImplementation):
    # Augment the features table instead of duplicating the logic in
    # hasFeature().
    _features = minidom.DOMImplementation._features + [
        ("traversal", "1.0"),
        ("traversal", "2.0"),
        ("traversal", None),
        ("range", "1.0"),
        ("range", "2.0"),
        ("range", None),
        ]

    def _create_document(self):
        return Document()

class Document(minidom.Document):
    implementation = DOMImplementation()

    def createNodeIterator(self, root, whatToShow, filter,
                           entityReferenceExpansion):
        from xml.dom.NodeIterator import NodeIterator
        return NodeIterator(root, whatToShow, filter, entityReferenceExpansion)

    def createTreeWalker(self, root, whatToShow, filter,
                         entityReferenceExpansion):
        from TreeWalker import TreeWalker
        return TreeWalker(root, whatToShow, filter, entityReferenceExpansion)

    def createRange(self):
        from Range import Range
        return Range(self)

def getDOMImplementation():
    return Document.implementation
