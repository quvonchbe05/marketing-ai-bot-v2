from pydantic import BaseModel, Field


class NotionSchema(BaseModel):
    title: str = Field(...)
    token: str = Field(...)
    database_id: str = Field(...)
