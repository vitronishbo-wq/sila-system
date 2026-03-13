from typing import Optional, Dict, Any
from pydantic import BaseModel

class RunReportSchema(BaseModel):
    report_id: int
    parameters: Optional[Dict[str, Any]] = {}

class ReportSchema(BaseModel):
    id: int
    name: str
    query: str
    parameters: Optional[Dict[str, Any]]
    created_by: Optional[int]
    created_at: Optional[str]