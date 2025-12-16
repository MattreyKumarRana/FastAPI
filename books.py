from fastapi import FastAPI, HTTPException

app = FastAPI()

BOOKS = [
    {
        "title": 'Title 1',
        "author": 'Author 1',
        "category": 'science'
    },
    {
        "title": 'Title 2',
        "author": 'Author 2',
        "category": 'history'
    },
    {
        "title": 'Title 3',
        "author": 'Author 3',
        "category": 'python'
    },
    {
        "title": 'Title 4',
        "author": 'Author 2',
        "category": 'math'
    },
    {
        "title": 'Title 5',
        "author": 'Author 5',
        "category": 'math'
    },
]


@app.get("/books")
async def read_all_books():
    return BOOKS

# Static Path
@app.get("/books/myBook")
async def get_my_book():
    return {
        "favourite_book": "This is my favourite book",
    }

# Dynamic Path
@app.get("/books/{dynamic_param}")
async def read_all_books(dynamic_param):
    for book in BOOKS:
        if book["title"] == dynamic_param:
            return book
    return None
