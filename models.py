from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Books model - Central book repository
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    genre = Column(String)
    description = Column(String)
    isbn = Column(String, unique=True, index=True)

    books_onsale = relationship("BookOnSale", back_populates="book")
    books_toborrow = relationship("BooksToBorrow", back_populates="book")

# BookOnSale model (already defined)
class BookOnSale(Base):
    __tablename__ = 'books_onsale'
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id'))  # Foreign key from books table
    price = Column(Integer)
    quantity = Column(Integer)

    book = relationship("Book", back_populates="books_onsale")

# BooksToBorrow model (already defined)
class BooksToBorrow(Base):
    __tablename__ = 'books_toborrow'
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id'))  # Foreign key from books table
    quantity = Column(Integer)

    book = relationship("Book", back_populates="books_toborrow")

# BorrowedBook model (already defined)
class BorrowedBook(Base):
    __tablename__ = 'borrowed_books'
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books_toborrow.id'))  # Foreign key from books_toborrow
    user_id = Column(Integer)
    due_date = Column(String)
    returned = Column(Boolean, default=False)

# PurchasedBook model (already defined)
class PurchasedBook(Base):
    __tablename__ = 'purchased_books'
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books_onsale.id'))  # Foreign key from books_onsale
    user_id = Column(Integer)
    quantity = Column(Integer)

# Feedback model (already defined)
class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    message = Column(String)

# HelpRequest model (already defined)
class HelpRequest(Base):
    __tablename__ = 'help'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    request = Column(String)

# User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    borrowed_books = relationship("BorrowedBook", back_populates="user")
    purchased_books = relationship("PurchasedBook", back_populates="user")

# Admin model
class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

