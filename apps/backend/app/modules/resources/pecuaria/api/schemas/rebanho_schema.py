from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from apps.backend.app.modules.resources.pecuaria.domain.enums import StatusRebanho, TipoAnimal


class RebanhoCreate(BaseModel):
    propriedade_id: UUID
    tipo_animal: TipoAnimal
    descricao: str
    quantidade_animais: int = 0


class RebanhoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_rebanho: str
    propriedade_id: UUID
    tipo_animal: TipoAnimal
    descricao: str
    quantidade_animais: int
    data_cadastro: date
    status: StatusRebanho
