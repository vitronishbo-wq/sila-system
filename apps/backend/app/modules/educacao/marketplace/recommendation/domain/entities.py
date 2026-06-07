"""Domain entities for Recommendation subdomain"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class Recommendation:
    """Entidade de Recomendação"""
    id: str
    citizen_id: str
    opportunity_id: str
    score: float
    reason: str
    model_version: str
    created_at: datetime


@dataclass
class UserPreference:
    """Entidade de Preferência do Cidadão"""
    citizen_id: str
    preferred_levels: List[str]
    preferred_modalities: List[str]
    preferred_cities: List[str]
    price_max: Optional[float]
    distance_max_km: Optional[float]
    updated_at: datetime
