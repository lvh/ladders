import unittest
from ladders import heuristic, naive

red_herrings = {
    4: ["lord", "text", "tarp", "dork", "moon", "trap", "trip", "code"]
}


samples = [
    ['cold', 'cord', 'card', 'ward', 'warm'],
    ["head", "heal", "teal", "tell", "tall", "tail"],
    ['heap', 'heat', 'peat', 'pert', 'port', 'sort'],
    ['like', 'bike', 'bake', 'rake', 'rate']
]



class _LadderTest(object):
    def _test(self, words, expected):
        """
        Tests all implementations with the given word list.
        """
        start, target = expected[0], expected[-1]
        ladders = self.find_ladders(start, target, words)
        for ladder in ladders:
            names = [node.name for node in ladder]
            self.assertEqual(names, expected)


    def test_ladder(self):
        for words in samples:
            self._test(words, words)


    def test_with_herrings(self):
        for words in samples:
            self._test(words + red_herrings[len(words[0])], words)



class BreadthFirstTest(_LadderTest, unittest.TestCase):
    find_ladders = staticmethod(naive.breadth_first)



class DepthFirstTest(_LadderTest, unittest.TestCase):
    find_ladders = staticmethod(naive.depth_first)



class HeuristicTest(_LadderTest, unittest.TestCase):
    find_ladders = staticmethod(heuristic.find_ladders)
