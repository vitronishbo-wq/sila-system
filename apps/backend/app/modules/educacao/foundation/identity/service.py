from __future__ import annotations

from typing import Any


class AcademicIdentityService:
    """Minimal in-memory identity service for academic profiles.

    Replace or adapt this with the real identity store or external IdP.
    """

    def __init__(self) -> None:
        # simple in-memory store for demo purposes
        self._store: dict[str, dict[str, Any]] = {}

    def create_profile(self, identity_id: str, profile: dict[str, Any]) -> None:
        self._store[identity_id] = profile

    def get_profile(self, identity_id: str) -> dict[str, Any] | None:
        return self._store.get(identity_id)

    def update_profile(self, identity_id: str, patch: dict[str, Any]) -> None:
        if identity_id not in self._store:
            raise KeyError("identity not found")
        self._store[identity_id].update(patch)
