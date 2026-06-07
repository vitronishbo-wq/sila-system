from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from apps.backend.app.modules.society.patrimonio_cultural.domain.enums import ActionType


@dataclass(kw_only=True)
class PreservationAction:
    action_id: UUID = field(default_factory=uuid4)
    asset_id: UUID
    action_type: ActionType
    description: str
    executed_by: str
    action_date: datetime
    cost: float | None = None
    funding_source: str | None = None
    technical_report_url: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def is_completed(self) -> bool:
        return self.action_date <= datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "action_id": str(self.action_id),
            "asset_id": str(self.asset_id),
            "action_type": self.action_type.value,
            "description": self.description,
            "executed_by": self.executed_by,
            "action_date": self.action_date.isoformat(),
            "cost": self.cost,
            "funding_source": self.funding_source,
            "technical_report_url": self.technical_report_url,
            "created_at": self.created_at.isoformat(),
            "is_completed": self.is_completed,
        }

    @classmethod
    def from_dict(cls, data: dict) -> PreservationAction:
        return cls(
            action_id=UUID(data["action_id"]),
            asset_id=UUID(data["asset_id"]),
            action_type=ActionType(data["action_type"]),
            description=data["description"],
            executed_by=data["executed_by"],
            action_date=datetime.fromisoformat(data["action_date"]),
            cost=data.get("cost"),
            funding_source=data.get("funding_source"),
            technical_report_url=data.get("technical_report_url"),
            created_at=datetime.fromisoformat(data["created_at"]),
        )
