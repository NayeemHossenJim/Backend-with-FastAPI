from fastapi import FastAPI

app = FastAPI()

class Book:
    def __init__(self, title: str, author: str, pages: int):
        self.title = title
        self.author = author
        self.pages = pages

BOOKS = [
    Book("Book One", "Author A", 300),
    Book("Book Two", "Author B", 250),
    Book("Book Three", "Author C", 400)
]

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI Book 2!"}

@app.get("/books")
async def get_books():
    return BOOKS