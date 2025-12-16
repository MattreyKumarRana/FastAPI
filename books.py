from fastapi import FastAPI, HTTPException, Body

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


# GET Requests in FastAPI
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI!"}

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


# Query Parameters
@app.get("/books/")
async def read_all_books(category: str):
    books_to_return = []
    for book in BOOKS:
        if book["category"].casefold() == category.casefold():
            books_to_return.append(book)

    # books to return by filter
    return books_to_return

@app.get("/books/{book_author}/")
async def get_books_by_author(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book["author"].casefold() == book_author.casefold() and book["category"].casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


# POST Requests in FastAPI
@app.post("/books/create_book")
async def create_book(book=Body(...)):
    return "book created"

# PUT Request in FastAPI
@app.put("/books/update_book")
async def update_book(updated_book=Body(...)):
    for i in range(len(BOOKS)):
        if updated_book["title"].casefold() == BOOKS[i].get("title").casefold():
            BOOKS[i] = updated_book
            return "Book updated"
    return None


# DELETE Request in FastAPI
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for book in BOOKS:
        if book["title"].casefold() == book_title.casefold():
            BOOKS.remove(book)
            return "Book deleted"
    return "No book found"