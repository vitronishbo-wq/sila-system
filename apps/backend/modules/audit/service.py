from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
from typing import Any, Dict, Optional
from uuid import UUID

from .models import AuditLog

async def log_action(
    db: AsyncSession,
    user_id: UUID,
    action: str,
    resource_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    request: Optional[Request] = None,
):
    """
    Institutional Audit Log helper.
    Captures IP and User-Agent from the request when available.
    """
    metadata = details.copy() if details else {}
    
    if request:
        metadata["ip"] = request.client.host if request.client else "unknown"
        metadata["user_agent"] = request.headers.get("user-agent", "unknown")
        # Could also log method, path, etc. if needed

    log = AuditLog(
        user_id=user_id,
        action=action,
        resource_id=resource_id,
        metadata_json=metadata
    )
    
    db.add(log)
    # We use flush or commit depending on the context, but usually log_action 
    # should be part of the same transaction or committed immediately.
    # To ensure traceability even if the main action fails (though sometimes we want the opposite),
    # we'll commit here or rely on the caller's transaction management.
    # Given the async nature and FastAPI dependencies, usually db.add is enough 
    # as the dependency will commit. But logs are critical.
    await db.commit()
