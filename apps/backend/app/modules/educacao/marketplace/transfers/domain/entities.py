"""Domain entities for Transfers subdomain"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class TransferRequest:
    """Entidade de Solicitação de Transferência"""
    id: str
    citizen_id: str
    source_institution_id: str
    destination_institution_id: str
    source_program_id: str
    destination_program_id: str
    status: str  # pending, approved, rejected, cancelled
    created_at: datetime
    approved_at: Optional[datetime]


@dataclass
class CurriculumCompatibility:
    """Entidade de Compatibilidade Curricular"""
    source_program_id: str
    destination_program_id: str
    compatible: bool
    credits_transferred: int
    credits_required_for_destination: int
    additional_requirements: List[str]
