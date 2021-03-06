#-*- encoding: utf-8 -*-
"""
Test cases for blind searching.
"""
import itertools
import unittest

from ladders import graph, blind
from ladders.test import memorynode


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



class DepthFirstSearchTests(unittest.TestCase, CommonSearchTestsMixin):
    def setUp(self):
        self.search_function = blind.depth_first_search


    def test_parallel_branches_with_two_goals(self):
        root = graph.Node("root")
        left, right = map(memorynode.create_branch, ("abcdefG", "ABCDEFG"))
        root.children.update(set([left[0], right[0]]))

        for node in itertools.chain(left, right):
            node.reset() # create_branch accesses children

        paths = self.search_function(root, lambda n: n == left[-1])
        picked_path = paths.next() # generator is lazy

        self.assertTrue(all(n1.readFrom ^ n2.readFrom)
                        for n1, n2 in itertools.izip(left[:-1], right[:-1]))
        
        picked, not_picked = [left, right] if left[0].readFrom else [right, left]

        for step in picked[:-1]:
            self.assertTrue(step.readFrom)

        for step in not_picked[:-1]:
            self.assertFalse(step.readFrom)

        not_picked_path = paths.next()

        for step in not_picked[:-1]:
            self.assertTrue(step.readFrom)

        self.assertRaises(StopIteration, paths.next)
