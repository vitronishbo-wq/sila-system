from pydantic import BaseModel
from typing import List, Optional


class KPIBase(BaseModel):
    code: str
    value: float


class KPIResponse(KPIBase):
    period: Optional[str]
