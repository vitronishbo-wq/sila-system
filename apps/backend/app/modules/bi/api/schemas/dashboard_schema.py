from typing import Optional, Any
from pydantic import BaseModel


class DashboardCreateSchema(BaseModel):
    name: str
    description: Optional[str]
    owner_id: Optional[int]
    layout: Optional[Any]


class DashboardSchema(DashboardCreateSchema):
    id: int
    created_at: Optional[str]
