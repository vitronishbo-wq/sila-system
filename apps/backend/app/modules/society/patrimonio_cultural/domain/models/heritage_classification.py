from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from app.modules.society.patrimonio_cultural.domain.enums import ClassificationType

@dataclass(kw_only=True)
class HeritageClassification:
    classification_id: UUID = field(default_factory=uuid4)
    asset_id: UUID
    classification_type: ClassificationType
    authority: str
    classification_date: datetime
    certificate_number: str | None = None
    legal_basis: str | None = None
    validity_period: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def is_valid(self) -> bool:
        return True

    def to_dict(self) -> dict:
        return {'classification_id': str(self.classification_id), 'asset_id': str(self.asset_id), 'classification_type': self.classification_type.value, 'authority': self.authority, 'classification_date': self.classification_date.isoformat(), 'certificate_number': self.certificate_number, 'legal_basis': self.legal_basis, 'validity_period': self.validity_period, 'created_at': self.created_at.isoformat(), 'is_valid': self.is_valid}

    @classmethod
    def from_dict(cls, data: dict) -> 'HeritageClassification':
        return cls(classification_id=UUID(data['classification_id']), asset_id=UUID(data['asset_id']), classification_type=ClassificationType(data['classification_type']), authority=data['authority'], classification_date=datetime.fromisoformat(data['classification_date']), certificate_number=data.get('certificate_number'), legal_basis=data.get('legal_basis'), validity_period=data.get('validity_period'), created_at=datetime.fromisoformat(data['created_at']))