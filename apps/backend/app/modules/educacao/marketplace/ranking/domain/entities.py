"""Domain entities for Ranking subdomain"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class InstitutionMetrics:
    """Entidade de Métricas de Instituição"""
    institution_id: str
    quality_score: float  # 0-100
    reputation_score: float  # 0-100
    accessibility_score: float  # 0-100
    employment_rate: float  # 0-100
    student_satisfaction: float  # 0-5
    number_programs: int
    total_students: int
    updated_at: datetime


@dataclass
class RankingEntry:
    """Entidade de Entrada em Ranking"""
    rank: int
    institution_id: str
    institution_name: str
    score: float
    change_from_last: int  # +/- posições
    metrics: InstitutionMetrics
