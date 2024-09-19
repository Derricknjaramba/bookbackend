CREATE TABLE help (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  request_date DATE NOT NULL,
  subject TEXT NOT NULL,
  message TEXT NOT NULL,
  status TEXT DEFAULT 'pending',  -- e.g., pending, in progress, resolved
  FOREIGN KEY (user_id) REFERENCES users (id)
);
