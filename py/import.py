#!/usr/bin/env python

import sys, sqlite3


def insert(line, c):
    toks = eval(line)
    c.execute('insert into search_abc values (?, ?, ?, ?, ?, ?)', toks)

    
if __name__ == '__main__':
    conn = sqlite3.connect(sys.argv[1])
    conn.text_factory = str
    c = conn.cursor()

    with file(sys.argv[2]) as f:
        for line in f:
            insert(line, c)

        conn.commit()
        c.close()
