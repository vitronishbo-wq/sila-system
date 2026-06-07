from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class ConsentStatus(str, Enum):
    GRANTED = "granted"
    DENIED = "denied"
    REVOKED = "revoked"
    EXPIRED = "expired"


@dataclass
class Consent:
    """Consentimento do cidadão para partilha de dados entre módulos.
    
    Exemplo: cidadão autoriza que a Educação consulte dados de identidade
    do módulo Identity para validar matrícula.
    """
    id: str
    citizen_id: str
    source_module: str
    target_module: str
    purpose: str
    data_types: list[str]
    status: ConsentStatus = ConsentStatus.GRANTED
    granted_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None
    revoked_at: Optional[datetime] = None


class ConsentManager:
    """Gestor de consentimento do cidadão para interoperabilidade."""

    def __init__(self) -> None:
        self._consents: list[Consent] = []

    def grant(self, citizen_id: str, source: str, target: str,
              purpose: str, data_types: list[str],
              expires_at: Optional[datetime] = None) -> Consent:
        consent = Consent(
            id=f"{citizen_id}-{source}-{target}-{purpose}",
            citizen_id=citizen_id, source_module=source,
            target_module=target, purpose=purpose,
            data_types=data_types, expires_at=expires_at,
        )
        self._consents.append(consent)
        return consent

    def revoke(self, consent_id: str) -> bool:
        for c in self._consents:
            if c.id == consent_id and c.status == ConsentStatus.GRANTED:
                c.status = ConsentStatus.REVOKED
                c.revoked_at = datetime.now(timezone.utc)
                return True
        return False

    def check(self, citizen_id: str, source: str, target: str,
              data_type: str) -> bool:
        now = datetime.now(timezone.utc)
        for c in self._consents:
            if (c.citizen_id == citizen_id and c.source_module == source
                    and c.target_module == target
                    and data_type in c.data_types
                    and c.status == ConsentStatus.GRANTED):
                if c.expires_at and now > c.expires_at:
                    c.status = ConsentStatus.EXPIRED
                    return False
                return True
        return False

    def list_by_citizen(self, citizen_id: str) -> list[Consent]:
        return [c for c in self._consents if c.citizen_id == citizen_id]

    def list_by_target(self, target_module: str) -> list[Consent]:
        return [c for c in self._consents if c.target_module == target_module]
