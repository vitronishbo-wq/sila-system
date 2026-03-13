from pydantic import BaseModel

class ConsumidorResponse(BaseModel):
    id: int
    nome: str