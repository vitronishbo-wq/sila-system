from __future__ import annotations

from pydantic import BaseModel


class CatalogoItemSchema(BaseModel):
    codigo: str
    descricao: str
