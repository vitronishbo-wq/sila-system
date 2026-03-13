"""
SILA X-Road Domain: Protocol definitions for atomic, signed, auditable exchanges.

Interoperability between:
- Ministry of Justice (MINJUS): Civil Registry, Identification
- Ministry of Health (MINSA): Birth/Death Records, Vaccination
- Ministry of Finance (MINFIN): Tax Registry
"""

from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field


class ServiceType(str, Enum):
    """X-Road service endpoints available in SILA."""
    # Justice ↔ Health
    VERIFY_BIRTH_NOTICE = "VERIFY_BIRTH_NOTICE"           # Justice → Health
    NOTIFY_DEATH_STATUS = "NOTIFY_DEATH_STATUS"           # Health → Justice
    VALIDATE_IDENTITY = "VALIDATE_IDENTITY"               # Health → Justice
    CHECK_RESIDENCE = "CHECK_RESIDENCE"                   # Health → Justice
    
    # Health ↔ Justice
    FETCH_BI_STATUS = "FETCH_BI_STATUS"                   # Health → Justice
    VERIFY_CITIZENSHIP = "VERIFY_CITIZENSHIP"             # Health → Justice
    
    # Shared Services
    SYNC_BIOMETRIC = "SYNC_BIOMETRIC"                     # Justice ↔ Health
    AUDIT_TRAIL_QUERY = "AUDIT_TRAIL_QUERY"               # Any → Audit Service
    SERVICE_DISCOVERY = "SERVICE_DISCOVERY"               # Any → X-Road Registry
    HEALTH_CHECK = "HEALTH_CHECK"                         # Any → Any


class MessageStatus(str, Enum):
    """Lifecycle status of SILA X-Road message."""
    CREATED = "CREATED"
    SIGNED = "SIGNED"
    TRANSMITTED = "TRANSMITTED"
    RECEIVED = "RECEIVED"
    PROCESSED = "PROCESSED"
    ARCHIVED = "ARCHIVED"
    REPLAY_BLOCKED = "REPLAY_BLOCKED"


class OriginMinistry(str, Enum):
    """Government entities participating in SILA exchange."""
    MINJUS = "MINJUS"      # Ministry of Justice
    MINSA = "MINSA"        # Ministry of Health
    MINFIN = "MINFIN"      # Ministry of Finance
    MINACOM = "MINACOM"    # Ministry of Local Government


class SILAEnvelope(BaseModel):
    """
    Atomic exchange unit for government-to-government communication.
    
    Every envelope is:
    1. Unique (message_id prevents replay attacks)
    2. Signed (signature ensures authenticity)
    3. Traced (correlation_id links cause-effect chains)
    4. Immutable (stored in audit trail before processing)
    """

    message_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique identifier (UUID v4), prevents replay attacks"
    )
    
    sender_service: OriginMinistry = Field(
        description="Originating ministry/service"
    )
    
    receiver_service: OriginMinistry = Field(
        description="Destination ministry/service"
    )
    
    service_type: ServiceType = Field(
        description="Type of data exchange (VERIFY_BIRTH_NOTICE, etc)"
    )
    
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        description="ISO 8601 timestamp of creation"
    )
    
    correlation_id: Optional[str] = Field(
        default=None,
        description="Links request-response pairs in audit trail"
    )
    
    payload: Dict[str, Any] = Field(
        description="Service-specific data (varies by service_type)"
    )
    
    signature: Optional[str] = Field(
        default=None,
        description="DSA/RSA signature (populated by Security Server)"
    )
    
    signer_certificate: Optional[str] = Field(
        default=None,
        description="X.509 certificate of signing authority"
    )
    
    trust_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Caller's sovereign trust score (validated by Trust Engine)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "message_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                "sender_service": "MINJUS",
                "receiver_service": "MINSA",
                "service_type": "VERIFY_BIRTH_NOTICE",
                "timestamp": "2026-03-11T14:45:00Z",
                "correlation_id": None,
                "payload": {
                    "citizen_nif": "123456789",
                    "birth_certificate_id": "BI_12345",
                    "query_reason": "IDENTITY_DOCUMENT_ISSUANCE"
                },
                "signature": "<base64-encoded-signature>",
                "trust_score": 0.92
            }
        }


class SILAEnvelopeResponse(BaseModel):
    """
    Response envelope from X-Road service.
    
    Maintains request-response traceability via correlation_id.
    """

    message_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Response message ID (different from request)"
    )
    
    correlation_id: str = Field(
        description="References original request message_id"
    )
    
    status: MessageStatus = Field(
        description="Processing outcome"
    )
    
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        description="When response was created"
    )
    
    payload: Dict[str, Any] = Field(
        description="Result data (varies by service_type)"
    )
    
    error: Optional[str] = Field(
        default=None,
        description="Error message if status != PROCESSED"
    )
    
    audit_record_id: str = Field(
        description="Reference to immutable audit trail entry"
    )


class InteroperabilityPolicy(BaseModel):
    """
    Rules governing X-Road exchanges between specific ministries.
    
    Example: MINJUS can request VERIFY_BIRTH_NOTICE from MINSA,
    but cannot request FETCH_BI_STATUS (reverse not allowed).
    """

    sender: OriginMinistry
    receiver: OriginMinistry
    allowed_service_types: list[ServiceType]
    requires_high_trust_score: bool = Field(
        default=True,
        description="If True, sender must have trust_score >= 0.85"
    )
    max_retry_attempts: int = 3
    timeout_seconds: int = 30
    requires_signature: bool = True

    class Config:
        json_schema_extra = {
            "example": {
                "sender": "MINJUS",
                "receiver": "MINSA",
                "allowed_service_types": [
                    "VERIFY_BIRTH_NOTICE",
                    "CHECK_RESIDENCE"
                ],
                "requires_high_trust_score": True,
                "max_retry_attempts": 3,
                "timeout_seconds": 30,
                "requires_signature": True
            }
        }
