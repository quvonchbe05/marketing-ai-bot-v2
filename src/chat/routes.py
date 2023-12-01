from fastapi import APIRouter, Depends
from src.chat.schemas import ChatSchema
from src.ai.marketing import MarketingAIBot
from src.auth.dependencies import access_route

router = APIRouter(
    tags=["Chat"],
    prefix='/api'
)


@router.post('/chat')
async def chat(request: ChatSchema, user=Depends(access_route)):
    ai = MarketingAIBot(user=user['id'])
    response = await ai.send_message(request.message)
    return response
