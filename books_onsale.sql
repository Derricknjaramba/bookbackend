CREATE TABLE books_on_sale (
  id INTEGER PRIMARY KEY ,
  book_id INTEGER NOT NULL,
  price INTEGER NOT NULL,
  FOREIGN KEY (book_id) REFERENCES books (id)
);
