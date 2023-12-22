from fastapi import APIRouter, HTTPException
from src.db.models import UserModel
from sqlalchemy import select
from src.db.database import async_session_maker
from src.auth.security import decode_password, generate_token
from src.auth.schemas import LoginSchema


router = APIRouter(tags=["Auth"], prefix="/api/auth")


@router.post("/login")
async def login(user: LoginSchema):
    """Endpoint for login"""
    async with async_session_maker() as session:
        stmt = select(UserModel).where(UserModel.username == user.username)
        user_db = await session.scalar(stmt)
    if (
        user_db
        and user_db.password
        and decode_password(user.password, user_db.password)
    ):
        token = generate_token(user_db)
        return {"token": token, "id": user_db.id, "is_admin": user_db.is_admin}
    else:
        raise HTTPException(status_code=401, detail="Incorrect username or password.")
