from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class BookRequest(BaseModel):
    title: str = Field(..., example="The Great Book")
    author: str = Field(min_length=3, example="John Doe")
    pages: int = Field(gt=0, lt=150, example=123)
    publish_date: int = Field(gt=2020,lt=2025, example=2023)

BOOKS = [
    {"title": "Book One", "author": "Author A", "pages": 200,"publish_date":2022},
    {"title": "Book Two", "author": "Author B", "pages": 150,"publish_date":2023},
]

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI Book 2!"}

@app.get("/books")
async def get_books():
    return BOOKS

@app.post("/create-book")
async def create_book(book: BookRequest):
    BOOKS.append(book.model_dump())
    return book

@app.get("/books/publish/")
async def get_books_by_publish_date(publish_date: int):
    for book in BOOKS:
        if book["publish_date"] == publish_date:
            return book