from sqlalchemy.orm import Session
from sqlalchemy import select
from .policies import (
    DataSegment, 
    PermissionPolicyModel
)
# from app.citizen.events.models import AccessLogModel

class AccessControlEngine:
    def __init__(self, db: Session, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.db = db
    def check_authorization(self, service_id: str, data_segment: DataSegment, action: str = "read") -> bool:
        if service_id == "ADMIN_CENTRAL":
            return True
        query = select(PermissionPolicyModel).where(
            PermissionPolicyModel.service_id == service_id,
            PermissionPolicyModel.data_segment == data_segment
        )
        try:
            result = self.db.execute(query)
            policy = result.scalar_one_or_none()
        except Exception:
            return False
        if not policy:
            return False
        action_type = action.lower()
        if action_type == "read":
            return policy.can_read
        if action_type == "write":
            return policy.can_write
        return False
    def authorize(self, service_id: str, segment: DataSegment, action: str = "read") -> bool:
        return self.check_authorization(service_id, segment, action)
    
    # def log_access(self, citizen_id: str, service_id: str, segment: DataSegment, legal_basis: str, performed_by: str = "SYSTEM"):
    #     try:
    #         c_id = uuid.UUID(citizen_id) if isinstance(citizen_id, str) else citizen_id
    #         log_entry = AccessLogModel(
    #             citizen_id=c_id,
    #             service_id=service_id,
    #             performed_by=performed_by,
    #             data_segment=segment,
    #             legal_basis=legal_basis
    #         )
    #         self.db.add(log_entry)
    #         self.db.commit()
    #         return log_entry
    #     except Exception as e:
    #         self.db.rollback()
    #         raise RuntimeError(f"Erro ao persistir log de auditoria: {str(e)}")

    # def list_access_logs(self, citizen_id: Optional[uuid.UUID] = None, limit: int = 50) -> List[AccessLogModel]:
    #     query = select(AccessLogModel).order_by(desc(AccessLogModel.timestamp))
    #     if citizen_id:
    #         query = query.where(AccessLogModel.citizen_id == citizen_id)
    #     return list(self.db.execute(query.limit(limit)).scalars().all())
