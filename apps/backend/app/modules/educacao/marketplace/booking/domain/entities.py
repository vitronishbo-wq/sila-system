"""Domain entities for Booking subdomain"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Booking:
    """Entidade de Reserva"""
    id: str
    citizen_id: str
    opportunity_id: str
    status: str  # reserved, enrolled, cancelled, expired
    reserved_at: datetime
    expires_at: datetime
    enrolled_at: Optional[datetime]
    enrollment_id: Optional[str]


@dataclass
class VacancyReservation:
    """Entidade de Reserva de Vaga"""
    id: str
    opportunity_id: str
    booking_id: str
    reserved_by_citizen_id: str
    reserved_at: datetime
    released_at: Optional[datetime]
