from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException
from src.auth.security import decode_jwt_token
from src.ai.engine import MarketingAIBot
from src.db.models import ChatHistoryModel
from sqlalchemy import select, update, insert
from src.db.database import async_session_maker
from src.chat.schemas import ChatSchema
from src.auth.dependencies import access_route

router = APIRouter(tags=["Chat"], prefix="/api")


async def get_user_history(id):
    async with async_session_maker() as session:
        history = await session.scalar(
            select(ChatHistoryModel).where(ChatHistoryModel.user_id == str(id))
        )
        if history:
            history = history.content
        else:
            history = []

    return history


async def create_or_update_history(user, content):
    async with async_session_maker() as session:
        user_db = await session.scalar(
            select(ChatHistoryModel).where(ChatHistoryModel.user_id == str(user))
        )
        if user_db:
            await session.execute(
                update(ChatHistoryModel)
                .values(content=content)
                .where(ChatHistoryModel.user_id == str(user))
            )
        else:
            await session.execute(
                insert(ChatHistoryModel).values(user_id=user, content=content)
            )

        await session.commit()


@router.websocket("/websocket/chat/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    await websocket.accept()

    if token:
        user = decode_jwt_token(token)
    else:
        raise HTTPException(status_code=401, detail="Not authenticated")

    history = await get_user_history(user["id"])

    bot = MarketingAIBot()
    await bot.set_history(history)

    try:
        async for data in websocket.iter_text():
            response = await bot.send_message(data)

            await websocket.send_json(response)
    except WebSocketDisconnect:
        print("Disconnect")
    finally:
        history = await bot.get_history()
        await create_or_update_history(user['id'], history)
