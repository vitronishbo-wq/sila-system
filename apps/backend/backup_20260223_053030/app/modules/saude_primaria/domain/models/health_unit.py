"""Health Unit Domain Model"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID, uuid4

from ..enums import HealthUnitType


@dataclass
class HealthUnit:
    """Unidade de saúde - Aggregate Root"""
    code: str
    name: str
    unit_type: HealthUnitType
    province: str
    municipality: str
    id: UUID = field(default_factory=uuid4)
    
    # Localização
    commune: Optional[str] = None
    address: str = ""
    phone: Optional[str] = None
    email: Optional[str] = None
    
    # Capacidade
    beds: int = 0
    has_emergency: bool = False
    has_laboratory: bool = False
    has_pharmacy: bool = False
    
    # Serviços
    specialties: List[str] = field(default_factory=list)
    
    # Horário
    opening_hours: Dict[str, str] = field(default_factory=dict)
    
    # Metadados
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Status
    is_active: bool = True
    
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.code or len(self.code.strip()) < 2:
            raise ValueError("Código deve ter pelo menos 2 caracteres")
        self.code = self.code.upper().strip()
    
    def add_specialty(self, specialty: str):
        """Adiciona especialidade"""
        if specialty not in self.specialties:
            self.specialties.append(specialty)
            self.updated_at = datetime.now()
    
    def remove_specialty(self, specialty: str):
        """Remove especialidade"""
        if specialty in self.specialties:
            self.specialties.remove(specialty)
            self.updated_at = datetime.now()
    
    def deactivate(self):
        """Desativa unidade"""
        self.is_active = False
        self.updated_at = datetime.now()
    
    def activate(self):
        """Ativa unidade"""
        self.is_active = True
        self.updated_at = datetime.now()
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "code": self.code,
            "name": self.name,
            "unit_type": self.unit_type.value,
            "province": self.province,
            "municipality": self.municipality,
            "commune": self.commune,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
            "beds": self.beds,
            "has_emergency": self.has_emergency,
            "has_laboratory": self.has_laboratory,
            "has_pharmacy": self.has_pharmacy,
            "specialties": self.specialties,
            "opening_hours": self.opening_hours,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


@dataclass
class HealthProfessional:
    """Profissional de saúde"""
    license_number: str
    specialization: str
    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    health_unit_id: UUID = field(default_factory=uuid4)
    
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
