from pydantic import BaseModel


class KPIBase(BaseModel):
    code: str
    value: float


class KPIResponse(KPIBase):
    period: str | None


class KPIDomainResponse(BaseModel):
    domain: str
    reference_date: str
    generated_at: str
    metrics: dict[str, float | int]
    metric_count: int


class KPIConsolidatedResponse(BaseModel):
    reference_date: str
    generated_at: str
    domains: dict[str, dict[str, float | int]]
    unavailable_domains: list[str]
    errors: dict[str, str]
