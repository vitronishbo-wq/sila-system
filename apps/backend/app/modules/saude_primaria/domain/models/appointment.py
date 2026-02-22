"""Appointment Domain Model"""
from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import Optional, Dict, Any, List
from uuid import UUID, uuid4

from ..enums import AppointmentStatus, AppointmentType, PriorityLevel


@dataclass
class Appointment:
    """Consulta médica - Aggregate Root"""
    id: UUID = field(default_factory=uuid4)
    appointment_number: Optional[str] = None
    
    # Identidades
    citizen_id: UUID = field(default_factory=uuid4)
    created_by: UUID = field(default_factory=uuid4)
    doctor_id: Optional[UUID] = None
    health_unit_id: UUID = field(default_factory=uuid4)
    
    # Dados da consulta
    appointment_type: AppointmentType = AppointmentType.ROUTINE
    specialty: str = ""
    appointment_date: date = field(default_factory=date.today)
    appointment_time: time = field(default_factory=lambda: time(9, 0))
    duration_minutes: int = 30
    
    # Status
    status: AppointmentStatus = AppointmentStatus.SCHEDULED
    priority: PriorityLevel = PriorityLevel.MEDIUM
    
    # Motivo
    reason: str = ""
    symptoms: Optional[str] = None
    notes: Optional[str] = None
    
    # Workflow
    workflow_instance_id: Optional[UUID] = None
    workflow_data: Dict[str, Any] = field(default_factory=dict)
    
    # Metadados
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    
    # Datas
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    confirmed_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    cancelled_reason: Optional[str] = None
    
    def __post_init__(self):
        if not self.reason or len(self.reason.strip()) < 5:
            raise ValueError("Motivo deve ter pelo menos 5 caracteres")
    
    @property
    def is_scheduled(self) -> bool:
        return self.status == AppointmentStatus.SCHEDULED
    
    @property
    def is_confirmed(self) -> bool:
        return self.status == AppointmentStatus.CONFIRMED
    
    @property
    def is_completed(self) -> bool:
        return self.status == AppointmentStatus.COMPLETED
    
    @property
    def is_cancelled(self) -> bool:
        return self.status == AppointmentStatus.CANCELLED
    
    @property
    def is_missed(self) -> bool:
        return self.status == AppointmentStatus.MISSED
    
    def confirm(self):
        """Confirma a consulta"""
        if self.status != AppointmentStatus.SCHEDULED:
            raise ValueError(f"Não é possível confirmar consulta com status {self.status}")
        
        self.status = AppointmentStatus.CONFIRMED
        self.confirmed_at = datetime.now()
        self.updated_at = datetime.now()
    
    def start(self):
        """Inicia a consulta"""
        if self.status not in [AppointmentStatus.SCHEDULED, AppointmentStatus.CONFIRMED]:
            raise ValueError(f"Não é possível iniciar consulta com status {self.status}")
        
        self.status = AppointmentStatus.IN_PROGRESS
        self.updated_at = datetime.now()
    
    def complete(self):
        """Finaliza a consulta"""
        if self.status != AppointmentStatus.IN_PROGRESS:
            raise ValueError(f"Não é possível finalizar consulta com status {self.status}")
        
        self.status = AppointmentStatus.COMPLETED
        self.completed_at = datetime.now()
        self.updated_at = datetime.now()
    
    def cancel(self, reason: str, cancelled_by: UUID):
        """Cancela a consulta"""
        if self.status in [AppointmentStatus.COMPLETED, AppointmentStatus.CANCELLED]:
            raise ValueError(f"Não é possível cancelar consulta com status {self.status}")
        
        self.status = AppointmentStatus.CANCELLED
        self.cancelled_at = datetime.now()
        self.cancelled_reason = reason
        self.updated_at = datetime.now()
        self.metadata["cancelled_by"] = str(cancelled_by)
    
    def reschedule(self, new_date: date, new_time: time, rescheduled_by: UUID):
        """Reagenda a consulta"""
        if self.status in [AppointmentStatus.COMPLETED, AppointmentStatus.CANCELLED]:
            raise ValueError(f"Não é possível reagendar consulta com status {self.status}")
        
        old_date = self.appointment_date
        old_time = self.appointment_time
        
        self.appointment_date = new_date
        self.appointment_time = new_time
        self.status = AppointmentStatus.RESCHEDULED
        self.updated_at = datetime.now()
        
        if "reschedule_history" not in self.metadata:
            self.metadata["reschedule_history"] = []
        
        self.metadata["reschedule_history"].append({
            "old_date": old_date.isoformat(),
            "old_time": old_time.isoformat(),
            "new_date": new_date.isoformat(),
            "new_time": new_time.isoformat(),
            "rescheduled_by": str(rescheduled_by),
            "rescheduled_at": datetime.now().isoformat()
        })
    
    def mark_missed(self):
        """Marca como não compareceu"""
        if self.status not in [AppointmentStatus.SCHEDULED, AppointmentStatus.CONFIRMED]:
            raise ValueError(f"Não é possível marcar como faltoso com status {self.status}")
        
        self.status = AppointmentStatus.MISSED
        self.updated_at = datetime.now()
    
    def assign_doctor(self, doctor_id: UUID, assigned_by: UUID):
        """Atribui médico à consulta"""
        self.doctor_id = doctor_id
        self.updated_at = datetime.now()
        self.metadata["assigned_by"] = str(assigned_by)
        self.metadata["assigned_at"] = datetime.now().isoformat()
    
    def link_workflow(self, workflow_instance_id: UUID):
        """Vincula instância de workflow"""
        self.workflow_instance_id = workflow_instance_id
        self.updated_at = datetime.now()
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "appointment_number": self.appointment_number,
            "citizen_id": str(self.citizen_id),
            "created_by": str(self.created_by),
            "doctor_id": str(self.doctor_id) if self.doctor_id else None,
            "health_unit_id": str(self.health_unit_id),
            "appointment_type": self.appointment_type.value,
            "specialty": self.specialty,
            "appointment_date": self.appointment_date.isoformat(),
            "appointment_time": self.appointment_time.isoformat(),
            "duration_minutes": self.duration_minutes,
            "status": self.status.value,
            "priority": self.priority.value,
            "reason": self.reason,
            "symptoms": self.symptoms,
            "notes": self.notes,
            "workflow_instance_id": str(self.workflow_instance_id) if self.workflow_instance_id else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "confirmed_at": self.confirmed_at.isoformat() if self.confirmed_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "cancelled_at": self.cancelled_at.isoformat() if self.cancelled_at else None,
            "cancelled_reason": self.cancelled_reason
        }
