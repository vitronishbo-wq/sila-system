"""Read-model: institution_marketplace_projection

This is a CQRS read-model optimized for marketplace queries.
"""
from __future__ import annotations

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from apps.backend.app.core.db import Base


class InstitutionMarketplaceProjection(Base):
    __tablename__ = "institution_marketplace_projection"
    id = Column(Integer, primary_key=True, autoincrement=True)
    institution_id = Column(PGUUID(as_uuid=True), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(64), nullable=True)
    city = Column(String(128), nullable=True)
    district = Column(String(128), nullable=True)
    rating = Column(Float, nullable=True)
    available_slots = Column(Integer, nullable=True)
    monthly_fee = Column(Integer, nullable=True)
    distance_score = Column(Float, nullable=True)
    approval_rate = Column(Float, nullable=True)
    transfer_acceptance_rate = Column(Float, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "institution_id": str(self.institution_id),
            "name": self.name,
            "type": self.type,
            "city": self.city,
            "district": self.district,
            "rating": self.rating,
            "available_slots": self.available_slots,
            "monthly_fee": self.monthly_fee,
            "distance_score": self.distance_score,
            "approval_rate": self.approval_rate,
            "transfer_acceptance_rate": self.transfer_acceptance_rate,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
