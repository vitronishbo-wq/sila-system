"""Identity domain commands."""

from dataclasses import dataclass


@dataclass
class CreateIdentityCommand:
    """Command to create/register identity."""

    citizen_id: str
    metadata: dict | None = None


@dataclass
class UpdateTrustScoreCommand:
    """Command to update trust score."""

    identity_id: str
    score: int
    reason: str
    metadata: dict | None = None


@dataclass
class PublishIdentityEventCommand:
    """Command to publish identity event."""

    event_type: str
    identity_id: str
    data: dict
