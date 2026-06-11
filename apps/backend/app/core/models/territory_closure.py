
from __future__ import annotations
import uuid
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.core.db.base_class import Base

class TerritoryClosure(Base):
    __tablename__ = "territory_closure"
    __table_args__ = (
        {"comment": "Tabela de Fechamento Transitivo para hierarquias territoriais. Permite consultas eficientes de ancestralidade e descendência."}
    )

    ancestor_id: uuid.UUID = Column(
        ForeignKey("locations.id", ondelete="CASCADE"), primary_key=True
    )
    descendant_id: uuid.UUID = Column(
        ForeignKey("locations.id", ondelete="CASCADE"), primary_key=True
    )
    depth: int = Column(Integer, nullable=False)

    ancestor = relationship("Location", foreign_keys=[ancestor_id])
    descendant = relationship("Location", foreign_keys=[descendant_id])
