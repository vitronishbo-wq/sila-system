from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import ChatMessage, ChatSession


async def create_session(db: AsyncSession, name: str | None = None) -> ChatSession:
    session = ChatSession(name=name)
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


async def add_message(
    db: AsyncSession,
    session_id: int,
    role: str,
    content: str,
) -> ChatMessage:
    msg = ChatMessage(session_id=session_id, role=role, content=content)
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg


async def get_recent_messages(
    db: AsyncSession,
    session_id: int,
    limit: int = 20,
) -> List[ChatMessage]:
    q = (
        select(ChatMessage)
        .where(
            ChatMessage.session_id == session_id,
        )
        .order_by(
            ChatMessage.created_at.desc(),
        )
        .limit(limit)
    )
    res = await db.execute(q)
    rows = res.scalars().all()
    return list(reversed(rows))
