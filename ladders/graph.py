#-*- encoding: utf-8 -*-
"""
Tools for describing graphs and operating on paths.
"""
import itertools


class Node(object):
    """
    A node in a graph.

    This is also sometimes called a vertex in literature.
    """
    def __init__(self, name, children=None):
        """
        Initializes a node.
        """
        self.name = name
        self.children = set(children) if children else set()


    def __eq__(self, other):
        """
        Compares two nodes for equality.
        """
        if isinstance(self, type(other)):
            return self.name == other.name
        
        return NotImplemented


    def __ne__(self, other):
        """
        Compares two nodes for equality.
        """
        result = self.__eq__(other)

        if result is NotImplemented:
            return result

        return not result
        

    def __hash__(self):
        """
        Returns the hash of the name of this node.
        """
        return hash(self.name)


    def __repr__(self):
        """
        Returns a textual representation of this node.
        """
        return "Node(%r)" % (self.name,)



class LadderNode(Node):
    """
    A node in a word ladder search graph.
    """
    def __init__(self, name, words):
        super(LadderNode, self).__init__(name)
        self.words = words


    @property
    def children(self):
        children = self._get_children()
        try:
            first_child = children.next()
            return itertools.chain([first_child], children)
        except StopIteration:
            return []


    def _get_children(self):
        child_words = [word for word in self.words if word != self.name]
        for word in child_words:
            if distance(word, self.name) == 1:
                yield LadderNode(word, child_words)


    @children.setter
    def children(self, words):
        self.words = words



def distance(word_one, word_two):
    return sum(1 for (x, y) in zip(word_one, word_two) if x != y)


def extended_paths(path):
    """
    Extends a path with all possible children of the last node in the path.

    @return: An iterable of the extended paths (one for each child node).
    @rtype: An iterable of paths.
    """
    for child in path[-1].children:
        yield path + [child]



def has_cycle(path):
    """
    Checks if a given path has at least one cycle in it.

    @return: A true value if the path has a cycle, a false value otherwise.
    """
    seen = set()
    
    for node in path:
        if node in seen:
            return True
        seen.add(node)
    else:
        return False


def has_new_cycle(path):
    """
    Checks if the last node in a given path introduces a cycle.
    """
    return path[-1] in path[:-1]


def create_branch(names, node_class=Node):
    """
    Creates a branch with no subbranches.

    If P -> C represents a parent -> child relationship, for an input of
    "ABCDEFG", this will create the nodes A through G which will have the
    parent-child relationships A->B, B->C, C->D... and only those.

    Returns the path representing the entire branch.
    """
    parents, children = itertools.tee(node_class(n) for n in names)
    
    path = [children.next()]

    for parent, child in itertools.izip(parents, children):
        parent.children.add(child)
        path.append(child)

    return path