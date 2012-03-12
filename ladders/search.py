"""
Generic graph search algorithms.
"""
import collections
import logging

from ladders import graph


log = logging.getLogger('ladders.search')


def _acyclic_extended_paths(path):
    """
    Returns the extended paths of a given path that do not have any cycles.
    """
    for new_path in graph.extended_paths(path):
        if not graph.has_new_cycle(new_path):
            yield new_path


def _generic_search(root, goal, expander):
    """
    A generic search tree pathfinder.

    Returns an iterable of paths that end in a goal state.
    """
    queue = collections.deque([[root]])

    while queue:
        path = queue.popleft()
        log.info("considering path %r" % (path,))

        if goal(path[-1]):
            log.info("found a path that reaches goal state %r" % (path[-1],))
            yield path

        if not path[-1].children:
            log.info("path is a dead end, ignoring")
            continue

        expander(path, queue)
