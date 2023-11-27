from fastapi import APIRouter
from src.chat.schemas import ChatSchema
from src.ai.marketing import MarketingAIBot


router = APIRouter(
    tags=["Chat"],
    prefix='/api'
)


@router.post('/chat')
async def chat(request: ChatSchema):
    ai = MarketingAIBot(user=request.user)
    response = await ai.send_message(request.message)
    return response
