import argparse
import logging
import sqlite3

from ladders import cache, naive, heuristic


algorithms = {
	"depth-first": naive.depth_first,
	"breadth-first": naive.breadth_first,
	"heuristic": heuristic.find_ladders
}


get_algorithm = lambda t: algorithms.get(t) # sigh, argparse. You can't use
# algorithms.get; that gives you an unhashable type ('dict') error. Brownie
# points if you can figure out why.


def parse_word_list(fn):
	with open(fn) as f:
		return [word.strip().upper() for word in f]


def make_cache(fn):
	if fn is not None:
		return cache.Cache(sqlite3.connect(fn))
	else:
		return None


parser = argparse.ArgumentParser(description="Find word ladders")

parser.add_argument('start', metavar='START',
	action='store', type=str.upper,
	help='the start of the word ladder')
parser.add_argument('target', metavar='TARGET',
	action='store', type=str.upper,
	help='the target of the word ladder')
parser.add_argument('-a, --algorithm', dest='algorithm', metavar="ALGO",
	action='store', type=get_algorithm, default=heuristic.find_ladders,
    help='method to use for finding the word ladders')
parser.add_argument('-o, --optimal', dest="optimal",
	action='store_true',
	help='if set, finds the shortest possible ladder')
parser.add_argument('-w, --word-list', dest="words",
	action='store', type=parse_word_list)
parser.add_argument('-c, --cache', dest="cache",
	action='store', type=make_cache)
parser.add_argument('-v, --verbose', dest="verbose",
	action='store_true',
	help='verbose logging')

def main():
	args = parser.parse_args()

	level = (logging.DEBUG if args.verbose else logging.ERROR)
	logging.basicConfig(level=level)

	if args.cache is not None and args.words is not None:
		args.cache.add_words(args.words)

	ladders = args.algorithm(args.start, args.target, args.words, args.cache)

	if args.optimal:
		ladder = min(ladders, key=len)
	else:
		ladder = ladders.next()

	if not args.verbose:
		print "{} {} {}".format(args.start, args.target, len(ladder))
	else:
		print ladder