from fastapi import APIRouter, Depends
from src.db.database import async_session_maker
from src.db.models import ChatHistoryModel
from sqlalchemy import select, delete
from pydantic import UUID4
from src.auth.dependencies import access_route


router = APIRouter(prefix="/api/history", tags=["Chat History"])


@router.get("/list")
async def history_list():
    async with async_session_maker() as session:
        stmt = select(ChatHistoryModel)
        response = await session.scalars(stmt)
    return response.all()


@router.get("")
async def history_detail(user=Depends(access_route)):
    async with async_session_maker() as session:
        stmt = select(ChatHistoryModel).where(ChatHistoryModel.user_id == user['id'])
        response = await session.scalar(stmt)
    return response


@router.delete("/delete")
async def history_clear(user=Depends(access_route)):
    async with async_session_maker() as session:
        stmt = delete(ChatHistoryModel).where(ChatHistoryModel.user_id == user['id'])
        await session.execute(stmt)
        await session.commit()
    return {"message": "success"}


@router.delete("/delete/all")
async def history_all_clear():
    async with async_session_maker() as session:
        stmt = delete(ChatHistoryModel)
        await session.execute(stmt)
        await session.commit()
    return {"message": "success"}
