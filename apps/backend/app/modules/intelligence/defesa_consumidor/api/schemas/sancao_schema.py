from pydantic import BaseModel

class SancaoResponse(BaseModel):
    reclamacao_id: int
    tipo: str
    status: str