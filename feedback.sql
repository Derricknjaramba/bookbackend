CREATE TABLE feedback (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  feedback_date DATE NOT NULL,
  feedback_type TEXT NOT NULL CHECK (feedback_type IN ('suggestion', 'complaint', 'compliment')),  -- e.g., suggestion, complaint, compliment
  message TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id)
);
