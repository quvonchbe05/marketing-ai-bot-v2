from fastapi import APIRouter
from src.db.database import async_session_maker
from src.db.models import BotConfigModel
from src.settings.schemas import SettingsSchema
from sqlalchemy import insert, select, update

router = APIRouter(
    tags=["Bot settings"],
    prefix='/api/settings'
)


@router.get('')
async def view():
    async with async_session_maker() as session:
        response = await session.scalar(select(BotConfigModel))

    return {
        'prompt': response.prompt,
        'model': response.model,
        'temperature': response.temperature,
    }


@router.put('/edit')
async def edit(settings: SettingsSchema):
    async with async_session_maker() as session:
        await session.execute(
            update(BotConfigModel).values(**settings.dict())
        )
        await session.commit()

    return {
        'message': 'success'
    }