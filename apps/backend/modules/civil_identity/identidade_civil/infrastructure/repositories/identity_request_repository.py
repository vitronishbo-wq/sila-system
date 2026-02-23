"""Repository for IdentityRequest persistence.

Stores a JSON representation of the IdentityRequest dataclass in a lightweight
table `identity_requests`. This is intentionally simple but correct and
transactional (uses SQLAlchemy mapped model). It provides the methods used by
services: `save`, `get_by_id`.
"""
from datetime import datetime
import uuid
from typing import Optional

from sqlalchemy import Column, String, DateTime, JSON, select, and_, func, desc
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base
from typing import Any, Tuple


def _sanitize_for_json(obj):
    """Recursively convert non-JSON-serializable objects to primitives.

    - UUID -> str
    - datetime/date -> isoformat
    - dataclass-like objects -> dict via __dict__
    """
    import datetime as _dt
    import uuid as _uuid

    if obj is None:
        return None
    if isinstance(obj, _uuid.UUID):
        return str(obj)
    if isinstance(obj, (_dt.datetime, _dt.date)):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: _sanitize_for_json(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_sanitize_for_json(v) for v in obj]
    # dataclass-like
    if hasattr(obj, "__dict__"):
        try:
            return _sanitize_for_json(obj.__dict__)
        except Exception:
            pass
    return obj


class IdentityRequestModel(Base):
    __tablename__ = "identity_requests"
    __table_args__ = {"extend_existing": True}

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    citizen_fuc_id = Column(String(50), nullable=False, index=True)
    service_code = Column(String(10), nullable=False)
    status = Column(String(50), nullable=False, default="PENDING")
    payload = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_domain(self):
        """Map to IdentityRequest domain model."""
        from ...domain.models.identity_request import IdentityRequest, RequestStatus
        
        # Ensure status is the Enum
        status_val = self.status
        if isinstance(status_val, str):
            try:
                status_val = RequestStatus(status_val.upper())
            except ValueError:
                status_val = RequestStatus.PENDING

        req = IdentityRequest(
            id=self.id,
            citizen_fuc_id=self.citizen_fuc_id,
            service_code=self.service_code,
            status=status_val,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
        # Load notes from payload if available
        if self.payload and isinstance(self.payload, dict):
            req.notes = self.payload.get("notes", [])
            req.bi_id = self.payload.get("bi_id")
            
        return req


class IdentityRequestRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, identity_request) -> Any:
        """Persist an IdentityRequest domain model or update existing record."""
        # Domain model -> data dict for persistence
        status_val = identity_request.status.value if hasattr(identity_request.status, 'value') else str(identity_request.status)
        
        payload_data = {
            "notes": getattr(identity_request, "notes", []),
            "bi_id": str(identity_request.bi_id) if getattr(identity_request, "bi_id", None) else None
        }

        stmt = select(IdentityRequestModel).where(IdentityRequestModel.id == identity_request.id)
        result = await self.session.execute(stmt)
        obj = result.scalar_one_or_none()

        if obj:
            obj.status = status_val
            obj.payload = _sanitize_for_json(payload_data)
            obj.updated_at = datetime.utcnow()
        else:
            obj = IdentityRequestModel(
                id=identity_request.id,
                citizen_fuc_id=identity_request.citizen_fuc_id,
                service_code=identity_request.service_code,
                status=status_val,
                payload=_sanitize_for_json(payload_data),
                created_at=getattr(identity_request, "created_at", datetime.utcnow())
            )
            self.session.add(obj)
            
        await self.session.flush()
        return obj.to_domain()

    async def get_by_id(self, req_id: uuid.UUID) -> Optional[Any]:
        """Fetch request by ID and return domain model."""
        stmt = select(IdentityRequestModel).where(IdentityRequestModel.id == req_id)
        result = await self.session.execute(stmt)
        obj = result.scalar_one_or_none()
        return obj.to_domain() if obj else None

    async def get_by_citizen(self, citizen_id: str, skip: int = 0, limit: int = 100, **filters) -> tuple:
        """Compatibility with BaseRequestService."""
        stmt = select(IdentityRequestModel).where(IdentityRequestModel.citizen_fuc_id == str(citizen_id))
        
        # Count
        count_stmt = select(func.count()).select_from(IdentityRequestModel).where(IdentityRequestModel.citizen_fuc_id == str(citizen_id))
        total_result = await self.session.execute(count_stmt)
        total = total_result.scalar() or 0

        # Query
        stmt = stmt.order_by(desc(IdentityRequestModel.created_at)).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [m.to_domain() for m in models], total

    async def get_pending(self):
        """Return list of pending identity requests."""
        stmt = select(IdentityRequestModel).where(
            IdentityRequestModel.status.in_(["PENDING", "PENDING_FUC_VALIDATION", "FUC_VALIDATION"])
        )
        result = await self.session.execute(stmt)
        return [m.to_domain() for m in result.scalars().all()]
