#!/usr/bin/env python

from tempfile import NamedTemporaryFile
import Levenshtein, sqlite3, sys, zlib

NCD_TABLE = """CREATE TABLE IF NOT EXISTS similarity (
  tuneid INTEGER,
  comparedtoid INTEGER,
  ncd REAL,
  hamming INTEGER,
  levenshtein INTEGER,
  PRIMARY KEY(tuneid, comparedtoid),
  FOREIGN KEY(tuneid) REFERENCES search_abc(id),
  FOREIGN KEY(comparedtoid) REFERENCES search_abc(id)
)"""

INSERT = """INSERT INTO similarity VALUES (?, ?, ?, ?, ?)"""

SELECT = """SELECT x.id, y.id, x.tunedata, y.tunedata
  FROM search_abc AS x
    JOIN search_abc AS y ON x.id != y.id
  WHERE x.tunetype='polka'"""

SELECT_START = """SELECT max(tuneid) FROM ncd"""

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

if __name__ == '__main__':
    conn = sqlite3.connect(sys.argv[1])
    c = conn.cursor()

    with NamedTemporaryFile() as tmpdb:
        tmp = sqlite3.connect(tmpdb.name)
        ctmp = tmp.cursor()
        ctmp.execute(NCD_TABLE)

        c.execute(SELECT)

        for tuneid, comparedtoid, tunedata, comparedtodata in c:
            print "%d | %d" % (tuneid, comparedtoid)
            ctmp.execute(INSERT,
                    (tuneid,
                        comparedtoid,
                        ncd(tunedata, comparedtodata),
                        hamming(tunedata, comparedtodata),
                        Levenshtein.distance(tunedata, comparedtodata)))

        ctmp.execute('select * from similarity')
        for row in ctmp:
            c.execute(INSERT, row)

    print 'Done.'
    conn.commit()
    c.close()
