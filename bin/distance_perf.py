import timeit

distance_functions = []

def distance_func(f):
    distance_functions.append(f)
    return f

@distance_func
def distance_sum(a, b):
    return sum(1 for (x, y) in zip(a, b) if x != y)

@distance_func
def distance_sum2(a, b):
    return sum(x != y for (x, y) in zip(a, b))

@distance_func
def distance_simple(a, b):
    s = 0
    for (x, y) in zip(a, b):
        s += x != y
    return s

@distance_func
def distance_sum_lc(a, b):
    return sum([1 for (x, y) in zip(a, b) if x != y])

@distance_func
def distance_sum2_lc(a, b):
    return sum([x != y for (x, y) in zip(a, b)])

samples = [
    ("pig", "wig"),
    ("pig", "sty"),
    ("aaaaaaaaaaaaaa", "aaaaaaaaaaaaaa"),
    ("aaaaaaaaaaaaaa", "aaaaaaaaaaaaab")
]

def measure():
    for f in distance_functions:
        print "Measuring function {}".format(f)
        setup = "from __main__ import {} as f".format(f.__name__)

        total = 0
        for a, b in samples:
            statement = "f({!r}, {!r})".format(a, b)
            partial = timeit.Timer(statement, setup).timeit()
            print "{} vs {}: {}s".format(a, b, partial)
            total += partial

        print "Total time: {}".format(total)

if __name__ == "__main__":
    measure()