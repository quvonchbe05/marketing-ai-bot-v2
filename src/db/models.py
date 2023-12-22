from src.db.database import Base
from sqlalchemy import Column, Text, Boolean, UUID, String, JSON, DateTime, Float, ForeignKey
from uuid import uuid4
import datetime
from sqlalchemy.orm import relationship


class BaseModel:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, nullable=True, default=datetime.datetime.utcnow())
    updated_at = Column(
        DateTime,
        nullable=True,
        default=datetime.datetime.utcnow(),
        onupdate=datetime.datetime.utcnow(),
    )


class BotConfigModel(Base, BaseModel):
    __tablename__ = "config"

    prompt: str = Column(Text, nullable=False)
    model: str = Column(String(155), nullable=False)
    temperature: float = Column(Float, nullable=False)


class FilesModel(Base, BaseModel):
    __tablename__ = "files"

    file_path: str = Column(Text, nullable=True)
    name: str = Column(String, nullable=True)


class NotionModel(Base, BaseModel):
    __tablename__ = "notion"

    title: str = Column(String, nullable=False)
    token: str = Column(String, nullable=False)
    database_id: str = Column(String, nullable=False)


class ChatHistoryModel(Base, BaseModel):
    __tablename__ = "history"

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    content = Column(JSON, nullable=True)

    user = relationship("UserModel", backref="chat_history")


class UserModel(Base, BaseModel):
    __tablename__ = "user"

    name: str = Column(String(255), nullable=False)
    username: str = Column(String, nullable=False)
    password: str = Column(String, nullable=True)
    is_admin: bool = Column(Boolean, default=False)
