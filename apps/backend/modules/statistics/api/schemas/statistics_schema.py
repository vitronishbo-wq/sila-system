from pydantic import BaseModel
from typing import Optional, List


class StatisticCreateSchema(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    unit: Optional[str] = None
    source_module: Optional[str] = None


class StatisticSchema(StatisticCreateSchema):
    id: int
    created_at: Optional[str]

    class Config:
        from_attributes = True


class LatestValueSchema(BaseModel):
    value: float
    period_start: Optional[str]

    class Config:
        from_attributes = True


class StatisticDetailSchema(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str]
    unit: Optional[str]
    source_module: Optional[str]
    created_at: Optional[str]
    total_records: int
    latest_value: Optional[LatestValueSchema]

    class Config:
        from_attributes = True

