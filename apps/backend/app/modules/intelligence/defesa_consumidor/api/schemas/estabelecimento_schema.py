from pydantic import BaseModel


class EstabelecimentoResponse(BaseModel):
    id: int
    nome_fantasia: str
