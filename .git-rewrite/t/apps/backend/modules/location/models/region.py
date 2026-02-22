"""
Region Model for Location Module

This module defines the Region model that was moved from app.models to maintain
proper module organization.
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.db.base_class import Base


class Region(Base):
    __table_args__ = {"extend_existing": True}
    """Modelo para regiões geográficas (países, províncias, municípios)."""
    __tablename__ = "location_region"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False)  # "municipio" | "provincia" | "pais"
    parent_id = Column(
        Integer, ForeignKey("location_region.id"), nullable=True
    )

    parent = relationship("Region", remote_side=[id], backref="children")
