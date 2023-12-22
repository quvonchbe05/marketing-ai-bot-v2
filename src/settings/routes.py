from fastapi import APIRouter
from src.db.database import async_session_maker
from src.db.models import BotConfigModel
from src.settings.schemas import SettingsSchema
from sqlalchemy import insert, select, update
from src.ai.data.params import prompt, temperature, model

router = APIRouter(
    tags=["Bot settings"],
    prefix='/api/settings'
)


@router.get('')
async def view():
    return {
        "model": model,
        "temperature": temperature,
        "prompt": prompt
    }


@router.put('/edit')
async def edit(settings: SettingsSchema):
    async with async_session_maker() as session:
        config = await session.scalar(select(BotConfigModel))
        if config:
            await session.execute(
                update(BotConfigModel).values(**settings.dict())
            )
        else:
            await session.execute(
                insert(BotConfigModel).values(**settings.dict())
            )
        await session.commit()

    return {
        'message': 'success'
    }
