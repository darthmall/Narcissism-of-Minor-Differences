CREATE TABLE IF NOT EXISTS search_abc (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  tunename TEXT NOT NULL,
  tunelink TEXT NOT NULL,
  keysig TEXT NOT NULL,
  tunetype TEXT NOT NULL,
  tunedata TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS similarity (
  tuneid INTEGER,
  comparedtoid INTEGER,
  ncd REAL,
  hamming INTEGER,
  levenshtein INTEGER,
  PRIMARY KEY(tuneid, comparedtoid),
  FOREIGN KEY(tuneid) REFERENCES search_abc(id),
  FOREIGN KEY(comparedtoid) REFERENCES search_abc(id)
);
