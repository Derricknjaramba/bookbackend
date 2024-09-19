CREATE TABLE borrowed_books (
  id INTEGER PRIMARY KEY ,
  book_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  borrowed_date DATE NOT NULL,
  return_date DATE NOT NULL,
  status TEXT DEFAULT 'borrowed',  -- e.g., borrowed, returned, overdue
  FOREIGN KEY (book_id) REFERENCES books (id),
  FOREIGN KEY (user_id) REFERENCES users (id)
);

