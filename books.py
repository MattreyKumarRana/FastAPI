from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return "Hello World"

@app.get("/books")
async def read_all_books():
    return {
        "message": "An Amazing Journey Starts....."
    }