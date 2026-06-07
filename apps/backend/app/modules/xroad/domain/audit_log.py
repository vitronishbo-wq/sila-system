import hashlib
from datetime import datetime

from pydantic import BaseModel


class AuditEntry(BaseModel):
    message_id: str
    origin: str
    destination: str
    payload_hash: str
    timestamp: str = datetime.utcnow().isoformat()
    previous_hash: str = "0"

    def compute_hash(self) -> str:
        data = f"{self.message_id}{self.origin}{self.destination}{self.payload_hash}{self.timestamp}{self.previous_hash}"
        return hashlib.sha256(data.encode()).hexdigest()
