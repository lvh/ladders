#!-*- encoding: utf-8 -*-
"""
A naive word ladder algorithm.
"""
import functools

from ladders import blind, graph


def _find_ladders(search, start, target, words):
    """
    Naive word ladder algorithm that finds ladders by depth-first search.
    """
    root = graph.LadderNode(start, words)
    def goal(node):
        return node.name == target
    return search(root, goal)


breadth_first, depth_first = [functools.partial(_find_ladders, s)
    for s in [blind.depth_first_search, blind.breadth_first_search]]