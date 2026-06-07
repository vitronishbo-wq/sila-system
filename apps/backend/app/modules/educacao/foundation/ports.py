from typing import Any, Protocol


class AuditPort(Protocol):
    def append(self, record: dict[str, Any]) -> None: ...


class EventBusPort(Protocol):
    def publish(self, topic: str, event: dict[str, Any]) -> None: ...


class IdentityPort(Protocol):
    def get_profile(self, identity_id: str) -> dict[str, Any]: ...


class AuthorizationPort(Protocol):
    def has_permission(self, user_id: str, permission: str, tenant_id: str | None = None) -> bool: ...


class WorkflowPort(Protocol):
    def persist_state(self, process_id: str, state: dict[str, Any]) -> None: ...


class NotificationPort(Protocol):
    def send(self, channel: str, to: str, subject: str, body: str, meta: dict[str, Any] | None = None) -> None: ...
