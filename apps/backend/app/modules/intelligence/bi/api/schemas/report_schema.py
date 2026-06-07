from typing import Any

from pydantic import BaseModel


class RunReportSchema(BaseModel):
    report_id: int
    parameters: dict[str, Any] | None = {}


class ReportSchema(BaseModel):
    id: int
    name: str
    query: str
    parameters: dict[str, Any] | None
    created_by: int | None
    created_at: str | None
