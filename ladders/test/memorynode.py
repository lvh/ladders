"""
A node that tracks what was done to it.

Useful for testing.
"""
import functools

from ladders import graph


class MemoryNode(graph.Node): # inherit __eq__, __hash__
    """
    A nodelike that remembers if you have asked about it's children.
    """
    def __init__(self, name, children=None):
        self.name = name
        self._children = set(children) if children else set()
        self.reset()


    def reset(self):
        self.readFrom, self.writtenTo = False, False


    def _getChildren(self):
        self.readFrom = True
        return self._children


    def _setChildren(self, children):
        self.writtenTo = True
        self._children = set(children)


    children = property(fget=_getChildren, fset=_setChildren)


create_branch = functools.partial(graph.create_branch, node_class=MemoryNode)
