import functools
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
    ['FIVE', 'FIRE', 'FIRM', 'FORM', 'FOAM', 'FOAL', 'FOUL', 'FOUR'],
    ['INK', 'INO', 'DNO', 'DUO', 'DUN', 'DEN', 'PEN'],
    ['NOSE', 'JOSE', 'JOIE', 'JOIN', 'COIN', 'CHIN'],
    ['DRY', 'DAY', 'BAY', 'BAT', 'BET', 'WET'],
    ['SOUP', 'SOUL', 'SAUL', 'HAUL', 'HARL', 'HARE'],
    ['PIE', 'PIG', 'BIG', 'BEG', 'BEL', 'EEL'],
    ['RICH', 'RICK', 'ROCK', 'SOCK', 'SOUK', 'SOUR', 'POUR', 'POOR'],
    ['APE', 'AUE', 'DUE', 'DUN', 'DAN', 'MAN'],
    ['HOT', 'HOA', 'KOA', 'KEA', 'TEA'],
    ['HAIR', 'LAIR', 'LAIE', 'LAME', 'CAME', 'COME', 'COMB'],
    ['OAK', 'OAR', 'FAR', 'FAY', 'FLY', 'ELY', 'ELM'],
    ['NAVY', 'NARY', 'MARY', 'MIRY', 'AIRY', 'AIRS', 'AIMS', 'ARMS', 'ARMY']
]


sample_tests = []


def add_sample_tests(test_case):
    for words in samples:
        start, end = words[0], words[-1]

        for f in sample_tests:
            base_name = f.__name__.lstrip("_test_")
            name = "test_{}_{}_{}".format(base_name, start, end)
            setattr(test_case, name, lambda self: f(self, words))

    return test_case


def sample_test(f):
    sample_tests.append(f)
    return f



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


    @sample_test
    def _test_ladder(self, words):
        self._test(words, words)


    @sample_test
    def _test_with_herrings(self, words):
        self._test(words + red_herrings[len(words[0])], words)



class BreadthFirstTest(_LadderTest, unittest.TestCase):
    find_ladders = staticmethod(naive.breadth_first)



class DepthFirstTest(_LadderTest, unittest.TestCase):
    find_ladders = staticmethod(naive.depth_first)



class HeuristicTest(_LadderTest, unittest.TestCase):
    find_ladders = staticmethod(heuristic.find_ladders)
