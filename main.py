from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize SQLite Databases
SQLALCHEMY_DATABASE_URL = "sqlite:///./books_database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models for database tables

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    isbn = Column(String)
    genre = Column(String)
    price = Column(Integer)
    stock = Column(Integer)
    

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    role = Column(String)

class BorrowedBook(Base):
    __tablename__ = "borrowed_books"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    borrowed_date = Column(String)
    return_date = Column(String)
    status =  Column(String)

class SoldBook(Base):
    __tablename__ = "books_on_sale"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    price = Column(Integer)

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    feedback_text = Column(String)
    feedback_date =Column(String)
    message_text  = Column(String)

class HelpRequest(Base):
    __tablename__ = "help_requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message_text = Column(String)
    request_date = Column(String)
    subject_text = Column(String)
    status_text = Column(String)

# Pydantic Schemas
class BookSchema(BaseModel):
    title: str
    author: str
    isbn: str
    genre: str
    price: int
    stock: int

class BookUpdateSchema(BaseModel):
    title: str = None
    author: str = None
    price: int = None
    stock: int = None

class UserSchema(BaseModel):
    name: str
    email: str

class FeedbackSchema(BaseModel):
    user_id: int
    feedback_text: str

class HelpSchema(BaseModel):
    user_id: int
    help_text: str

class BorrowedBookSchema(BaseModel):
    id: int 
    book_id: int
    user_id: int
    borrowed_date: str 
    return_date: str
    status: int

class SoldBookSchema(BaseModel):
    id: int
    book_id: int 
    user_id: int
    price: int

Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD Operations

# Admin: Add a new book [TESTED]
@app.post("/admin/add_book", response_model=BookSchema)
def add_book(book: BookSchema, db: SessionLocal = Depends(get_db)):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# Admin: Delete a book [TESTED]
@app.delete("/admin/delete_book/{book_id}")
def delete_book(book_id: int, db: SessionLocal = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted"}

# Admin: View all borrowed books [TESTED]
@app.get("/admin/borrowed_books", response_model=List[BorrowedBookSchema])
def view_borrowed_books(db: SessionLocal = Depends(get_db)):
    return db.query(BorrowedBook).all()

# Admin: View all sold books [TESTED]
@app.get("/admin/sold_books", response_model=List[SoldBookSchema])
def view_sold_books(db: SessionLocal = Depends(get_db)):
    return db.query(SoldBook).all()

# Admin: View all users [TESTED]
@app.get("/admin/users", response_model=List[UserSchema])
def view_users(db: SessionLocal = Depends(get_db)):
    return db.query(User).all()

# User: Borrow a book []
@app.post("/user/borrow_book/{book_id}")
def borrow_book(book_id: int, user_id: int, db: SessionLocal = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book and book.stock > 0:
        borrowed_book = BorrowedBook(book_id=book_id, user_id=user_id)
        book.stock -= 1
        db.add(borrowed_book)
        db.commit()
        return {"message": "Book borrowed successfully"}
    raise HTTPException(status_code=404, detail="Book not available")

# User: Buy a book
@app.post("/user/buy_book/{book_id}")
def buy_book(book_id: int, user_id: int, db: SessionLocal = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book and book.stock > 0:
        sold_book = SoldBook(book_id=book_id, user_id=user_id)
        book.stock -= 1
        db.add(sold_book)
        db.commit()
        return {"message": "Book purchased successfully"}
    raise HTTPException(status_code=404, detail="Book not available")

# User: View all books [TESTED]
@app.get("/user/books", response_model=List[BookSchema])
def view_all_books(db: SessionLocal = Depends(get_db)):
    return db.query(Book).all()

# User: Send feedback
@app.post("/user/send_feedback")
def send_feedback(feedback: FeedbackSchema, db: SessionLocal = Depends(get_db)):
    new_feedback = Feedback(**feedback.dict())
    db.add(new_feedback)
    db.commit()
    return {"message": "Feedback sent"}

# User: Ask for help
@app.post("/user/ask_help")
def ask_help(help_request: HelpSchema, db: SessionLocal = Depends(get_db)):
    new_help = HelpRequest(**help_request.dict())
    db.add(new_help)
    db.commit()
    return {"message": "Help request sent"}

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)