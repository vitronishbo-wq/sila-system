"""Medical Record Domain Model."""
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from uuid import UUID, uuid4


@dataclass
class VitalSigns:
    """Sinais vitais."""

    blood_pressure_systolic: Optional[int] = None
    blood_pressure_diastolic: Optional[int] = None
    heart_rate: Optional[int] = None
    respiratory_rate: Optional[int] = None
    temperature: Optional[float] = None
    oxygen_saturation: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    bmi: Optional[float] = None

    def calculate_bmi(self) -> None:
        """Calcula IMC."""
        if self.weight and self.height and (self.height > 0):
            self.bmi = round(self.weight / (self.height / 100) ** 2, 2)

    def to_dict(self) -> dict:
        return {
            "blood_pressure": (
                f"{self.blood_pressure_systolic}/{self.blood_pressure_diastolic}"
                if self.blood_pressure_systolic
                else None
            ),
            "heart_rate": self.heart_rate,
            "respiratory_rate": self.respiratory_rate,
            "temperature": self.temperature,
            "oxygen_saturation": self.oxygen_saturation,
            "weight": self.weight,
            "height": self.height,
            "bmi": self.bmi,
        }


@dataclass
class MedicalRecord:
    """Registro medico - Aggregate Root."""

    id: UUID = field(default_factory=uuid4)
    record_number: Optional[str] = None
    citizen_id: UUID = field(default_factory=uuid4)
    health_unit_id: UUID = field(default_factory=uuid4)
    appointment_id: Optional[UUID] = None
    doctor_id: UUID = field(default_factory=uuid4)
    chief_complaint: str = ""
    history_of_present_illness: Optional[str] = None
    past_medical_history: Optional[str] = None
    family_history: Optional[str] = None
    social_history: Optional[str] = None
    allergies: List[str] = field(default_factory=list)
    vital_signs: Optional[VitalSigns] = None
    physical_exam: Optional[str] = None
    diagnosis: List[str] = field(default_factory=list)
    diagnosis_codes: List[str] = field(default_factory=list)
    treatment_plan: Optional[str] = None
    recommendations: Optional[str] = None
    follow_up_date: Optional[date] = None
    prescription_ids: List[UUID] = field(default_factory=list)
    exam_request_ids: List[UUID] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        if not self.chief_complaint or len(self.chief_complaint.strip()) < 5:
            raise ValueError("Queixa principal deve ter pelo menos 5 caracteres")

    def add_diagnosis(self, diagnosis: str, code: Optional[str] = None) -> None:
        """Adiciona diagnostico."""
        if diagnosis not in self.diagnosis:
            self.diagnosis.append(diagnosis)
            if code and code not in self.diagnosis_codes:
                self.diagnosis_codes.append(code)
            self.updated_at = datetime.now()

    def add_prescription(self, prescription_id: UUID) -> None:
        """Adiciona referencia de prescricao."""
        if prescription_id not in self.prescription_ids:
            self.prescription_ids.append(prescription_id)
            self.updated_at = datetime.now()

    def add_exam_request(self, exam_request_id: UUID) -> None:
        """Adiciona referencia de pedido de exame."""
        if exam_request_id not in self.exam_request_ids:
            self.exam_request_ids.append(exam_request_id)
            self.updated_at = datetime.now()

    def update_vitals(self, vitals: VitalSigns) -> None:
        """Atualiza sinais vitais."""
        self.vital_signs = vitals
        self.vital_signs.calculate_bmi()
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "record_number": self.record_number,
            "citizen_id": str(self.citizen_id),
            "health_unit_id": str(self.health_unit_id),
            "appointment_id": str(self.appointment_id) if self.appointment_id else None,
            "doctor_id": str(self.doctor_id),
            "chief_complaint": self.chief_complaint,
            "history_of_present_illness": self.history_of_present_illness,
            "past_medical_history": self.past_medical_history,
            "family_history": self.family_history,
            "social_history": self.social_history,
            "allergies": self.allergies,
            "vital_signs": self.vital_signs.to_dict() if self.vital_signs else None,
            "physical_exam": self.physical_exam,
            "diagnosis": self.diagnosis,
            "diagnosis_codes": self.diagnosis_codes,
            "treatment_plan": self.treatment_plan,
            "recommendations": self.recommendations,
            "follow_up_date": (
                self.follow_up_date.isoformat() if self.follow_up_date else None
            ),
            "prescription_ids": [str(pid) for pid in self.prescription_ids],
            "exam_request_ids": [str(eid) for eid in self.exam_request_ids],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
