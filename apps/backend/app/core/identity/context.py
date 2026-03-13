from dataclasses import dataclass
from typing import Any, Mapping
from uuid import UUID, NAMESPACE_DNS, uuid5

@dataclass(frozen=True)
class IdentityContext:
    """Normalized identity context derived from authenticated token payload."""
    payload: Mapping[str, Any]

    def user_id(self) -> UUID:
        return self._resolve_uuid(('user_id', 'id', 'sub', 'email'), namespace='identity-user')

    def citizen_id(self) -> UUID:
        return self._resolve_uuid(('citizen_id', 'user_id', 'id', 'email'), namespace='identity-citizen')

    def email(self) -> str | None:
        value = self.payload.get('email')
        return str(value) if value else None

    def _resolve_uuid(self, keys: tuple[str, ...], namespace: str) -> UUID:
        for key in keys:
            value = self.payload.get(key)
            if not value:
                continue
            try:
                return UUID(str(value))
            except ValueError:
                return uuid5(NAMESPACE_DNS, f'{namespace}:{value}')
        return uuid5(NAMESPACE_DNS, f'{namespace}:anonymous')