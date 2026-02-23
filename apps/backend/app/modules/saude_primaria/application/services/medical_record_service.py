from app.core.observability import trace
"""Medical Record Service"""
from typing import Optional, List
from uuid import UUID

from app.modules.saude_primaria.domain.models.medical_record import MedicalRecord, VitalSigns
from app.modules.saude_primaria.application.ports.medical_record_repository_port import MedicalRecordRepositoryPort


class MedicalRecordService:
    """Application service for medical record management"""
    
    def __init__(self, repository: MedicalRecordRepositoryPort):
        self.repository = repository
    
    @trace()
    async def create_medical_record(
        self,
        citizen_id: UUID,
        doctor_id: UUID,
        health_unit_id: UUID,
        chief_complaint: str,
        appointment_id: Optional[UUID] = None,
        history_of_present_illness: Optional[str] = None,
        past_medical_history: Optional[str] = None,
        family_history: Optional[str] = None,
        social_history: Optional[str] = None,
        allergies: Optional[List[str]] = None,
        physical_exam: Optional[str] = None,
        treatment_plan: Optional[str] = None,
        recommendations: Optional[str] = None
    ) -> MedicalRecord:
        """Create new medical record"""
        record = MedicalRecord(
            citizen_id=citizen_id,
            doctor_id=doctor_id,
            health_unit_id=health_unit_id,
            chief_complaint=chief_complaint,
            appointment_id=appointment_id,
            history_of_present_illness=history_of_present_illness,
            past_medical_history=past_medical_history,
            family_history=family_history,
            social_history=social_history,
            allergies=allergies or [],
            physical_exam=physical_exam,
            treatment_plan=treatment_plan,
            recommendations=recommendations
        )
        
        return await self.repository.save(record)
    
    @trace()
    async def get_medical_record(self, record_id: UUID) -> Optional[MedicalRecord]:
        """Get medical record by ID"""
        return await self.repository.get_by_id(record_id)
    
    @trace()
    async def list_citizen_records(self, citizen_id: UUID, skip: int = 0, limit: int = 100) -> List[MedicalRecord]:
        """List citizen medical records"""
        return await self.repository.get_by_citizen(citizen_id, skip, limit)
    
    @trace()
    async def update_vital_signs(self, record_id: UUID, vitals: VitalSigns) -> MedicalRecord:
        """Update vital signs"""
        record = await self.repository.get_by_id(record_id)
        if not record:
            raise ValueError(f"Medical record {record_id} not found")
        
        record.update_vitals(vitals)
        return await self.repository.update(record)
    
    @trace()
    async def add_diagnosis(self, record_id: UUID, diagnosis: str, code: Optional[str] = None) -> MedicalRecord:
        """Add diagnosis to record"""
        record = await self.repository.get_by_id(record_id)
        if not record:
            raise ValueError(f"Medical record {record_id} not found")
        
        record.add_diagnosis(diagnosis, code)
        return await self.repository.update(record)
    
    @trace()
    async def add_prescription(self, record_id: UUID, prescription_id: UUID) -> MedicalRecord:
        """Add prescription reference"""
        record = await self.repository.get_by_id(record_id)
        if not record:
            raise ValueError(f"Medical record {record_id} not found")
        
        record.add_prescription(prescription_id)
        return await self.repository.update(record)
    
    @trace()
    async def add_exam_request(self, record_id: UUID, exam_request_id: UUID) -> MedicalRecord:
        """Add exam request reference"""
        record = await self.repository.get_by_id(record_id)
        if not record:
            raise ValueError(f"Medical record {record_id} not found")
        
        record.add_exam_request(exam_request_id)
        return await self.repository.update(record)
    
    @trace()
    async def search_records(self, filters: dict, skip: int = 0, limit: int = 100) -> tuple[List[MedicalRecord], int]:
        """Search medical records"""
        return await self.repository.search(filters, skip, limit)
