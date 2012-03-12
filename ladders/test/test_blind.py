#-*- encoding: utf-8 -*-
"""
Test cases for blind searching.
"""
import itertools
import unittest

from ladders import graph, blind


class AcyclicExtendedPathTests(unittest.TestCase):
    def test_single_root_node(self):
        r = graph.Node(0)
        aep = blind._acyclic_extended_paths([r])

        self.assertRaises(StopIteration, aep.next) # 0 children


    def test_self_referencing_root_node(self):
        """
        Tests the acyclic extended path of a node that has itself as a child.
        """
        r = graph.Node(0)
        r.children.add(r)
        aep = blind._acyclic_extended_paths([r])

        self.assertRaises(StopIteration, aep.next) # 1 child, 1 cycle


    def test_two_nodes(self):
        r, c = [graph.Node(i) for i in (0, 1)]
        r.children.add(c)

        aep = blind._acyclic_extended_paths([r])

        self.assertEquals([r, c], aep.next())
        self.assertRaises(StopIteration, aep.next) # 1 child, 1 cycle


    def test_unlinked_branches(self):
        branchids = (xrange(*r) for r in ((0, 10), (10, 20), (20, 30)))
        b1, b2, b3 = (graph.create_branch(id) for id in branchids)
        r = graph.Node("root")
        for child in b1[0], b2[0], b3[0]:
            r.children.add(child)

        aep = blind._acyclic_extended_paths([r])
        self.assertTrue(expectedPath in aep for expectedPath in
                        [[r, b1[0]], [r, b2[0]], [r, b3[0]]])

        aep = blind._acyclic_extended_paths([r, b1[0]])
        self.assertEquals([r, b1[0], b1[1]], aep.next())
        self.assertRaises(StopIteration, aep.next)


    def test_linked_branches(self):
        branchids = (xrange(*r) for r in ((0, 10), (10, 20), (20, 30)))
        b1, b2, b3 = (graph.create_branch(id) for id in branchids)
        r = graph.Node("root")
        for child in b1[0], b2[0], b3[0]:
            r.children.add(child)

        # introduce a cycle
        b1[1].children.add(b2[0])
        b2[1].children.add(b1[0])

        aep = list(blind._acyclic_extended_paths([r]))
        self.assertEquals(len(aep), 3) # 3 children, 0 cycles
        self.assertTrue(expectedPath in aep for expectedPath in
                        [[r, b1[0]], [r, b2[0]], [r, b3[0]]])

        aep = list(blind._acyclic_extended_paths([r, b1[0]]))
        self.assertEquals(len(aep), 1)
        self.assertEquals(aep[0], [r, b1[0], b1[1]])

        badPath = [r, b1[0], b1[1], b2[0], b2[1]]
        aep = list(blind._acyclic_extended_paths(badPath))
        self.assertEquals(len(aep), 1) # 2 children, 1 cycle
        self.assertEquals(aep[0], badPath + [b2[2]])



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