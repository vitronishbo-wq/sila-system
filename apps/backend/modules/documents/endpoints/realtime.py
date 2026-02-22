from fastapi import APIRouter, Depends, Query
from sse_starlette.sse import EventSourceResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
import asyncio

from core.db.session import get_async_db
from core.security import get_current_active_user
from modules.identity.models.user import User
from modules.documents.models.documents import Document

router = APIRouter()

@router.get("/status-stream")
async def document_status_stream(
    last_seen: int = Query(0, description="Último timestamp de update visto pelo cliente"),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user),
):
    async def event_generator():
        # Converte o last_seen timestamp para datetime
        last_dt = datetime.fromtimestamp(last_seen, tz=timezone.utc).replace(tzinfo=None) if last_seen > 0 else datetime.min
        
        while True:
            # Busca documentos do usuário com mudança após o último check
            query = (
                select(Document.id, Document.status, Document.updated_at)
                .where(Document.owner_id == current_user.id)
                .where(Document.updated_at > last_dt)
                .order_by(Document.updated_at.desc())
            )
            result = await db.execute(query)
            updates = result.all()

            if updates:
                latest_update = max(u.updated_at for u in updates)
                last_dt = latest_update # Atualiza para o próximo loop
                
                yield {
                    "event": "update",
                    "data": [{"id": str(u.id), "status": u.status} for u in updates],
                    "retry": 3000,
                }

            await asyncio.sleep(3)

    return EventSourceResponse(event_generator())
