"""Vaccine Domain Model"""
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from uuid import UUID, uuid4

from ..enums import VaccineStatus


@dataclass
class Vaccine:
    """Vacina"""
    code: str
    name: str
    id: UUID = field(default_factory=uuid4)
    description: Optional[str] = None
    manufacturer: str = ""
    
    # Doses
    doses_required: int = 1
    dose_interval_days: Optional[int] = None
    
    # Idade mínima (em meses)
    min_age_months: int = 0
    max_age_months: Optional[int] = None
    
    # Contra-indicações
    contraindications: List[str] = field(default_factory=list)
    
    # Metadados
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Status
    is_active: bool = True
    is_mandatory: bool = False
    
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None


@dataclass
class VaccineDose:
    """Dose de vacina aplicada"""
    id: UUID = field(default_factory=uuid4)
    
    # Identidades
    citizen_id: UUID = field(default_factory=uuid4)
    vaccine_id: UUID = field(default_factory=uuid4)
    health_unit_id: UUID = field(default_factory=uuid4)
    applied_by: UUID = field(default_factory=uuid4)
    
    # Dados da dose
    dose_number: int = 1
    batch_number: str = ""
    application_date: date = field(default_factory=date.today)
    next_dose_date: Optional[date] = None
    
    # Status
    status: VaccineStatus = VaccineStatus.APPLIED
    
    # Reações
    adverse_reactions: Optional[str] = None
    
    # Metadados
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.dose_number < 1:
            raise ValueError("Número da dose deve ser >= 1")
    
    @property
    def has_next_dose(self) -> bool:
        return self.next_dose_date is not None
    
    @property
    def is_next_dose_due(self) -> bool:
        if not self.next_dose_date:
            return False
        return date.today() >= self.next_dose_date
    
    def schedule_next_dose(self, next_date: date):
        """Agenda próxima dose"""
        self.next_dose_date = next_date
        self.updated_at = datetime.now()
    
    def record_reaction(self, reaction: str):
        """Registra reação adversa"""
        self.adverse_reactions = reaction
        self.updated_at = datetime.now()
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "citizen_id": str(self.citizen_id),
            "vaccine_id": str(self.vaccine_id),
            "health_unit_id": str(self.health_unit_id),
            "applied_by": str(self.applied_by),
            "dose_number": self.dose_number,
            "batch_number": self.batch_number,
            "application_date": self.application_date.isoformat(),
            "next_dose_date": self.next_dose_date.isoformat() if self.next_dose_date else None,
            "status": self.status.value,
            "adverse_reactions": self.adverse_reactions,
            "has_next_dose": self.has_next_dose,
            "is_next_dose_due": self.is_next_dose_due,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
