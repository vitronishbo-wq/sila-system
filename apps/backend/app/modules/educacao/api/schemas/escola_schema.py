from __future__ import annotations
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.educacao.domain.models import CicloEnsino, TipoEscola

class EscolaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo_med: str
    nome: str
    tipo: TipoEscola
    ciclos: list[CicloEnsino]
    provincia: str
    municipio: str
    comuna: str
    bairro: str
    endereco: str
    contacto: Optional[str] = None
    email: Optional[str] = None
    ativa: bool