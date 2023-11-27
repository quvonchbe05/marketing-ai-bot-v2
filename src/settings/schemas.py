from pydantic import BaseModel, Field


class SettingsSchema(BaseModel):
    prompt: str = Field(...)
    model: str = Field(...)
    temperature: float = Field(...)
