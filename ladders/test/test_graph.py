#-*- encoding: utf-8 -*-
"""
Test cases for the basic graph components.
"""
import itertools
import unittest

from ladders import graph


class NodeTests(unittest.TestCase):
    def setUp(self):
        self.n1, self.n2, self.n3 = (graph.Node(i) for i in (1, 1, 2))


    def test_empty_nodes(self):
        """
        Tests that nodes start empty by default.
        """
        for node in self.n1, self.n2, self.n3:
            self.assertFalse(node.children)


    def test_equality(self):
        """
        Tests that nodes with the same name are equal.
        """
        for x in (self.n1, self.n2, self.n3):
            self.assertEquals(x, x)

        self.assertEquals(self.n1, self.n2)


    def test_inequality(self):
        """
        Tests that nodes with different names are not equal.
        """
        self.assertNotEquals(self.n1, self.n3)
        self.assertNotEquals(self.n2, self.n3)


    def test_path_equality(self):
        """
        Tests that equal paths compare equal.
        """
        self.assertEquals([graph.Node('root')], [graph.Node('root')])
        self.assertEquals([graph.Node(i) for i in xrange(10)],
                          [graph.Node(i) for i in xrange(10)])


    def test_path_inequality(self):
        """
        Tests that different paths compare unequal.
        """
        self.assertNotEquals([graph.Node('root')], [graph.Node('goal')])
        path_one = [graph.Node(i) for i in xrange(10)]
        path_two = [graph.Node(i) for i in xrange(10)]
        self.assertEquals(path_one, path_two)


    def test_add_children(self):
        """
        Tests that children can be added after the node has been created.
        """
        parent, child = (graph.Node(id) for id in ("parent", "child"))
        parent.children.add(child)
        self.assertTrue(child in parent.children)


    def test_hash_in_set(self):
        nodes = set([self.n1, self.n2, self.n3])
        self.assertEquals(len(nodes), 2)


    def test_equal_hash(self):
        self.assertEquals(hash(self.n1), hash(self.n1))
        self.assertEquals(hash(self.n1), hash(self.n2))


    def test_unequal_hash(self):
        self.assertNotEquals(hash(self.n1), hash(self.n3))
        self.assertNotEquals(hash(self.n2), hash(self.n3))



class BranchCreationTests(unittest.TestCase):
    def _test(self, identifiers):
        path = graph.create_branch(identifiers)
        self.assertEquals(len(path), len(identifiers))
        self.assertFalse(path[-1].children)
        self.assertFalse(graph.has_cycle(path))


    def test_one_element(self):
        """
        Tests what happens when you try to create a one-element branch.
        """
        self._test(xrange(1))


    def test_many_elements(self):
        """
        Tests what happens when you try to create a ten-element branch.
        """
        self._test(xrange(10))



class PathExtensionTests(unittest.TestCase):
    def test_childless_root(self):
        """
        Tests that the set of extended paths of a path consisting of a single
        root node with no children is empty.
        """
        extended_paths = graph.extended_paths([graph.Node(1)])
        self.assertRaises(StopIteration, extended_paths.next)


    def test_leaf(self):
        """
        Tests that the extended path node of a leaf (which is not the root)
        node is empty.
        """
        n1, n2, n3 = (graph.Node(i) for i in xrange(3))
        n1.children.add(n2)
        n2.children.add(n3)

        extended_paths = graph.extended_paths([n1, n2, n3])
        self.assertRaises(StopIteration, extended_paths.next)


    def test_bogus_branches(self):
        """
        Tests that the extended path node of a leaf (which is not the root)
        node is empty, even when there are a few unrelated branches.
        """
        n1, n2, n3 = (graph.Node(i) for i in xrange(3))
        n1.children.add(n2)
        n2.children.add(n3)

        n1.children.add(graph.create_branch("abcdefg")[0])
        n2.children.add(graph.create_branch("ABCDEFGHIJK")[0])


        extended_paths = graph.extended_paths([n1, n2, n3])
        self.assertRaises(StopIteration, extended_paths.next)


    def test_many_children(self):
        root = graph.Node(-1)
        newChildren = set(graph.Node(i) for i in xrange(10))
        root.children.update(newChildren)

        basePath = [root]
        extended_paths = list(graph.extended_paths(basePath))
        self.assertEquals(len(extended_paths), len(newChildren))

        for extendedPath in map(list, extended_paths):
            self.assertEquals(len(extendedPath), len(basePath) + 1)



class CycleTests(unittest.TestCase):
    def setUp(self):
        self.nodes = [graph.Node(i) for i in xrange(10)]


    def test_no_cycle(self):
        self.assertFalse(graph.has_cycle(self.nodes))
        self.assertFalse(graph.has_new_cycle(self.nodes))


    def _test_has_cycle(self, ids):
        """
        Generalized case for verifying cyclic paths are detected.
        """
        self.assertTrue(graph.has_cycle([self.nodes[i] for i in ids]))


    def _test_has_new_cycle(self, ids):
        """
        Generalized case for verifying some cyclic paths (where the cycle is
        introduced at the end) are detected.
        """
        self.assertTrue(graph.has_new_cycle([self.nodes[i] for i in ids]))


    def _test_hasNoNewCycle(self, ids):
        """
        Generalized case for verifying some possibly cyclic paths (where the
        cycle is not introduced at the end, or there is no cycle to be found)
        are detected.
        """
        self.assertFalse(graph.has_new_cycle([self.nodes[i] for i in ids]))


    def test_at_start(self):
        ids = [1, 1, 2, 3, 4, 5, 6]
        self._test_has_cycle(ids)
        self._test_hasNoNewCycle(ids)


    def test_at_end(self):
        ids = [1, 2, 3, 4, 5, 6, 1]
        self._test_has_cycle(ids)
        self._test_has_new_cycle(ids)


    def test_long_cycle_at_start(self):
        ids = [1, 2, 1, 3, 4, 5, 6]
        self._test_has_cycle(ids)
        self._test_hasNoNewCycle(ids)


    def test_two_sequential_middle_cycles(self):
        ids = [1, 2, 3, 2, 4, 5, 4, 6]
        self._test_has_cycle(ids)
        self._test_hasNoNewCycle(ids)


    def test_two_nested_middle_cycles(self):
        ids = [1, 2, 3, 2, 3, 4, 5, 6]
        self._test_has_cycle(ids)
        self._test_hasNoNewCycle(ids)


    def test_two_sequential_end_cycles(self):
        ids = [1, 2, 3, 2, 4, 5, 6, 5]
        self._test_has_cycle(ids)
        self._test_has_new_cycle(ids)


    def test_two_nested_end_cycles(self):
        ids = [1, 2, 3, 4, 5, 2, 6, 5]
        self._test_has_cycle(ids)
        self._test_has_new_cycle(ids)


    def test_infinite_cycle(self):
        path = itertools.cycle([graph.Node(i) for i in xrange(3)])
        self.assertTrue(graph.has_cycle(path))
