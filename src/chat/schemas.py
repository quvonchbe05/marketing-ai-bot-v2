from pydantic import BaseModel, Field, UUID4


class ChatSchema(BaseModel):
    user: UUID4 = None
    message: str = Field(...)
