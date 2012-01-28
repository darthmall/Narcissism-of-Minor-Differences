DROP TABLE IF EXISTS search_abc;

CREATE TABLE IF NOT EXISTS search_abc (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  tunename TEXT NOT NULL,
  tunelink TEXT NOT NULL,
  keysig TEXT NOT NULL,
  tunetype TEXT NOT NULL,
  tunedata TEXT NOT NULL
);
