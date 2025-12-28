from fastapi import APIRouter
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext

router = APIRouter()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic Model for a user
class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    role: str

@router.post("/auth")
async def create_user(create_user_request: CreateUserRequest):
    create_user_model = Users(
        user_name=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        is_active=True,
        hashed_password=bcrypt_context.hash(create_user_request.password),
    )

    return create_user_model
