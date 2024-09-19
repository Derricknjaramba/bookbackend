CREATE TABLE mpesa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    checkout_request_id TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    amount REAL NOT NULL,
    paying_phone_number TEXT NOT NULL,
    receipt_number TEXT UNIQUE NOT NULL,
    transaction_date TEXT NOT NULL
);
