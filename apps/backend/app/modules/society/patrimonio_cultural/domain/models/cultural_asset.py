from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from apps.backend.app.modules.society.patrimonio_cultural.domain.enums import (
    ActionType,
    AssetStatus,
    AssetType,
    ClassificationLevel,
    ClassificationType,
)
from apps.backend.app.modules.society.patrimonio_cultural.domain.exceptions import (
    UNESCOPreconditionError,
)
from apps.backend.app.modules.society.patrimonio_cultural.domain.models.cultural_event import (
    CulturalEvent,
)
from apps.backend.app.modules.society.patrimonio_cultural.domain.models.heritage_classification import (
    HeritageClassification,
)
from apps.backend.app.modules.society.patrimonio_cultural.domain.models.preservation_action import (
    PreservationAction,
)


@dataclass(kw_only=True)
class CulturalAsset:
    asset_id: UUID = field(default_factory=uuid4)
    name: str
    asset_type: AssetType
    description: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    altitude: float | None = None
    province: str | None = None
    municipality: str | None = None
    address: str | None = None
    status: AssetStatus = AssetStatus.REGISTERED
    classification_level: ClassificationLevel | None = None
    classification_date: datetime | None = None
    historical_period: str | None = None
    cultural_significance: str | None = None
    legal_reference: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None
    classifications: list[HeritageClassification] = field(default_factory=list)
    events: list[CulturalEvent] = field(default_factory=list)
    preservation_actions: list[PreservationAction] = field(default_factory=list)

    @property
    def is_protected(self) -> bool:
        return self.status == AssetStatus.PROTECTED

    @property
    def has_unesco_classification(self) -> bool:
        return self.classification_level in {
            ClassificationLevel.UNESCO,
            ClassificationLevel.WORLD_HERITAGE,
        }

    def classify(
        self,
        *,
        level: ClassificationLevel,
        authority: str,
        classification_date: datetime | None = None,
    ) -> None:
        if level in {ClassificationLevel.UNESCO, ClassificationLevel.WORLD_HERITAGE}:
            if self.classification_level != ClassificationLevel.NATIONAL:
                raise UNESCOPreconditionError(
                    "Patrimonio UNESCO exige classificacao nacional previa"
                )
        self.classification_level = level
        self.classification_date = classification_date or datetime.utcnow()
        self.status = AssetStatus.PROTECTED
        self.updated_at = datetime.utcnow()
        self.classifications.append(
            HeritageClassification(
                asset_id=self.asset_id,
                classification_type=self._infer_classification_type(),
                authority=authority,
                classification_date=self.classification_date,
            )
        )

    def add_preservation_action(
        self,
        *,
        action_type: ActionType,
        description: str,
        executed_by: str,
        action_date: datetime | None = None,
    ) -> PreservationAction:
        if not self.is_protected:
            raise ValueError("Apenas patrimonio protegido pode ter acoes registadas")
        action = PreservationAction(
            asset_id=self.asset_id,
            action_type=action_type,
            description=description,
            executed_by=executed_by,
            action_date=action_date or datetime.utcnow(),
        )
        self.preservation_actions.append(action)
        self.updated_at = datetime.utcnow()
        return action

    def add_event(self, *, name: str, event_date: datetime, organizer: str) -> CulturalEvent:
        event = CulturalEvent(
            asset_id=self.asset_id, name=name, event_date=event_date, organizer=organizer
        )
        self.events.append(event)
        self.updated_at = datetime.utcnow()
        return event

    def _infer_classification_type(self) -> ClassificationType:
        mapping = {
            AssetType.MONUMENT: ClassificationType.HISTORIC,
            AssetType.ARCHAEOLOGICAL_SITE: ClassificationType.ARCHAEOLOGICAL,
            AssetType.HISTORIC_BUILDING: ClassificationType.HISTORIC,
            AssetType.CULTURAL_LANDSCAPE: ClassificationType.ETHNOGRAPHIC,
            AssetType.INTANGIBLE_HERITAGE: ClassificationType.ETHNOGRAPHIC,
            AssetType.MUSEUM_COLLECTION: ClassificationType.ARTISTIC,
            AssetType.ARCHAEOLOGICAL_ARTIFACT: ClassificationType.ARCHAEOLOGICAL,
            AssetType.TRADITIONAL_KNOWLEDGE: ClassificationType.ETHNOGRAPHIC,
        }
        return mapping.get(self.asset_type, ClassificationType.HISTORIC)

    def to_dict(self) -> dict:
        return {
            "asset_id": str(self.asset_id),
            "name": self.name,
            "asset_type": self.asset_type.value,
            "description": self.description,
            "province": self.province,
            "municipality": self.municipality,
            "location": {
                "latitude": self.latitude,
                "longitude": self.longitude,
                "altitude": self.altitude,
                "province": self.province,
                "municipality": self.municipality,
                "address": self.address,
            },
            "status": self.status.value,
            "classification_level": self.classification_level.value
            if self.classification_level
            else None,
            "classification_date": self.classification_date.isoformat()
            if self.classification_date
            else None,
            "historical_period": self.historical_period,
            "cultural_significance": self.cultural_significance,
            "legal_reference": self.legal_reference,
            "is_protected": self.is_protected,
            "has_unesco_classification": self.has_unesco_classification,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "classifications": [item.to_dict() for item in self.classifications],
            "events": [item.to_dict() for item in self.events],
            "preservation_actions": [item.to_dict() for item in self.preservation_actions],
        }

    @classmethod
    def from_dict(cls, data: dict) -> CulturalAsset:
        location = data.get("location") or {}
        return cls(
            asset_id=UUID(data["asset_id"]),
            name=data["name"],
            asset_type=AssetType(data["asset_type"]),
            description=data.get("description"),
            latitude=data.get("latitude") or location.get("latitude"),
            longitude=data.get("longitude") or location.get("longitude"),
            altitude=data.get("altitude") or location.get("altitude"),
            province=data.get("province") or location.get("province"),
            municipality=data.get("municipality") or location.get("municipality"),
            address=data.get("address") or location.get("address"),
            status=AssetStatus(data["status"]),
            classification_level=ClassificationLevel(data["classification_level"])
            if data.get("classification_level")
            else None,
            classification_date=datetime.fromisoformat(data["classification_date"])
            if data.get("classification_date")
            else None,
            historical_period=data.get("historical_period"),
            cultural_significance=data.get("cultural_significance"),
            legal_reference=data.get("legal_reference"),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"])
            if data.get("updated_at")
            else None,
            classifications=[
                HeritageClassification.from_dict(item) for item in data.get("classifications", [])
            ],
            events=[CulturalEvent.from_dict(item) for item in data.get("events", [])],
            preservation_actions=[
                PreservationAction.from_dict(item) for item in data.get("preservation_actions", [])
            ],
        )
