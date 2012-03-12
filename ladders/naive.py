"""
A naive word ladder algorithm.
"""

def find_ladder(start, target, words):
    """
    Naive word ladder algorithm.

    Does linear search over ``words`` for each step in the ladder.
    """
    current, ladder = start, [start]

    while current != target:
        current = _find_next(current, target, words)
        ladder.append(current)

    return ladder


def _distance(word_one, word_two):
    return sum(1 for (x, y) in zip(word_one, word_two) if x != y)


def _find_next(current, target, words):
    current_distance = _distance(current, target)

    for candidate in words:
        closer = _distance(candidate, target) < current_distance
        if closer and _distance(current, candidate) == 1:
            return candidate
    else:
        raise ValueError("can't find the next step in the word ladder")
