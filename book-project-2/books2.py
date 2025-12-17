from fastapi import FastAPI

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, book_id, title, author, description, rating):
        self.id = book_id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

BOOKS = [
    Book(1, "Computer Science", 'codingwithroby', 'A very nice book!', 5),
    Book(2, "FastAPI", 'codingwithroby', 'A great book!', 5),
    Book(3, "Computer 101", 'codingwithroby', 'Amazing book!', 5),
    Book(4, "Title 1", 'author 1', 'Bad book!', 1),
    Book(5, "Title 2", 'author 2', 'Okayish!', 3),
]

@app.get("/")
async def root():
    return "Book2 Project Started"

@app.get("/books")
async def get_books():
    return BOOKS