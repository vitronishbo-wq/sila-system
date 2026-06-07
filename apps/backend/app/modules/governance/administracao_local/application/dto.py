from pydantic import BaseModel


class AdministradorDTO(BaseModel):
    id: str
    nome: str
    cargo: str


class CreateAdministradorDTO(BaseModel):
    nome: str
    cargo: str
