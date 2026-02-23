"""Prescription Domain Model"""
from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from typing import Optional, Dict, Any, List
from uuid import UUID, uuid4

from ..enums import PrescriptionStatus, MedicationType


@dataclass
class PrescriptionItem:
    """Item de prescrição"""
    medication_code: str
    medication_name: str
    dosage: str
    frequency: str
    duration_days: int
    quantity: int
    unit: str
    notes: Optional[str] = None
    medication_type: MedicationType = MedicationType.OCCASIONAL


@dataclass
class Prescription:
    """Prescrição médica - Aggregate Root"""
    id: UUID = field(default_factory=uuid4)
    prescription_number: Optional[str] = None
    
    # Identidades
    citizen_id: UUID = field(default_factory=uuid4)
    doctor_id: UUID = field(default_factory=uuid4)
    appointment_id: Optional[UUID] = None
    health_unit_id: UUID = field(default_factory=uuid4)
    
    # Dados da prescrição
    items: List[PrescriptionItem] = field(default_factory=list)
    clinical_notes: Optional[str] = None
    recommendations: Optional[str] = None
    
    # Validade
    issue_date: date = field(default_factory=date.today)
    expiry_date: Optional[date] = None
    
    # Status
    status: PrescriptionStatus = PrescriptionStatus.ACTIVE
    
    # Workflow
    workflow_instance_id: Optional[UUID] = None
    
    # Metadados
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Datas
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    dispensed_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.items:
            raise ValueError("Prescrição deve ter pelo menos um item")
        
        if not self.expiry_date:
            self.expiry_date = self.issue_date + timedelta(days=30)
    
    @property
    def is_active(self) -> bool:
        return self.status == PrescriptionStatus.ACTIVE
    
    @property
    def is_expired(self) -> bool:
        if self.expiry_date and date.today() > self.expiry_date:
            return True
        return False
    
    @property
    def total_items(self) -> int:
        return len(self.items)
    
    def add_item(self, item: PrescriptionItem):
        """Adiciona item à prescrição"""
        self.items.append(item)
        self.updated_at = datetime.now()
    
    def remove_item(self, medication_code: str):
        """Remove item da prescrição"""
        self.items = [i for i in self.items if i.medication_code != medication_code]
        self.updated_at = datetime.now()
    
    def dispense(self, items_dispensed: List[str] = None):
        """Registra dispensação"""
        if items_dispensed and len(items_dispensed) < len(self.items):
            self.status = PrescriptionStatus.PARTIALLY_DISPENSED
        else:
            self.status = PrescriptionStatus.DISPENSED
        
        self.dispensed_at = datetime.now()
        self.updated_at = datetime.now()
        self.metadata["dispensed_items"] = items_dispensed or [i.medication_code for i in self.items]
    
    def cancel(self, reason: str, cancelled_by: UUID):
        """Cancela a prescrição"""
        self.status = PrescriptionStatus.CANCELLED
        self.updated_at = datetime.now()
        self.metadata["cancelled_by"] = str(cancelled_by)
        self.metadata["cancelled_at"] = datetime.now().isoformat()
        self.metadata["cancellation_reason"] = reason
    
    def check_expiry(self) -> bool:
        """Verifica se expirou e atualiza status"""
        if self.is_expired and self.status == PrescriptionStatus.ACTIVE:
            self.status = PrescriptionStatus.EXPIRED
            self.updated_at = datetime.now()
            return True
        return False
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "prescription_number": self.prescription_number,
            "citizen_id": str(self.citizen_id),
            "doctor_id": str(self.doctor_id),
            "appointment_id": str(self.appointment_id) if self.appointment_id else None,
            "health_unit_id": str(self.health_unit_id),
            "items": [
                {
                    "medication_code": i.medication_code,
                    "medication_name": i.medication_name,
                    "dosage": i.dosage,
                    "frequency": i.frequency,
                    "duration_days": i.duration_days,
                    "quantity": i.quantity,
                    "unit": i.unit,
                    "notes": i.notes,
                    "medication_type": i.medication_type.value
                }
                for i in self.items
            ],
            "clinical_notes": self.clinical_notes,
            "recommendations": self.recommendations,
            "issue_date": self.issue_date.isoformat(),
            "expiry_date": self.expiry_date.isoformat() if self.expiry_date else None,
            "status": self.status.value,
            "is_active": self.is_active,
            "is_expired": self.is_expired,
            "workflow_instance_id": str(self.workflow_instance_id) if self.workflow_instance_id else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "dispensed_at": self.dispensed_at.isoformat() if self.dispensed_at else None
        }
