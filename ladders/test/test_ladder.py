import unittest
from ladders import heuristic, naive

red_herrings = {
    3: ['CAD', 'TRY', 'POT', 'NOT', 'ROT', 'TOT', 'COT'],
    4: ['LORD', 'TEXT', 'TARP', 'DORK', 'MOON', 'TRAP', 'TRIP', 'CODE']
}


samples = [
    ['COLD', 'CORD', 'CARD', 'WARD', 'WARM'],
    ['HEAD', 'HEAL', 'TEAL', 'TELL', 'TALL', 'TAIL'],
    ['HEAP', 'HEAT', 'PEAT', 'PERT', 'PORT', 'SORT'],
    ['LIKE', 'BIKE', 'BAKE', 'RAKE', 'RATE'],
    ['PIG', 'WIG', 'WAG', 'WAY', 'SAY', 'STY'],
    ['FIVE', 'FIRE', 'FIRM', 'FORM', 'FOAM', 'FOAL', 'FOUL', 'FOUR']
]


def add_sample_tests(test_case):
    for words in samples:
        start, end = words[0], words[-1]

        name = "test_{}_{}_ladder".format(start, end)
        setattr(test_case, name, lambda self: self._test_ladder(words))

        name = "test_{}_{}_with_herrings".format(start, end)
        setattr(test_case, name, lambda self: self._test_with_herrings(words))

    return test_case



@add_sample_tests
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


    def _test_ladder(self, words):
        self._test(words, words)


    def _test_with_herrings(self, words):
        self._test(words + red_herrings[len(words[0])], words)



class BreadthFirstTest(_LadderTest, unittest.TestCase):
    find_ladders = staticmethod(naive.breadth_first)



class DepthFirstTest(_LadderTest, unittest.TestCase):
    find_ladders = staticmethod(naive.depth_first)



class HeuristicTest(_LadderTest, unittest.TestCase):
    find_ladders = staticmethod(heuristic.find_ladders)
