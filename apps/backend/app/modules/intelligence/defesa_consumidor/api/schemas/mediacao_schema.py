from pydantic import BaseModel

class MediacaoResponse(BaseModel):
    reclamacao_id: int
    status: str