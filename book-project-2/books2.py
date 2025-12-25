from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed for the book", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(ge=1, le=5)
    published_date: int = Field(ge=1999, le=3000)

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A very amazing book still",
                "rating": 5,
                "published_date": 2000
            }]
        }
    }

BOOKS = [
    Book(id=1, title="Computer Science", author="codingwithroby", description="A very nice book!", rating=5, published_date=2012),
    Book(id=2, title="FastAPI", author="codingwithroby", description="A great book!", rating=5, published_date=2015),
    Book(id=3, title="Computer 101", author="codingwithroby", description="Amazing book!", rating=5, published_date=2020),
    Book(id=4, title="Title 1", author="author 1", description="Bad book!", rating=1, published_date=2010),
    Book(id=5, title="Title 2", author="author 2", description="Okayish!", rating=3, published_date=2017),
]

@app.get("/")
async def root():
    return {"message": "Book2 Project Started"}

@app.get("/books")
async def get_books():
    return BOOKS

@app.get("/books/{book_id}")
async def get_book(book_id: int = Path(gt = 0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    return "Not Found"

@app.get("/books")
async def get_books_by_rating(rating: int = Query(gt = 0, lt = 6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)

    return books_to_return

@app.post("/create_book")
async def create_book(book: BookRequest):
    new_book = Book(**book.model_dump())
    BOOKS.append(increment_id(new_book))
    return new_book

# GET Request fetch book by published date
@app.get("/books/book_date/{book_date}")
async def get_books_by_published_date(book_date: int = Path(ge=1999, le=3000)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == book_date:
            books_to_return.append(book)

    return books_to_return

@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i].id = book.id
            BOOKS[i].title = book.title
            BOOKS[i].author = book.author
            BOOKS[i].description = book.description
            BOOKS[i].rating = book.rating

# DELETE Request with FastAPI
@app.delete("/books/{book_id}")
async def delete_book(book_id: int = Path(gt = 0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break


def increment_id(book:Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 0
    return book