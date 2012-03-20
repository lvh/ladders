=========
 ladders
=========

This is an entry in the Benefitfocus word ladders competition.

Usage
=====

The ``ladder`` script lives in the ``bin/`` directory.

Basic information on the command line arguments can be found by
passing the ``-h`` or ``--help`` flags.

In it's simplest form, it takes two words (the start and target of the
word ladder) and a word list::

    ladder PIG STY -w words

And it will print out something like::

    PIG STY 6

Examples
========

This entry comes with a few sample dictionaries to get started
quickly. From the package root, try::

    PYTHONPATH="." bin/ladder RICH POOR -v -w samples/four

The ``-v`` flag enables verbose mode, displaying the paths taken along
the way to finding a solution.

To see the effect of the heuristic algorithm (for more information on
the algorithms, see below), try a depth-first one instead::

    PYTHONPATH="." bin/ladder RICH POOR -v -w samples/four -a depth-first

``samples/four`` is just a list of all words of length four in
``/usr/share/dict/words`` on an OS X Lion machine, converted to
uppercase and then ``sort``ed and ``uniq``ed.

Algorithms
==========

The word ladders are found by graph search. This implementation comes
with three different algorithms, which can be specified with the
``--algorithm`` flag (shorthand ``-a``):

    - depth-first
    - breadth-first
    - heuristic (default)

Heuristic search will sort by the number of letters by which a
candidate word differs from the target word::

    d("aaa", "aaa") == 0
    d("aaa", "aab") == 1
    d("abc", "xyz") == 3

Profiling has found out that in many cases the distance metric ends up
being a bottleneck. It has been optimized somewhat, but particularly
for long words where the word list is not significantly longer than
the ladder length, depth-first or breadth-first can be slightly faster.

The distance function optimization can be found in ``bin/distance_perf.py``.

Any algorithm can be told to exhaustively search for an optimal
solution. This currently does `not` prune paths that are longer than
an already found path, so any algorithm will effectively walk the
entire node space. This is an area suitable for improvement without
too much effort, however, no time was spent here because the original
question did not ask for optimal solutions.

Caching
=======

For large (empirically ~5k+) word lists where you want to find
multiple ladders, you can store a SQLite cache of the adjacency
information. This can produce large speedups, particularly on cases
where the word list contains words of different length. (The indexing
structure is sufficiently smart that this doesn't really affect
performance, however the default linear search algorithm is not.)

To build the cache, pass the ``--cache`` (shorthand: ``-c``) option
together with a word list. To use a cache that's already been built,
just pass the cache argument without a word list.

Credits
=======

All code in the package is originally authored and still has the
copyright held by the contest applicant, Laurens Van Houtven. An
earlier version of the graph search code (without heuristic search) is
available under a liberal license on Launchpad under
``lp:~lvh/graphsearch/trunk``.

License
=======

See the ``LICENSE`` file for details.

