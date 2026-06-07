from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class SignatureStatus(str, Enum):
    PENDING = "pending"
    SIGNED = "signed"
    VERIFIED = "verified"
    EXPIRED = "expired"
    REVOKED = "revoked"


@dataclass
class DigitalSignature:
    signer_id: str
    signer_role: str
    document_id: str
    module: str
    signature_hash: Optional[str] = None
    status: SignatureStatus = SignatureStatus.PENDING
    signed_at: Optional[datetime] = None
    verified_at: Optional[datetime] = None
    certificate_serial: Optional[str] = None


class SignatureEngine:
    """Engine de assinatura digital para atos administrativos."""

    def __init__(self) -> None:
        self._signatures: list[DigitalSignature] = []

    def sign(self, signer_id: str, signer_role: str, document_id: str,
             module: str, certificate_serial: Optional[str] = None) -> DigitalSignature:
        sig = DigitalSignature(
            signer_id=signer_id,
            signer_role=signer_role,
            document_id=document_id,
            module=module,
            status=SignatureStatus.SIGNED,
            signed_at=datetime.now(timezone.utc),
            certificate_serial=certificate_serial,
        )
        self._signatures.append(sig)
        return sig

    def verify(self, document_id: str) -> Optional[DigitalSignature]:
        for sig in self._signatures:
            if sig.document_id == document_id and sig.status == SignatureStatus.SIGNED:
                sig.status = SignatureStatus.VERIFIED
                sig.verified_at = datetime.now(timezone.utc)
                return sig
        return None

    def revoke(self, document_id: str) -> bool:
        for sig in self._signatures:
            if sig.document_id == document_id and sig.status == SignatureStatus.SIGNED:
                sig.status = SignatureStatus.REVOKED
                return True
        return False

    def list_by_signer(self, signer_id: str) -> list[DigitalSignature]:
        return [s for s in self._signatures if s.signer_id == signer_id]
