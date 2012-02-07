#!/usr/bin/env python

import Levenshtein, MySQLdb, sys, zlib

INSERT = """INSERT INTO similarity VALUES (%s, %s, %s, %s, %s, %s)"""

SELECT = """SELECT x.idx, y.idx, x.tunedata, y.tunedata
  FROM search_abc AS x
    JOIN search_abc AS y ON x.idx != y.idx
  WHERE x.tunetype='jig' AND y.tunetype='jig'"""

def ncd(x, y):
    try:
        cx = float(sys.getsizeof(zlib.compress(x)))
        cy = float(sys.getsizeof(zlib.compress(y)))
        cxy = float(sys.getsizeof(zlib.compress(x + y)))

        return (cxy - min(cx, cy)) / max(cx, cy)
    except:
        return -1

def hamming(x, y):
    if len(x) != len(y):
        return -1

    return sum(c1 != c2 for c1, c2 in zip(x, y))

# Taken from http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Longest_common_substring#Python
def LongestCommonSubstring(S1, S2):
    M = [[0]*(1+len(S2)) for i in xrange(1+len(S1))]
    longest, x_longest = 0, 0
    for x in xrange(1,1+len(S1)):
        for y in xrange(1,1+len(S2)):
            if S1[x-1] == S2[y-1]:
                M[x][y] = M[x-1][y-1] + 1
                if M[x][y]>longest:
                    longest = M[x][y]
                    x_longest  = x
            else:
                M[x][y] = 0
    return S1[x_longest-longest: x_longest]

if __name__ == '__main__':
    conn = MySQLdb.connect(user='root', db=sys.argv[1])
    c1 = conn.cursor()
    c2 = conn.cursor()

    c1.execute(SELECT)
    for tuneid, comparedtoid, tunedata, comparedtodata in c1:
        print "%d | %d" % (tuneid, comparedtoid)
        c2.execute(INSERT,
                (tuneid,
                    comparedtoid,
                    ncd(tunedata, comparedtodata),
                    hamming(tunedata, comparedtodata),
                    Levenshtein.distance(tunedata, comparedtodata),
                    LongestCommonSubstring(tunedata, comparedtodata)))

    print 'Done.'
    conn.commit()
    c1.close()
    c2.close()
    conn.close()
