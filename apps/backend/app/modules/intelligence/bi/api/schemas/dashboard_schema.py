from typing import Any, Optional
from pydantic import BaseModel

class DashboardCreateSchema(BaseModel):
    name: str
    description: Optional[str]
    owner_id: Optional[int]
    layout: Optional[Any]

class DashboardSchema(DashboardCreateSchema):
    id: int
    created_at: Optional[str]

class DashboardDomainDataResponse(BaseModel):
    domain: str
    reference_date: str
    generated_at: str
    metrics: dict[str, float | int]
    metric_count: int

class DashboardExecutiveResponse(BaseModel):
    reference_date: str
    generated_at: str
    summary: dict[str, Any]
    domains: dict[str, dict[str, float | int]]
    unavailable_domains: list[str]
    errors: dict[str, str]