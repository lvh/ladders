"""
Heuristic-based graph search.
"""
import functools

from ladders import graph, search


def find_ladders(start, target, words):
	"""
	Find ladders heuristically.
	"""
	root = graph.LadderNode(start, words)

	def heuristic(path):
		return graph.distance(path[-1].name, target)

	def goal(node):
		return node.name == target

	expander = functools.partial(_heuristic_expander, heuristic=heuristic)
	return search._generic_search(root, goal, expander)


def _heuristic_expander(path, queue, heuristic):
	queue.extend(search._acyclic_extended_paths(path))
	return sorted(queue, key=heuristic)