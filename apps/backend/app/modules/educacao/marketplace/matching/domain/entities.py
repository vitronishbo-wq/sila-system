"""Domain entities for Matching subdomain"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class Match:
    """Entidade de Match entre Cidadão e Oportunidade"""
    citizen_id: str
    opportunity_id: str
    match_score: float  # 0-100
    eligibility_status: str  # eligible, ineligible, pending
    compatibility_level: str  # high, medium, low
    reasons: List[str]
    created_at: datetime


@dataclass
class EligibilityRule:
    """Entidade de Regra de Elegibilidade"""
    id: str
    opportunity_id: str
    rule_name: str
    rule_description: str
    validation_logic: str
    mandatory: bool
    created_at: datetime
