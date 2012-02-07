CREATE TABLE IF NOT EXISTS similarity (
  tuneid INTEGER NOT NULL,
  comparedtoid INTEGER NOT NULL,
  ncd FLOAT,
  hamming INTEGER,
  levenshtein INTEGER,
  lcs VARCHAR(128),
  PRIMARY KEY(tuneid, comparedtoid),
  FOREIGN KEY(tuneid) REFERENCES search_abc(idx) ON DELETE CASCADE,
  FOREIGN KEY(comparedtoid) REFERENCES search_abc(idx) ON DELETE CASCADE
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
