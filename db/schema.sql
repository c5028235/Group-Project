DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS films;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user INTEGER NOT NULL REFERENCES users(id),
    listing_type TEXT NOT NULL,
    postcode TEXT,
    listing_details TEXT,
    poster TEXT,
    duration INTEGER,
    town TEXT,
    price INTEGER
);
