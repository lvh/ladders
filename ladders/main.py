import argparse
import logging

from ladders import naive, heuristic


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
parser.add_argument('-v, --verbose', dest="verbose",
	action='store_true',
	help='verbose logging')

def main():
	args = parser.parse_args()

	if args.verbose:
		logging.basicConfig()

	ladders = args.algorithm(args.start, args.target, args.words)

	if args.optimal:
		ladder = min(ladders, key=len)
	else:
		ladder = ladders.next()

	if not args.verbose:
		print "{} {} {}".format(ladder[0], ladder[-1], len(ladder))
	else:
		print ladder