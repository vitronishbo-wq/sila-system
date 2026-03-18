"""Identity bridge exports to avoid direct module-to-module imports."""
from typing import Optional, Any
from uuid import uuid4
import uuid
from sqlalchemy import Column, Date, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from apps.backend.app.modules.identity.subdomains.citizen_identity_graph.application.identity_graph_service import IdentityGraphService
from apps.backend.app.modules.justice.domain.citizen import Citizen as CitizenEntity
from apps.backend.app.modules.justice._deprecated.bounded_contexts.infrastructure.models.bi_event_record import BIEventRecord
from apps.backend.app.modules.justice._deprecated.bounded_contexts.infrastructure.models.bi_record import BIRecord
from app.core.db import Base

class _IdentityCitizenRepositoryProxy:

    def __call__(self, *args, **kwargs):
        from apps.backend.app.modules.justice._deprecated.bounded_contexts.civil_registry_core.infrastructure.repositories.citizen_repository import CitizenRepository
        return CitizenRepository(*args, **kwargs)

    def __getattr__(self, item):
        from apps.backend.app.modules.justice._deprecated.bounded_contexts.civil_registry_core.infrastructure.repositories.citizen_repository import CitizenRepository
        return getattr(CitizenRepository, item)
IdentityCitizenRepository = _IdentityCitizenRepositoryProxy()

class CitizenFUC(Base):
    __tablename__ = 'citizen_fuc'
    __table_args__ = {'extend_existing': True}
    citizen_id = Column(PGUUID(as_uuid=True), unique=True, nullable=False, index=True, default=uuid.uuid4)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    birth_date = Column(Date, nullable=True)
    document_number = Column(String(64), nullable=True)
    vital_status = Column(String(32), nullable=True)
__all__ = ['BIEventRecord', 'BIRecord', 'CitizenFUC', 'CitizenEntity', 'IdentityCitizenRepository', 'IdentityBridge']

class IdentityBridge:
    """Compatibility wrapper for legacy imports expecting a class."""
    CitizenFUC = CitizenFUC
    CitizenEntity = CitizenEntity
    BIEventRecord = BIEventRecord
    BIRecord = BIRecord
    IdentityCitizenRepository = IdentityCitizenRepository

    def __init__(self, identity_graph: Optional[IdentityGraphService]=None, user_service: Optional[Any]=None):
        self.identity_graph = identity_graph
        self.user_service = user_service

    async def create_identity_from_birth(self, citizen_id: str, name: str, birth_date: str):
        if not self.identity_graph or not self.user_service:
            raise ValueError('identity_graph and user_service are required')
        identity_id = str(uuid4())
        await self.identity_graph.create_citizen_node(identity_id=identity_id, citizen_id=citizen_id, name=name, birth_date=birth_date)
        if not hasattr(self.user_service, "create_user_identity"):
            raise ValueError("user_service missing create_user_identity")
        await self.user_service.create_user_identity(identity_id=identity_id, citizen_id=citizen_id)
        return identity_id
