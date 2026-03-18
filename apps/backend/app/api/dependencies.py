from uuid import UUID
from fastapi import Depends
from app.api.deps import get_identity_context
from apps.backend.app.core.identity.context import IdentityContext

async def extract_citizen_id(identity: IdentityContext=Depends(get_identity_context)) -> UUID:
    return identity.citizen_id()