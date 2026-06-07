from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class NamedEntityCreate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=200)
    descricao: str | None = Field(None, max_length=5000)
    conteudo: dict[str, Any] | None = None


class NamedEntityUpdate(BaseModel):
    nome: str | None = Field(None, min_length=3, max_length=200)
    descricao: str | None = Field(None, max_length=5000)
    conteudo: dict[str, Any] | None = None


class NamedEntityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    descricao: str | None
    conteudo: dict[str, Any] | None
    data_criacao: datetime
    data_atualizacao: datetime | None


class NamedEntityListResponse(BaseModel):
    itens: list[NamedEntityResponse]
    total: int
    pagina: int
    tamanho_pagina: int
