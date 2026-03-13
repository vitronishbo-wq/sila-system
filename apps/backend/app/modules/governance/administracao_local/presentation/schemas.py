from pydantic import BaseModel

class AdministradorRead(BaseModel):
    id: str
    nome: str
    cargo: str

class AdministradorCreate(BaseModel):
    nome: str
    cargo: str