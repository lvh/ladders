import functools
import itertools
import unittest

from ladders import graph, heuristic
from ladders.test import memorynode


class HeuristicTest(unittest.TestCase):
    def test_heuristic(self):
        """
        Tests that branches are visited according to the heuristic.
        """
        root = graph.Node("r")
        left, right = map(memorynode.create_branch, ["vwxyzG", "abcdeG"])
        root.children.update(set([left[0], right[0]]))
        for node in itertools.chain(left, right):
            node.reset()

        def goal(node):
            return node.name == "G"

        def _heuristic(path):
            """
            Uses the ordinal value of the node name.

            This means "abcde" comes before "vwxyz".
            """
            return ord(path[-1].name)

        paths = heuristic.heuristic_search(root, goal, _heuristic)
        paths.next()

        for step in left:
            self.assertFalse(step.readFrom)

        for step in right[:-1]:
            # final node is a goal, so children never get accessed
            self.assertTrue(step.readFrom)

        paths.next()

        for step in left[:-1]:
            self.assertTrue(step.readFrom)