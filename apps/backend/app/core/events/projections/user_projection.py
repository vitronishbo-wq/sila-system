"""User Projection - Phase 20: CQRS Read Model for RapidQuery"""
from uuid import UUID
from app.core.events.projections.registry import BaseProjection
from app.core.domain.base_aggregate import DomainEvent

class UserProjection(BaseProjection):
    """
    CQRS Read Model: Optimized for fast queries of user information.
    Built from USER_* events, denormalized for performance.
    """

    @property
    def name(self) -> str:
        return 'users_read_model'

    async def handle_event(self, event: DomainEvent) -> dict:
        """Transform user events into read model data."""
        if event.event_type == 'USER_CREATED':
            return {'id': str(event.aggregate_id), 'email': event.metadata.get('email'), 'name': event.metadata.get('name'), 'tenant_id': str(event.metadata.get('tenant_id')), 'status': 'CREATED', 'permissions': [], 'created_at': event.timestamp.isoformat(), 'updated_at': event.timestamp.isoformat()}
        elif event.event_type == 'USER_ACTIVATED':
            return {'id': str(event.aggregate_id), 'status': 'ACTIVE', 'updated_at': event.timestamp.isoformat()}
        elif event.event_type == 'USER_SUSPENDED':
            return {'id': str(event.aggregate_id), 'status': 'SUSPENDED', 'suspension_reason': event.metadata.get('reason'), 'updated_at': event.timestamp.isoformat()}
        elif event.event_type == 'PERMISSION_GRANTED':
            permission = event.metadata.get('permission')
            resource = event.metadata.get('resource')
            return {'id': str(event.aggregate_id), 'permission_added': f'{permission}:{resource}', 'updated_at': event.timestamp.isoformat()}
        elif event.event_type == 'PERMISSION_REVOKED':
            permission = event.metadata.get('permission')
            resource = event.metadata.get('resource')
            return {'id': str(event.aggregate_id), 'permission_removed': f'{permission}:{resource}', 'updated_at': event.timestamp.isoformat()}
        return None

class UserPermissionsProjection(BaseProjection):
    """
    Specialized projection: Fast lookup of user permissions.
    Optimized for authorization checks.
    """

    @property
    def name(self) -> str:
        return 'user_permissions_index'

    async def handle_event(self, event: DomainEvent) -> dict:
        """Build permissions index from permission events."""
        if event.event_type == 'PERMISSION_GRANTED':
            return {'user_id': str(event.aggregate_id), 'permission': event.metadata.get('permission'), 'resource': event.metadata.get('resource'), 'granted_at': event.timestamp.isoformat(), 'status': 'ACTIVE'}
        elif event.event_type == 'PERMISSION_REVOKED':
            return {'user_id': str(event.aggregate_id), 'permission': event.metadata.get('permission'), 'resource': event.metadata.get('resource'), 'revoked_at': event.timestamp.isoformat(), 'status': 'REVOKED'}
        return None