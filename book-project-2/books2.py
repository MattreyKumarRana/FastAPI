from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    author: str
    description: str
    rating: int

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed for the book", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(ge=1, le=5)

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A very amazing book still",
                "rating": 5
            }]
        }
    }

BOOKS = [
    Book(id=1, title="Computer Science", author="codingwithroby", description="A very nice book!", rating=5),
    Book(id=2, title="FastAPI", author="codingwithroby", description="A great book!", rating=5),
    Book(id=3, title="Computer 101", author="codingwithroby", description="Amazing book!", rating=5),
    Book(id=4, title="Title 1", author="author 1", description="Bad book!", rating=1),
    Book(id=5, title="Title 2", author="author 2", description="Okayish!", rating=3),
]

@app.get("/")
async def root():
    return {"message": "Book2 Project Started"}

@app.get("/books")
async def get_books():
    return BOOKS

@app.post("/create_book")
async def create_book(book: BookRequest):
    new_book = Book(**book.model_dump())
    BOOKS.append(increment_id(new_book))
    return new_book


def increment_id(book:Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 0

    return book