from __future__ import annotations
from apps.backend.app.modules.society.familia.domain.enums import MemberRole

class FamilyCompositionProjector:

    def project_from_aggregate(self, aggregate) -> dict:
        dependents_count = len([m for m in aggregate.members if m.role == MemberRole.DEPENDENT])
        return {'family_id': aggregate.id, 'head_citizen_id': aggregate.head_citizen_id, 'head_name': '', 'member_count': len(aggregate.members), 'dependents_count': dependents_count, 'active_relationships': 0, 'code': aggregate.code, 'status': aggregate.status.value, 'created_at': aggregate.created_at.isoformat(), 'updated_at': aggregate.updated_at.isoformat()}