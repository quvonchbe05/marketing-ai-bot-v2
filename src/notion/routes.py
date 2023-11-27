from fastapi import APIRouter
from src.db.database import async_session_maker
from src.db.models import NotionModel
from src.notion.schemas import NotionSchema
from sqlalchemy import insert, select, update, delete
from pydantic import UUID4
from src.utils.validators import notion_validator


router = APIRouter(prefix="/api/notion", tags=["Notion integration"])


@router.get("/list")
async def notion_list():
    async with async_session_maker() as session:
        stmt = select(NotionModel)
        response = await session.scalars(stmt)
    return response.all()


@router.get("/{id}")
async def notion_detail(id: UUID4):
    async with async_session_maker() as session:
        stmt = select(NotionModel).where(NotionModel.id == id)
        response = await session.scalar(stmt)
    return response


@router.post("/create")
async def notion_create(
    notion: NotionSchema,
):
    validate_notion = notion_validator(notion)
    async with async_session_maker() as session:
        stmt = insert(NotionModel).values(
            title=validate_notion.title,
            token=validate_notion.token,
            database_id=validate_notion.database_id,
        )
        await session.execute(stmt)
        await session.commit()
    return {"message": "success"}


@router.put("/edit/{id}")
async def notion_edit(notion: NotionSchema, id: UUID4):
    async with async_session_maker() as session:
        stmt = (
            update(NotionModel)
            .values(
                title=notion.title, token=notion.token, database_id=notion.database_id
            )
            .where(NotionModel.id == id)
        )
        await session.execute(stmt)
        await session.commit()
    return {"message": "success"}


@router.delete("/delete/{id}")
async def notion_delete(id: UUID4):
    async with async_session_maker() as session:
        stmt = delete(NotionModel).where(NotionModel.id == id)
        await session.execute(stmt)
        await session.commit()
    return {"message": "success"}


@router.delete("/delete/all")
async def notion_all_delete():
    async with async_session_maker() as session:
        stmt = delete(NotionModel)
        await session.execute(stmt)
        await session.commit()
    return {"message": "success"}
