from pydantic import BaseModel


class StatisticCreateSchema(BaseModel):
    name: str
    code: str
    description: str | None = None
    unit: str | None = None
    source_module: str | None = None


class StatisticSchema(StatisticCreateSchema):
    id: int
    created_at: str | None

    class Config:
        from_attributes = True


class LatestValueSchema(BaseModel):
    value: float
    period_start: str | None

    class Config:
        from_attributes = True


class StatisticDetailSchema(BaseModel):
    id: int
    name: str
    code: str
    description: str | None
    unit: str | None
    source_module: str | None
    created_at: str | None
    total_records: int
    latest_value: LatestValueSchema | None

    class Config:
        from_attributes = True
