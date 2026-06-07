from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class VerifiableCredential(BaseModel):
    context: list[str] = Field(default=["https://www.w3.org/2018/credentials/v1"], alias="@context")
    id: str
    type: list[str] = ["VerifiableCredential"]
    issuer: str
    issuance_date: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    credential_subject: dict[str, Any]
    proof: dict[str, Any] | None = None

    class Config:
        populate_by_name = True
