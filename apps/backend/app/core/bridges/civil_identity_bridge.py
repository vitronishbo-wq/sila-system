"""Civil identity bridge exports to avoid direct module-to-module imports.

Consolidation contract:
- Canonical citizen core lives in ``app.modules.justice.civil_registry``.
- ``app.modules.justice.civil_registry`` remains focused on BI/document domain and
  acts as compatibility fallback for citizen reads when needed.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.backend.app.modules.justice._deprecated.bounded_contexts.infrastructure.models.document import (
    Document,
)
from apps.backend.app.modules.justice.application.citizen_service import (
    CitizenService as CanonicalCitizenService,
    CitizenService as LegacyCitizenService,
)

logger = logging.getLogger(__name__)


class CitizenService:
    """Unified citizen service facade.

    Uses canonical identity service when DB session is available; falls back to
    legacy identidade_civil query service for compatibility paths.
    """

    def __init__(self, db_session=None, query_service=None, **kwargs):
        self._primary = CanonicalCitizenService(db_session=db_session, **kwargs)
        self._fallback = LegacyCitizenService(query_service=query_service)
        self._has_db = db_session is not None

    async def validate_citizen(self, citizen_id: str) -> bool:
        if self._has_db:
            try:
                return await self._primary.validate_citizen(citizen_id)
            except Exception as exc:
                logger.warning(
                    "Primary citizen validation failed; falling back to legacy query path",
                    extra={"citizen_id": citizen_id, "error": str(exc)},
                )
        return await self._fallback.validate_citizen(citizen_id)

    async def get_citizen_data(self, citizen_id: str) -> dict:
        if self._has_db:
            try:
                return await self._primary.get_citizen_data(citizen_id)
            except Exception as exc:
                logger.warning(
                    "Primary citizen lookup failed; falling back to legacy query path",
                    extra={"citizen_id": citizen_id, "error": str(exc)},
                )
        return await self._fallback.get_citizen_data(citizen_id)

    async def get_citizen(self, citizen_id: str) -> Any | None:
        return await self._fallback.get_citizen(citizen_id)

    async def find_all(self, name_filter: str | None = None) -> list[Any]:
        return await self._fallback.find_all(name_filter=name_filter)

    def clear_cache(self) -> None:
        self._primary.clear_cache()


__all__ = ["CitizenService", "Document"]
