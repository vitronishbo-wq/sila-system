"""Identity domain queries."""

from dataclasses import dataclass


@dataclass
class GetIdentityByCitizenQuery:
    """Query to retrieve identity by citizen ID."""

    citizen_id: str


@dataclass
class GetTrustScoreQuery:
    """Query to get trust score."""

    identity_id: str


@dataclass
class ListIdentitiesQuery:
    """Query to list identities."""

    limit: int = 100
    offset: int = 0
