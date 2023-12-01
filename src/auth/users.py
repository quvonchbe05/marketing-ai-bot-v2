from fastapi import APIRouter, HTTPException
from src.db.models import UserModel
from sqlalchemy import select, insert, update, delete
from src.db.database import async_session_maker
from src.auth.schemas import UserSchema, PasswordSchema
from src.auth.security import encode_password
from pydantic import UUID4

router = APIRouter(
    prefix="/api/users",
    tags=[
        "Users",
    ],
)


@router.get("/list")
async def user_list():
    """Endpoint for get list of users"""
    async with async_session_maker() as session:
        stmt = select(UserModel)
        users = await session.scalars(stmt)
    return users.all()


@router.get("/detail/{user_id}")
async def user_detail(user_id: UUID4):
    """Endpoint for get user details"""
    async with async_session_maker() as session:
        stmt = select(UserModel).where(UserModel.id == user_id)
        users = await session.scalar(stmt)
    return users


@router.post("/generate/password")
async def generate_password(data: PasswordSchema):
    """Endpoint for generate new password user"""
    async with async_session_maker() as session:
        stmt = (
            update(UserModel)
            .values(password=encode_password(data.password))
            .where(UserModel.id == data.user_id)
        )
        await session.execute(stmt)
        await session.commit()
    return {"message": "success"}


@router.post("/create")
async def user_create(
    new_user: UserSchema,
):
    """Endpoint for create new user"""
    async with async_session_maker() as session:
        # Check if the username is already registered
        db_username_query = select(UserModel).where(UserModel.username == new_user.username)
        db_username = await session.scalar(db_username_query)
        if db_username:
            raise HTTPException(
                status_code=400, detail="This username is already registered."
            )

        stmt = insert(UserModel).values(
            name=new_user.name,
            username=new_user.username,
        )
        await session.execute(stmt)
        await session.commit()

    return {"status": "success"}


@router.put("/edit/{user_id}")
async def user_edit(
    user_id: UUID4,
    new_user: UserSchema,
):
    """Endpoint for edit user"""
    async with async_session_maker() as session:
        stmt = (
            update(UserModel)
            .values(
                name=new_user.name,
                username=new_user.username,
                is_admin=new_user.is_admin,
            )
            .where(UserModel.id == user_id)
        )
        await session.execute(stmt)
        await session.commit()

    return {"status": "success"}


@router.delete("/delete/{user_id}")
async def user_edit(user_id: UUID4):
    """Endpoint for delete user"""
    async with async_session_maker() as session:
        stmt = delete(UserModel).where(UserModel.id == user_id)
        await session.execute(stmt)
        await session.commit()

    return {"status": "success"}
