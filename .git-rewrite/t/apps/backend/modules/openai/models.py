from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.db.base_class import Base


class ChatSession(Base):
    __tablename__ = "openai_chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class ChatMessage(Base):
    __tablename__ = "openai_chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("openai_chat_sessions.id"), nullable=False)
    role = Column(String(32), nullable=False)  # 'user' | 'assistant' | 'system'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    session = relationship("ChatSession", back_populates="messages")


ChatSession.messages = relationship(
    "ChatMessage",
    back_populates="session",
    order_by=ChatMessage.created_at,
    cascade="all, delete-orphan",
)
