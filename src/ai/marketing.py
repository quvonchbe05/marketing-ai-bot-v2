from src.config import OPENAI_API_KEY
from src.ai.base import Base
from src.ai.tools import search_from_documents


class MarketingAIBot(Base):
    def __init__(self, user=None):
        super().__init__(
            tools=[search_from_documents],
            openai_api_key=OPENAI_API_KEY,
            model="gpt-3.5-turbo",
            temperature=0.4,
            user=user
        )

