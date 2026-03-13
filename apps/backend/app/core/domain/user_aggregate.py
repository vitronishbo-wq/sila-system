"""User Aggregate Root - Phase 20: Event-Sourced User Entity"""
from uuid import UUID
from datetime import datetime
from enum import Enum
from app.core.domain.base_aggregate import BaseAggregate, DomainEvent

class UserStatus(str, Enum):
    CREATED = 'CREATED'
    ACTIVE = 'ACTIVE'
    SUSPENDED = 'SUSPENDED'
    DELETED = 'DELETED'

class UserCreatedEvent(DomainEvent):
    """Event: User was created in the system."""

    def __init__(self, email: str, name: str, tenant_id: UUID, **kwargs):
        super().__init__(**kwargs)
        self.email = email
        self.name = name
        self.tenant_id = tenant_id

class UserActivatedEvent(DomainEvent):
    """Event: User account was activated."""

    def __init__(self, reason: str='Account activation', **kwargs):
        super().__init__(**kwargs)
        self.reason = reason

class UserSuspendedEvent(DomainEvent):
    """Event: User account was suspended."""

    def __init__(self, reason: str, **kwargs):
        super().__init__(**kwargs)
        self.reason = reason

class PermissionGrantedEvent(DomainEvent):
    """Event: Permission was granted to user."""

    def __init__(self, permission: str, resource: str, **kwargs):
        super().__init__(**kwargs)
        self.permission = permission
        self.resource = resource

class PermissionRevokedEvent(DomainEvent):
    """Event: Permission was revoked."""

    def __init__(self, permission: str, resource: str, **kwargs):
        super().__init__(**kwargs)
        self.permission = permission
        self.resource = resource

class UserAggregate(BaseAggregate):
    """
    User aggregate root - manages all user-related state changes.
    All state modifications generate immutable events.
    """

    def __init__(self, user_id: UUID=None):
        super().__init__(user_id)
        self.email: str = ''
        self.name: str = ''
        self.tenant_id: UUID = None
        self.status: UserStatus = UserStatus.CREATED
        self.permissions: set = set()
        self.created_at: datetime = None
        self.updated_at: datetime = None

    def create_user(self, email: str, name: str, tenant_id: UUID) -> None:
        """Command: Create a new user."""
        if self.status != UserStatus.CREATED:
            raise ValueError('User already exists')
        event = UserCreatedEvent(aggregate_id=self.id, event_type='USER_CREATED', version=self.version + 1, email=email, name=name, tenant_id=tenant_id)
        self.record_event(event)

    def activate_user(self, reason: str='Account activation') -> None:
        """Command: Activate user account."""
        if self.status == UserStatus.ACTIVE:
            raise ValueError('User already active')
        event = UserActivatedEvent(aggregate_id=self.id, event_type='USER_ACTIVATED', version=self.version + 1, reason=reason)
        self.record_event(event)

    def suspend_user(self, reason: str) -> None:
        """Command: Suspend user account."""
        if self.status == UserStatus.SUSPENDED:
            raise ValueError('User already suspended')
        event = UserSuspendedEvent(aggregate_id=self.id, event_type='USER_SUSPENDED', version=self.version + 1, reason=reason)
        self.record_event(event)

    def grant_permission(self, permission: str, resource: str) -> None:
        """Command: Grant a permission to the user."""
        perm_key = f'{permission}:{resource}'
        if perm_key in self.permissions:
            raise ValueError(f'Permission already granted: {perm_key}')
        event = PermissionGrantedEvent(aggregate_id=self.id, event_type='PERMISSION_GRANTED', version=self.version + 1, permission=permission, resource=resource)
        self.record_event(event)

    def revoke_permission(self, permission: str, resource: str) -> None:
        """Command: Revoke a permission from the user."""
        perm_key = f'{permission}:{resource}'
        if perm_key not in self.permissions:
            raise ValueError(f'Permission not found: {perm_key}')
        event = PermissionRevokedEvent(aggregate_id=self.id, event_type='PERMISSION_REVOKED', version=self.version + 1, permission=permission, resource=resource)
        self.record_event(event)

    def _on_user_created(self, event: UserCreatedEvent) -> None:
        """Apply USER_CREATED event."""
        self.email = event.email
        self.name = event.name
        self.tenant_id = event.tenant_id
        self.status = UserStatus.CREATED
        self.created_at = event.timestamp
        self.updated_at = event.timestamp

    def _on_user_activated(self, event: UserActivatedEvent) -> None:
        """Apply USER_ACTIVATED event."""
        self.status = UserStatus.ACTIVE
        self.updated_at = event.timestamp

    def _on_user_suspended(self, event: UserSuspendedEvent) -> None:
        """Apply USER_SUSPENDED event."""
        self.status = UserStatus.SUSPENDED
        self.updated_at = event.timestamp

    def _on_permission_granted(self, event: PermissionGrantedEvent) -> None:
        """Apply PERMISSION_GRANTED event."""
        perm_key = f'{event.permission}:{event.resource}'
        self.permissions.add(perm_key)
        self.updated_at = event.timestamp

    def _on_permission_revoked(self, event: PermissionRevokedEvent) -> None:
        """Apply PERMISSION_REVOKED event."""
        perm_key = f'{event.permission}:{event.resource}'
        self.permissions.discard(perm_key)
        self.updated_at = event.timestamp