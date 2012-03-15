"""
A SQLite-based word adjacency cache.
"""
import string


UPPERCASE = frozenset(string.ascii_uppercase)



class Cache(object):
    def __init__(self, db):
        self.db = db
        db.execute("CREATE TABLE IF NOT EXISTS words (word TEXT PRIMARY KEY)")
        db.execute("PRAGMA case_sensitive_like=1;")


    def add_words(self, words):
        tuples = ((word,) for word in words)
        self.db.executemany("INSERT OR IGNORE INTO words VALUES (?)", tuples)
        self.db.commit()


    def find_adjacent_words(self, word):
        query = """SELECT word FROM words
            WHERE word != ? AND (({exact}) OR ({pattern}))"""

        exact_match_clause = "word IN ({})".format(",".join("?" * 25))
        like_clause = " OR ".join(["(word LIKE ?)"] * (len(word) - 1))

        exact_matches = _find_exact_matches(word)
        like_patterns = _find_like_patterns(word)

        query = query.format(exact=exact_match_clause, pattern=like_clause)
        params = [word] + exact_matches + like_patterns
        cursor = self.db.execute(query, params)
        return (word.encode("ascii") for (word,) in cursor)



def _find_exact_matches(word):
    pattern = "{{}}{}".format(word[1:])
    return [pattern.format(c) for c in UPPERCASE - set(word[0])]


def _find_like_patterns(word):
    return [_replace(word, idx) for idx in xrange(1, len(word))]


def _replace(string, index, character="_"):
    b = bytearray(string)
    b[index] = character
    return str(b)
