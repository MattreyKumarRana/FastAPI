from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated, List
from pydantic import BaseModel, Field
from starlette import status
from models import Todos
from sqlalchemy.orm import Session
from database import SessionLocal
from .auth import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/todos", status_code=status.HTTP_200_OK)
async def get_todos(user: user_dependency, db : db_dependency):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not Authenticate")
    return db.query(Todos).all()

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, db : db_dependency, user: user_dependency):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not Authenticate")

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(detail="Todo not found", status_code=status.HTTP_404_NOT_FOUND)

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()



