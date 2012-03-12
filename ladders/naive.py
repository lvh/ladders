#!-*- encoding: utf-8 -*-
"""
A naive word ladder algorithm.
"""
from ladders import blind, graph


class NaiveNode(graph.Node):
    def __init__(self, name, words):
        super(NaiveNode, self).__init__(name)
        self.words = words


    @property
    def children(self):
        child_words = [word for word in self.words if word != self.name]
        for word in child_words:
            if _distance(word, self.name) == 1:
                yield NaiveNode(word, child_words)


    @children.setter
    def children(self, words):
        self.words = words



def _distance(word_one, word_two):
    return sum(1 for (x, y) in zip(word_one, word_two) if x != y)


def find_ladders(start, target, words):
    """
    Naive word ladder algorithm.
    """
    root = NaiveNode(start, words)

    def goal(node):
        return node.name == target

    return blind.depth_first_search(root, goal)
