DROP TABLE IF EXISTS coupons;
DROP TABLE IF EXISTS admins;

CREATE TABLE coupons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    is_active INTEGER DEFAULT 1,
    claimed_by_ip TEXT,
    claimed_by_session TEXT,
    claimed_at TEXT
);

CREATE TABLE admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
