from .database import Base
from sqlalchemy import Column, Text, Boolean, UUID, String, JSON, DateTime, Float
from uuid import uuid4
import datetime


class BaseModel:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, nullable=True, default=datetime.datetime.utcnow())
    updated_at = Column(
        DateTime,
        nullable=True,
        default=datetime.datetime.utcnow(),
        onupdate=datetime.datetime.utcnow(),
    )


class ChatHistoryModel(Base, BaseModel):
    __tablename__ = "history"

    user = Column(String, nullable=True)
    content = Column(JSON, nullable=True)


class BotConfigModel(Base, BaseModel):
    __tablename__ = "config"

    prompt: str = Column(Text, nullable=False)
    model: str = Column(String(155), nullable=False)
    temperature: float = Column(Float, nullable=False)


class FilesModel(Base, BaseModel):
    __tablename__ = "files"

    file_path: str = Column(Text, nullable=True)


class NotionModel(Base, BaseModel):
    __tablename__ = "notion"

    title: str = Column(String, nullable=False)
    token: str = Column(String, nullable=False)
    database_id: str = Column(String, nullable=False)
