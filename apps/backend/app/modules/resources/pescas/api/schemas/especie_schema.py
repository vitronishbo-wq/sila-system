from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class EspecieCreate(BaseModel):
    nome_comum: str = Field(..., min_length=2)
    nome_cientifico: str = Field(..., min_length=2)
    codigo_fao: str = Field(..., min_length=2)


class EspecieResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    nome_comum: str
    nome_cientifico: str
    codigo_fao: str
    ameacada: bool = False
    observacoes: str | None = None
