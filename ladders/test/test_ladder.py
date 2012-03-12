import unittest
from ladders import naive

red_herrings = {
    4: ["lord", "lard", "rare", "dork", "moon", "trap", "trip"]
}

class _LadderTest(object):
    implementations = [naive.find_ladder]

    def _test(self, words, expected):
        """
        Tests all implementations with the given word list.
        """
        for find_ladder in self.implementations:
            ladder = find_ladder(self.start, self.target, words)
            self.assertEqual(ladder, expected)


    def test_ladder(self):
        self._test(self.words, self.words)


    def test_with_herrings(self):
        length = len(self.words[0])
        self._test(self.words + red_herrings[length], self.words)



class ColdWarmTest(_LadderTest, unittest.TestCase):
    start, target = "cold", "warm"
    words = ['cold', 'cord', 'card', 'ward', 'warm']



class HeadTailTest(_LadderTest, unittest.TestCase):
    start, target = "head", "tail"
    words = ["head", "heal", "teal", "tell", "tall", "tail"]



class HeapSortTest(_LadderTest, unittest.TestCase):
    start, target = "heap", "sort"
    words = ['heap', 'heat', 'peat', 'pert', 'port', 'sort']
