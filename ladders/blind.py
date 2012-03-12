#!-*- encoding: utf-8 -*-
"""
Functions of searching blindly in a search tree.
"""
import logging
import collections

from ladders import graph


log = logging.getLogger('graphsearch.blind')


def _acyclic_extended_paths(path):
    """
    Returns the extended paths of a given path that do not have any cycles.
    """
    for new_path in graph.extended_paths(path):
        if not graph.has_new_cycle(new_path):
            yield new_path


def _depth_first_expander(path, queue):
    """
    A queue expander that results in a depth-first search.
    """
    log.info("expanding queue depth-first for path %r" % (path,))
    queue.extendleft(_acyclic_extended_paths(path))



def depth_first_search(root, goal):
    """
    Tries to find paths from the root node to a node satisfying the goal
    condition using depth-first search.
    """
    log.info("starting depth-first search from %r" % (root,))
    return _generic_search(root, goal, _depth_first_expander)



def _breadth_first_expander(path, queue):
    """
    A queue expander that results in a breadth-first search.
    """
    log.info("expanding queue breadth-first for path %r" % (path,))
    queue.extend(_acyclic_extended_paths(path))



def breadth_first_search(root, goal):
    """
    Tries to find paths from the root node to a node satisfying the goal
    condition using breadth-first search.
    """
    log.info("starting breadth-first search from %r" % (root,))
    return _generic_search(root, goal, _breadth_first_expander)



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