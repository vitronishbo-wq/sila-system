from fastapi import APIRouter

from apps.backend.app.modules.justice._deprecated.bounded_contexts.cemetery_management.api.router import (
    router as cemetery_router,
)
from apps.backend.app.modules.justice._deprecated.bounded_contexts.civil_registry_core.api.router import (
    router as citizen_router,
)
from apps.backend.app.modules.justice._deprecated.bounded_contexts.identity_documents.api.router import (
    router as documents_router,
)
from apps.backend.app.modules.justice._deprecated.bounded_contexts.vital_events.api.router import (
    router as events_router,
)

router = APIRouter(prefix="/justice", tags=["justice"])
router.include_router(citizen_router)
router.include_router(documents_router)
router.include_router(events_router)
router.include_router(cemetery_router)


@router.get("/ping")
async def ping() -> dict[str, str]:
    return {"module": "justice", "status": "ok"}
