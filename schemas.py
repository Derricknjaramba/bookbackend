class BookSchema(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    genre: str
    price: int
    stock: int

    class Config:
        orm_mode = True 