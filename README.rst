=========
 ladders
=========

This is an entry in the Benefitfocus word ladders competition.

Usage
=====

The ``ladder`` script lives in the ``bin/`` directory.

Basic information on the command line arguments can be found by passing the ``-h`` or ``--help`` flags.

In it's simplest form, it takes two words (the start and target of the word ladder) and a word list::

    ladder PIG STY -w words

And it will print out something like::

    PIG STY 6


Algorithms
==========

The word ladders are found by graph search. This implementation comes with three different algorithms, which can be specified with the ``--algorithm`` flag (shorthand ``-a``):

    - depth-first
    - breadth-first
    - heuristic (default)

Heuristic search will sort by the number of letters by which a candidate word differs from the target word::

    d("aaa", "aaa") == 0
    d("aaa", "aab") == 1
    d("abc", "xyz") == 3

Profiling has found out that in many cases the distance metric ends up being a bottleneck. It has been optimized somewhat, but particularly for long words where the word list is not significantly longer than the ladder length, depth-first or breadth-first can be much faster.

The distance function optimization can be found in ``bin/distance_perf.py``.


Caching
=======

For large (empirically ~5k+) word lists where you want to find multiple ladders, you can store a SQLite cache of the adjacency information. This can produce large speedups, particularly on cases where the word list contains words of different length. (The indexing structure is sufficiently smart that this doesn't really affect performance, however the default linear search algorithm is not.)

To build the cache, pass the ``--cache`` (shorthand: ``-c``) option together with a word list. To use a cache that's already been built, just pass the cache argument without a word list.
