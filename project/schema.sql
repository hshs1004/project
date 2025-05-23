CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
);

CREATE TABLE accounts (
    user_id INTEGER,
    balance INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE transfers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_user INTEGER,
    to_user INTEGER,
    amount INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);