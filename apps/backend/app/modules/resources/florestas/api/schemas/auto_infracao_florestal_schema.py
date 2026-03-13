from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class AutoInfracaoFlorestalCreate(BaseModel):
    codigo: str = Field(..., min_length=2)
    descricao: str = Field(..., min_length=3)

class AutoInfracaoFlorestalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    codigo: str
    descricao: str
    ativo: bool = True
    observacoes: Optional[str] = None