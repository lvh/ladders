import sqlite3
import unittest

from ladders import cache


class TestLikePatterns(unittest.TestCase):
	def test_single_character(self):
		patterns = cache._find_like_patterns("A")
		self.assertEqual(patterns, [])


	def test_word(self):
		patterns = cache._find_like_patterns("ABCDE")
		self.assertEqual(patterns, ["A_CDE", "AB_DE", "ABC_E", "ABCD_"])



class TestExactMatches(unittest.TestCase):
	def test_word(self):
		matches = set(cache._find_exact_matches("ABC"))
		self.assertNotIn("ABC", matches)
		self.assertEqual(len(matches), 25) # each letter except A



class TestCache(unittest.TestCase):
	def test_cache(self):
		db = sqlite3.connect(":memory:")
		c = cache.Cache(db)
		c.add_words(["AAA", "AAB", "AAC", "AAD", "ABB", "ABA"])
		adjacent_words = set(c.find_adjacent_words("AAA"))
		for negative in ["AAA", "ABB"]:
			self.assertNotIn(negative, adjacent_words)
		for positive in ["AAB", "AAC", "AAD", "ABA"]:
			self.assertIn(positive, adjacent_words)
