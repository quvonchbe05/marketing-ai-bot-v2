from pydantic import BaseModel, Field, UUID4


class ChatSchema(BaseModel):
    message: str = Field(...)
