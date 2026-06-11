from __future__ import annotations

import uuid
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from apps.backend.app.core.db import Base

class ProvinciaModel(Base):
    __tablename__ = "territorios_provincias"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)

    municipios: Mapped[list["MunicipioModel"]] = relationship(back_populates="provincia")

class MunicipioModel(Base):
    __tablename__ = "territorios_municipios"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(128), nullable=False)
    provincia_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("territorios_provincias.id"), nullable=False, index=True)

    provincia: Mapped["ProvinciaModel"] = relationship(back_populates="municipios")
    comunas: Mapped[list["ComunaModel"]] = relationship(back_populates="municipio")

class ComunaModel(Base):
    __tablename__ = "territorios_comunas"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(128), nullable=False)
    municipio_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("territorios_municipios.id"), nullable=False, index=True)

    municipio: Mapped["MunicipioModel"] = relationship(back_populates="comunas")