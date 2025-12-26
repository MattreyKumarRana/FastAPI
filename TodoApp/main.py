# Main Python file for the Todos App

from fastapi import FastAPI, Depends
from typing import Annotated
import models
from models import Todos
from sqlalchemy.orm import Session
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

# GET Request
@app.get("/")
async def read_all_todos(db: db_dependency):
    return db.query(Todos).all()
