from sqlalchemy.orm import Session
from sqlalchemy import select
from .policies import DataSegment, PermissionPolicyModel

class AccessControlEngine:

    def __init__(self, db: Session, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.db = db

    def check_authorization(self, service_id: str, data_segment: DataSegment, action: str='read') -> bool:
        if service_id == 'ADMIN_CENTRAL':
            return True
        query = select(PermissionPolicyModel).where(PermissionPolicyModel.service_id == service_id, PermissionPolicyModel.data_segment == data_segment)
        try:
            result = self.db.execute(query)
            policy = result.scalar_one_or_none()
        except Exception:
            return False
        if not policy:
            return False
        action_type = action.lower()
        if action_type == 'read':
            return policy.can_read
        if action_type == 'write':
            return policy.can_write
        return False

    def authorize(self, service_id: str, segment: DataSegment, action: str='read') -> bool:
        return self.check_authorization(service_id, segment, action)