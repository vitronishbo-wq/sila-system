"""Exam Request Domain Model"""
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, Dict, Any
from uuid import UUID, uuid4

from ..enums import ExamStatus, PriorityLevel


@dataclass
class ExamRequest:
    """Pedido de exame - Aggregate Root"""
    id: UUID = field(default_factory=uuid4)
    request_number: Optional[str] = None
    
    # Identidades
    citizen_id: UUID = field(default_factory=uuid4)
    doctor_id: UUID = field(default_factory=uuid4)
    health_unit_id: UUID = field(default_factory=uuid4)
    
    # Dados do exame
    exam_type: str
    exam_description: str
    clinical_indication: str
    
    # Status e prioridade
    status: ExamStatus = ExamStatus.REQUESTED
    priority: PriorityLevel = PriorityLevel.MEDIUM
    
    # Datas
    requested_date: date = field(default_factory=date.today)
    scheduled_date: Optional[date] = None
    collection_date: Optional[date] = None
    result_date: Optional[date] = None
    
    # Resultado
    result_file: Optional[str] = None
    result_notes: Optional[str] = None
    
    # Workflow
    workflow_instance_id: Optional[UUID] = None
    
    # Metadados
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.exam_type or len(self.exam_type.strip()) < 2:
            raise ValueError("Tipo de exame deve ter pelo menos 2 caracteres")
    
    @property
    def is_requested(self) -> bool:
        return self.status == ExamStatus.REQUESTED
    
    @property
    def is_collected(self) -> bool:
        return self.status == ExamStatus.COLLECTED
    
    @property
    def is_completed(self) -> bool:
        return self.status == ExamStatus.COMPLETED
    
    def schedule(self, scheduled_date: date):
        """Agenda o exame"""
        if self.status != ExamStatus.REQUESTED:
            raise ValueError(f"Não é possível agendar exame com status {self.status}")
        
        self.scheduled_date = scheduled_date
        self.status = ExamStatus.SCHEDULED
        self.updated_at = datetime.now()
    
    def collect_sample(self):
        """Registra coleta de amostra"""
        if self.status != ExamStatus.SCHEDULED:
            raise ValueError(f"Não é possível coletar amostra com status {self.status}")
        
        self.collection_date = date.today()
        self.status = ExamStatus.COLLECTED
        self.updated_at = datetime.now()
    
    def submit_for_analysis(self):
        """Envia para análise"""
        if self.status != ExamStatus.COLLECTED:
            raise ValueError(f"Não é possível submeter com status {self.status}")
        
        self.status = ExamStatus.IN_ANALYSIS
        self.updated_at = datetime.now()
    
    def complete_exam(self, result_notes: str, result_file: Optional[str] = None):
        """Conclui o exame"""
        if self.status != ExamStatus.IN_ANALYSIS:
            raise ValueError(f"Não é possível concluir exame com status {self.status}")
        
        self.result_date = date.today()
        self.result_notes = result_notes
        self.result_file = result_file
        self.status = ExamStatus.COMPLETED
        self.updated_at = datetime.now()
    
    def cancel_exam(self, reason: str):
        """Cancela o exame"""
        self.status = ExamStatus.CANCELLED
        self.updated_at = datetime.now()
        self.metadata["cancellation_reason"] = reason
        self.metadata["cancelled_at"] = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "request_number": self.request_number,
            "citizen_id": str(self.citizen_id),
            "doctor_id": str(self.doctor_id),
            "health_unit_id": str(self.health_unit_id),
            "exam_type": self.exam_type,
            "exam_description": self.exam_description,
            "clinical_indication": self.clinical_indication,
            "status": self.status.value,
            "priority": self.priority.value,
            "requested_date": self.requested_date.isoformat(),
            "scheduled_date": self.scheduled_date.isoformat() if self.scheduled_date else None,
            "collection_date": self.collection_date.isoformat() if self.collection_date else None,
            "result_date": self.result_date.isoformat() if self.result_date else None,
            "result_file": self.result_file,
            "result_notes": self.result_notes,
            "workflow_instance_id": str(self.workflow_instance_id) if self.workflow_instance_id else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
