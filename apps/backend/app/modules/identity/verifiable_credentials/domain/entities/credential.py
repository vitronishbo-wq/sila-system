from datetime import datetime
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

class VerifiableCredential(BaseModel):
    context: List[str] = Field(default=["https://www.w3.org/2018/credentials/v1"], alias="@context")
    id: str
    type: List[str] = ["VerifiableCredential"]
    issuer: str
    issuance_date: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    credential_subject: Dict[str, Any]
    proof: Optional[Dict[str, Any]] = None

    class Config:
        populate_by_name = True
