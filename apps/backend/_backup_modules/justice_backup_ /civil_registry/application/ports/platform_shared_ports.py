"""Ports de compatibilidade para dependencias de plataforma.

Este modulo centraliza imports para que a camada `application/services`
dependa de um ponto unico interno, sem acoplamento direto a caminhos
de infraestrutura legados.
"""
try:
    from app.core.audit import audit_log
except Exception:

    async def audit_log(*args, **kwargs):
        """Fallback no-op when audit helper is unavailable."""
        return None
from app.core.constants import EntityStatus
from app.core.db import Base
from app.core.events import get_event_bus
from app.core.notifications.services.notification_service import NotificationService
from app.core.observability.middleware import trace
from app.core.services.base_request_service import BaseRequestService
from app.core.territory.models.territory import Territory
from app.core.workflow.infrastructure.repositories.request_repository import RequestRepository
from app.core.workflow.models.request import Request
from ..services.events import CitizenValidated, CitizenValidationFailed
try:
    from app.core.document.models.document_file import DocumentFile
except Exception:

    class DocumentFile:
        pass
try:
    from app.core.document.services.document_service import DocumentService as CoreDocumentService
except Exception:

    class CoreDocumentService:

        def __init__(self, *args, **kwargs):
            raise RuntimeError('CoreDocumentService indisponivel no ambiente atual')
__all__ = ['Base', 'BaseRequestService', 'CitizenValidated', 'CitizenValidationFailed', 'CoreDocumentService', 'DocumentFile', 'EntityStatus', 'NotificationService', 'Request', 'RequestRepository', 'Territory', 'audit_log', 'get_event_bus', 'trace']