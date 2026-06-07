from datetime import datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class SILAEnvelope(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid4()))
    sender_service: str
    receiver_service: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    payload: dict[str, Any]
    signature: str
