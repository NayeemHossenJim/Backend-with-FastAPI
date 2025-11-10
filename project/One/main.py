from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {"title": "Book One", "author": "Author A"},
    {"title": "Book Two", "author": "Author B"},
    {"title": "Book Three", "author": "Author C"}
]

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}

# Get all books (static path)
@app.get("/books")
async def get_books():
    return BOOKS

# Get book by author (dynamic path parameter)
@app.get("/books/{book_author}")
async def get_books_by_author(book_author: str):
    for book in BOOKS:
        if book["author"].casefold() == book_author.casefold():
            return book
        
# Get book by title and author (using query parameter for author)
@app.get("/books/{book_title}/")
async def get_book_by_title_and_author(book_title: str, author: str):
    for book in BOOKS:
        if (book["title"].casefold() == book_title.casefold() and
                book["author"].casefold() == author.casefold()):
            return book
        
# Add a new book (POST request)
@app.post("/books")
async def add_book(book: dict):
    BOOKS.append(book)
    return book

# Update an existing book (PUT request)
@app.put("/books/{book_title}")
async def update_book(book_title: str):
    for book in BOOKS:
        if book["title"].casefold() == book_title.casefold():
            book["title"] = "Updated Title"
            return book
        

# Delete a book (DELETE request)
@app.delete("/books/{book_title}")
async def delete_book(book_title: str):
    for i, book in enumerate(BOOKS):
        if book["title"].casefold() == book_title.casefold():
            del BOOKS[i]
            return {"message": "Book deleted"}
    return {"error": "Book not found"}