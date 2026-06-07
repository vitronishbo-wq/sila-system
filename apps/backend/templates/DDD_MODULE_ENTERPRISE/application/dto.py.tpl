from pydantic import BaseModel


class EntityDTO(BaseModel):
    id: str
    # Add DTO attributes here
