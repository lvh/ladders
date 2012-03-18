import functools
import unittest

from ladders import graph, heuristic
from ladders.test import memorynode


class HeuristicTest(unittest.TestCase):
    def test_heuristic(self):
        """
        Tests that branches are visited according to the heuristic.
        """
        root = graph.node("r")

        branch = functools.partial(graph.create_branch, node_class=MemoryNode)
        left, right = map(branch, ["xyzG", "abcG"])
        root.children.update(set([left[0], right[0])))

        paths = heuristic.heuristic_search()
        paths.next()

        for step in left:
            self.assertFalse(step.readFrom)

        for step in right:
            self.assertTrue(step.readFrom)

        paths.next()

        for step in left:
            self.assertTrue(step.readFrom)