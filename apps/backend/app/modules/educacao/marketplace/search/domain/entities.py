"""Domain entities for Search subdomain"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class SearchQuery:
    """Entidade de Query de Busca"""
    id: str
    query_text: str
    filters: dict
    results_count: int
    execution_time_ms: float
    created_at: datetime


@dataclass
class SearchResult:
    """Entidade de Resultado de Busca"""
    id: str
    type: str  # opportunity, institution, program
    title: str
    description: str
    metadata: dict
    relevance_score: float
