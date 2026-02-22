"""
Region Model for Location Module
Refatorado para suportar a busca recursiva do DataScope (DPA 2024).
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional, List

from config.database import Base

class Region(Base):
    """
    Modelo unificado para a Divisão Político-Administrativa (DPA).
    Serve como a tabela mestra 'locations' referenciada no DataScope.
    """
    __tablename__ = "locations" # Renomeado para consistência com o core.scope
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    
    # Nível: 'PAIS' | 'PROVINCIA' | 'MUNICIPIO' | 'COMUNA'
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Auto-relacionamento para Hierarquia Recursiva
    parent_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("locations.id", ondelete="CASCADE"), nullable=True
    )

    # Relacionamentos ORM
    parent: Mapped[Optional["Region"]] = relationship(
        "Region", remote_side=[id], back_populates="children"
    )
    children: Mapped[List["Region"]] = relationship(
        "Region", back_populates="parent", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Region(name={self.name}, type={self.type}, parent_id={self.parent_id})>"
