from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# In-memory database
books = []
next_id = 1

class Book(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    publication_year: int
    genre: str

# Create a new book
@app.post("/books/", response_model=Book)
def create_book(book: Book):
    global next_id
    book.id = next_id
    next_id += 1
    books.append(book)
    return book

# Retrieve a list of all books
@app.get("/books/", response_model=list[Book])
def get_books():
    return books

# Retrieve details of a specific book
@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# Update details of a book
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    for book in books:
        if book.id == book_id:
            book.title = updated_book.title
            book.author = updated_book.author
            book.publication_year = updated_book.publication_year
            book.genre = updated_book.genre
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# Delete a book
@app.delete("/books/{book_id}", response_model=Book)
def delete_book(book_id: int):
    for book in books:
        if book.id == book_id:
            books.remove(book)
            return book
    raise HTTPException(status_code=404, detail="Book not found")
