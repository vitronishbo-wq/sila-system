from pydantic import BaseModel
from typing import Optional

class AdministradorDTO(BaseModel):
    id: str
    nome: str
    cargo: str

class CreateAdministradorDTO(BaseModel):
    nome: str
    cargo: str