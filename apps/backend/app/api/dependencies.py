from uuid import UUID

from apps.backend.app.api.deps import get_identity_context
from fastapi import Depends

from apps.backend.app.core.identity.context import IdentityContext

identity_context_dep = Depends(get_identity_context)


async def extract_citizen_id(identity: IdentityContext = identity_context_dep) -> UUID:
    return identity.citizen_id()
