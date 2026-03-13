"""Service requests bridge for cross-domain integrations."""
from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.governance.service_requests.application.ports.request_repository_port import RequestRepositoryPort
from apps.backend.app.modules.governance.service_requests.infrastructure.models.attachment_model import AttachmentModel
from apps.backend.app.modules.governance.service_requests.infrastructure.models.request_event_model import RequestEventModel
from apps.backend.app.modules.governance.service_requests.infrastructure.models.service_request_model import ServiceRequestModel
from apps.backend.app.modules.governance.service_requests.infrastructure.repositories.request_repository import RequestRepository

def make_service_request_repository(db: AsyncSession) -> RequestRepository:
    return RequestRepository(db)
__all__ = ['AttachmentModel', 'RequestEventModel', 'RequestRepository', 'RequestRepositoryPort', 'ServiceRequestModel', 'make_service_request_repository']