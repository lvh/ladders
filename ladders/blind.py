#!-*- encoding: utf-8 -*-
"""
Functions of searching blindly in a search tree.
"""
import logging

from ladders import search


log = logging.getLogger('ladders.blind')


def _depth_first_expander(path, queue):
    """
    A queue expander that results in a depth-first search.
    """
    log.info("expanding queue depth-first for path %r" % (path,))
    queue.extendleft(search._acyclic_extended_paths(path))


def depth_first_search(root, goal):
    """
    Tries to find paths from the root node to a node satisfying the goal
    condition using depth-first search.
    """
    log.info("starting depth-first search from %r" % (root,))
    return search._generic_search(root, goal, _depth_first_expander)


def _breadth_first_expander(path, queue):
    """
    A queue expander that results in a breadth-first search.
    """
    log.info("expanding queue breadth-first for path %r" % (path,))
    queue.extend(search._acyclic_extended_paths(path))


def breadth_first_search(root, goal):
    """
    Tries to find paths from the root node to a node satisfying the goal
    condition using breadth-first search.
    """
    log.info("starting breadth-first search from %r" % (root,))
    return search._generic_search(root, goal, _breadth_first_expander)
