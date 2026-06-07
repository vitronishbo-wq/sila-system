"""Domain entities for Discovery subdomain"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Opportunity:
    """Entidade de Oportunidade Educacional"""
    id: str
    institution_id: str
    program_id: str
    level: str  # básico, médio, superior, etc
    vacancies_total: int
    vacancies_available: int
    modality: str  # presencial, remoto, híbrido
    start_date: datetime
    end_date: Optional[datetime]
    price: Optional[float]
    description: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Institution:
    """Entidade de Instituição Educacional"""
    id: str
    name: str
    type: str  # pública, privada, comunitária
    city: str
    state: str
    latitude: float
    longitude: float
    phone: Optional[str]
    email: str
    website: Optional[str]
    created_at: datetime


@dataclass
class Program:
    """Entidade de Programa Educacional"""
    id: str
    institution_id: str
    name: str
    level: str
    duration_months: int
    description: str
    requirements: list
    created_at: datetime
