"""
Tests for generic test tools.
"""
import unittest

from ladders import graph, search


class AcyclicExtendedPathTests(unittest.TestCase):
    def test_single_root_node(self):
        r = graph.Node(0)
        aep = search._acyclic_extended_paths([r])

        self.assertRaises(StopIteration, aep.next) # 0 children


    def test_self_referencing_root_node(self):
        """
        Tests the acyclic extended path of a node that has itself as a child.
        """
        r = graph.Node(0)
        r.children.add(r)
        aep = search._acyclic_extended_paths([r])

        self.assertRaises(StopIteration, aep.next) # 1 child, 1 cycle


    def test_two_nodes(self):
        r, c = [graph.Node(i) for i in (0, 1)]
        r.children.add(c)

        aep = search._acyclic_extended_paths([r])

        self.assertEquals([r, c], aep.next())
        self.assertRaises(StopIteration, aep.next) # 1 child, 1 cycle


    def test_unlinked_branches(self):
        branchids = (xrange(*r) for r in ((0, 10), (10, 20), (20, 30)))
        b1, b2, b3 = (graph.create_branch(id) for id in branchids)
        r = graph.Node("root")
        for child in b1[0], b2[0], b3[0]:
            r.children.add(child)

        aep = search._acyclic_extended_paths([r])
        self.assertTrue(expectedPath in aep for expectedPath in
                        [[r, b1[0]], [r, b2[0]], [r, b3[0]]])

        aep = search._acyclic_extended_paths([r, b1[0]])
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

        aep = list(search._acyclic_extended_paths([r]))
        self.assertEquals(len(aep), 3) # 3 children, 0 cycles
        self.assertTrue(expectedPath in aep for expectedPath in
                        [[r, b1[0]], [r, b2[0]], [r, b3[0]]])

        aep = list(search._acyclic_extended_paths([r, b1[0]]))
        self.assertEquals(len(aep), 1)
        self.assertEquals(aep[0], [r, b1[0], b1[1]])

        badPath = [r, b1[0], b1[1], b2[0], b2[1]]
        aep = list(search._acyclic_extended_paths(badPath))
        self.assertEquals(len(aep), 1) # 2 children, 1 cycle
        self.assertEquals(aep[0], badPath + [b2[2]])