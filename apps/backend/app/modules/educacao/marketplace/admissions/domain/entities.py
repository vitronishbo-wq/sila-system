"""Domain entities for Admissions subdomain"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class Admission:
    """Entidade de Processo de Admissão"""
    id: str
    citizen_id: str
    opportunity_id: str
    status: str  # pending, approved, rejected, pending_documents
    created_at: datetime
    processed_at: Optional[datetime]
    approved_at: Optional[datetime]
    decision_letter_url: Optional[str]


@dataclass
class AdmissionEligibility:
    """Entidade de Elegibilidade para Admissão"""
    citizen_id: str
    opportunity_id: str
    is_eligible: bool
    eligibility_score: float
    validation_errors: List[str]
    required_documents: List[str]
    checked_at: datetime
