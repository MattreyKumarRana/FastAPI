from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated, List
from pydantic import BaseModel, Field
from starlette import status
from models import Users
from sqlalchemy.orm import Session
from database import SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext

# Pydantic Model for a user
class UpdateUserPasswordRequest(BaseModel):
    current_password: str
    new_password: str

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

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/get_user", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db.query(Users).filter(Users.id == user.get("id")).first() # type: ignore

@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, update_user_password: UpdateUserPasswordRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user = db.query(Users).filter(Users.id == user.get("id")).first() # type: ignore

    user_fields = {
        'password': update_user_password.current_password,
        'new_password': update_user_password.new_password,
    }

    if not bcrypt_context.verify(user_fields.get('password'), user.hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password")

    user.hashed_password = bcrypt_context.hash(user_fields.get('new_password'))
    db.commit()



