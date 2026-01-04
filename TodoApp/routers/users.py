from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated, List
from pydantic import BaseModel, Field
from starlette import status
from models import Users
from sqlalchemy.orm import Session
from database import SessionLocal
from .auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/get_user", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db.query(Users).filter(Users.id == user.get("id")).first() # type: ignore