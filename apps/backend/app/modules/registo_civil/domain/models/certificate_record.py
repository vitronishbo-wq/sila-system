from datetime import datetime
from typing import Dict, Any
import enum

class CertificateType(str, enum.Enum):
    BIRTH = "birth"
    MARRIAGE = "marriage"
    DEATH = "death"
    NON_MARRIAGE = "non_marriage"
    CIVIL_STATE = "civil_state"

class CertificateRecord:
    """Modelo de Domínio para Certidões (VO/Entity)."""
    def __init__(
        self,
        id: str,
        type: CertificateType,
        citizen_id: str,
        issued_at: datetime,
        content: Dict[str, Any],
        authenticity_code: str
    ):
        self.id = id
        self.type = type
        self.citizen_id = citizen_id
        self.issued_at = issued_at
        self.content = content
        self.authenticity_code = authenticity_code

    def __repr__(self):
        return f"<CertificateRecord(type={self.type}, citizen={self.citizen_id})>"
