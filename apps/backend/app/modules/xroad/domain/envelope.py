from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4
from typing import Dict, Any

class SILAEnvelope(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid4()))
    sender_service: str
    receiver_service: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    payload: Dict[str, Any]
    signature: str