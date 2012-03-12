#-*- encoding: utf-8 -*-
"""
Test cases for blind searching.
"""
import itertools
import unittest

from ladders import graph, blind


class CommonSearchTestsMixin(object):
    def test_one_node(self):
        r = graph.Node('root')
        paths = self.search_function(r, lambda n: n == r)

        self.assertEquals([r], paths.next())
        self.assertRaises(StopIteration, paths.next)


    def test_two_nodes(self):
        r, g = graph.Node('root'), graph.Node('goal')
        r.children.add(g)
        paths = self.search_function(r, lambda n: n == g)

        self.assertEquals([r, g], paths.next())
        self.assertRaises(StopIteration, paths.next)


    def test_two_disjunct_nodes(self):
        r, g = graph.Node('root'), graph.Node('goal')
        paths = self.search_function(r, lambda n: n == g)
        
        self.assertRaises(StopIteration, paths.next)



class BreadthFirstSearchTests(unittest.TestCase, CommonSearchTestsMixin):
    def setUp(self):
        self.search_function = blind.breadth_first_search


    def test_two_branches_with_different_goal_depth(self):
        r = graph.Node("r")
        b1 = graph.create_branch("abcG")
        b2 = graph.create_branch("ABCDG")

        r.children.update(set([b1[0], b2[0]]))

        paths = blind.breadth_first_search(r, lambda n: n == graph.Node('G'))
        self.assertEquals([graph.Node(i) for i in "rabcG"], paths.next())
        self.assertEquals([graph.Node(i) for i in "rABCDG"], paths.next())
        self.assertRaises(StopIteration, paths.next)


class _MemoryNode(graph.Node): # inherit __eq__, __hash__
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
        


class TestMemoryNode(unittest.TestCase):
    def test_access(self):
        n = _MemoryNode(1)
        self.assertFalse(n.readFrom)
        n.children
        self.assertTrue(n.readFrom)


    def test_access_reset(self):
        n = _MemoryNode(1)
        n.children
        n.reset()
        self.assertFalse(n.readFrom)        


    def test_mutation(self):
        n = _MemoryNode(1)
        self.assertFalse(n.readFrom)
        n.children.add(_MemoryNode(2))
        self.assertTrue(n.readFrom)


    def test_mutation_reset(self):
        n = _MemoryNode(1)
        n.children.add(_MemoryNode(2))
        n.reset()
        self.assertFalse(n.readFrom)


    def test_assignment(self):
        n = _MemoryNode(1)
        self.assertFalse(n.writtenTo)
        n.children = set()
        self.assertTrue(n.writtenTo)


    def test_assignment_reset(self):
        n = _MemoryNode(1)
        n.children = set()
        n.reset()
        self.assertFalse(n.writtenTo)



class DepthFirstSearchTests(unittest.TestCase, CommonSearchTestsMixin):
    def setUp(self):
        self.search_function = blind.depth_first_search


    def test_parallel_branches_with_two_goals(self):
        r = graph.Node("r")
        b1, b2 = [graph.create_branch(i, node_class=_MemoryNode)
                  for i in ("abcdefG", "ABCDEFG")]
        r.children.update(set([b1[0], b2[0]]))

        for node in itertools.chain(b1, b2):
            node.reset() # create_branch accesses children

        paths = self.search_function(r, lambda n: n == b1[-1])

        pickedPath = paths.next() # generator is lazy

        self.assertTrue(all(n1.readFrom ^ n2.readFrom)
                        for n1, n2 in itertools.izip(b1[:-1], b2[:-1]))
        
        picked, notPicked = [b1, b2] if b1[0].readFrom else [b2, b1]

        for step in picked[:-1]:
            self.assertTrue(step.readFrom)

        for step in notPicked[:-1]:
            self.assertFalse(step.readFrom)

        notPickedPath = paths.next()
        
        for step in notPicked[:-1]:
            self.assertTrue(step.readFrom)

        self.assertRaises(StopIteration, paths.next)