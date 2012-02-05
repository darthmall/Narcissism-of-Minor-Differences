#!/usr/bin/env python

from random import choice
import sys, sqlite3

SELECT_START = """SELECT DISTINCT tuneid
  FROM similarity WHERE levenshtein >= 0"""

SELECT_SIMILAR = """SELECT y.tunename, y.tunedata, s.ncd, s.hamming, s.levenshtein
  FROM search_abc AS y
    JOIN similarity AS s ON s.comparedtoid = y.id
   WHERE s.tuneid = ?
     AND s.levenshtein >= 0
   ORDER BY s.levenshtein asc
   LIMIT 5"""

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
    conn = sqlite3.connect(sys.argv[1])
    c = conn.cursor()

    c.execute(SELECT_START)
    tuneid = choice(c.fetchall())

    c.execute('SELECT tunename, tunedata FROM search_abc WHERE id=?', tuneid)
    name, abc = choice(c.fetchall())

    print '{:5d} {:5f} {:5d} {:30} {}'.format(0, 0.0, 0, name, abc)

    for r in c.execute(SELECT_SIMILAR, tuneid):
        print '{:5d} {:5d} {:5f} {:30} {} {}'.format(r[4], r[3], r[2], r[0], LongestCommonSubstring(abc, r[1]), r[1])

