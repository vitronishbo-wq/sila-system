from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from pydantic import ConfigDict

class RequestCreate(BaseModel):
    service_id: UUID
    data: Optional[Dict[str, Any]] = None

class RequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    citizen_id: UUID
    service_id: UUID
    state: str
    data: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime