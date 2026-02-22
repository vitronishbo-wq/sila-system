"""Medical Record Repository Implementation"""
from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from app.modules.saude_primaria.domain.models.medical_record import MedicalRecord
from app.modules.saude_primaria.application.ports.medical_record_repository_port import MedicalRecordRepositoryPort
from app.modules.saude_primaria.infrastructure.models.medical_record_model import MedicalRecordModel


class MedicalRecordRepository(MedicalRecordRepositoryPort):
    """Medical record repository implementation"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    def _to_domain(self, model: MedicalRecordModel) -> MedicalRecord:
        """Convert model to domain"""
        from app.modules.saude_primaria.domain.models.medical_record import VitalSigns
        
        vital_signs = None
        if model.vital_signs:
            vital_signs = VitalSigns(
                blood_pressure_systolic=model.vital_signs.get("blood_pressure_systolic"),
                blood_pressure_diastolic=model.vital_signs.get("blood_pressure_diastolic"),
                heart_rate=model.vital_signs.get("heart_rate"),
                respiratory_rate=model.vital_signs.get("respiratory_rate"),
                temperature=model.vital_signs.get("temperature"),
                oxygen_saturation=model.vital_signs.get("oxygen_saturation"),
                weight=model.vital_signs.get("weight"),
                height=model.vital_signs.get("height"),
                bmi=model.vital_signs.get("bmi")
            )
        
        prescription_ids = [UUID(pid) if isinstance(pid, str) else pid for pid in (model.prescription_ids or [])]
        exam_request_ids = [UUID(eid) if isinstance(eid, str) else eid for eid in (model.exam_request_ids or [])]
        
        return MedicalRecord(
            id=model.id,
            record_number=model.record_number,
            citizen_id=model.citizen_id,
            health_unit_id=model.health_unit_id,
            appointment_id=model.appointment_id,
            doctor_id=model.doctor_id,
            chief_complaint=model.chief_complaint,
            history_of_present_illness=model.history_of_present_illness,
            past_medical_history=model.past_medical_history,
            family_history=model.family_history,
            social_history=model.social_history,
            allergies=model.allergies or [],
            vital_signs=vital_signs,
            physical_exam=model.physical_exam,
            diagnosis=model.diagnosis or [],
            diagnosis_codes=model.diagnosis_codes or [],
            treatment_plan=model.treatment_plan,
            recommendations=model.recommendations,
            follow_up_date=model.follow_up_date,
            prescription_ids=prescription_ids,
            exam_request_ids=exam_request_ids,
            metadata=model.metadata_,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _to_model(self, record: MedicalRecord) -> MedicalRecordModel:
        """Convert domain to model"""
        vital_signs_dict = None
        if record.vital_signs:
            vital_signs_dict = {
                "blood_pressure_systolic": record.vital_signs.blood_pressure_systolic,
                "blood_pressure_diastolic": record.vital_signs.blood_pressure_diastolic,
                "heart_rate": record.vital_signs.heart_rate,
                "respiratory_rate": record.vital_signs.respiratory_rate,
                "temperature": record.vital_signs.temperature,
                "oxygen_saturation": record.vital_signs.oxygen_saturation,
                "weight": record.vital_signs.weight,
                "height": record.vital_signs.height,
                "bmi": record.vital_signs.bmi
            }
        
        return MedicalRecordModel(
            id=record.id,
            record_number=record.record_number,
            citizen_id=record.citizen_id,
            health_unit_id=record.health_unit_id,
            appointment_id=record.appointment_id,
            doctor_id=record.doctor_id,
            chief_complaint=record.chief_complaint,
            history_of_present_illness=record.history_of_present_illness,
            past_medical_history=record.past_medical_history,
            family_history=record.family_history,
            social_history=record.social_history,
            allergies=record.allergies,
            vital_signs=vital_signs_dict,
            physical_exam=record.physical_exam,
            diagnosis=record.diagnosis,
            diagnosis_codes=record.diagnosis_codes,
            treatment_plan=record.treatment_plan,
            recommendations=record.recommendations,
            follow_up_date=record.follow_up_date,
            prescription_ids=[str(pid) for pid in record.prescription_ids],
            exam_request_ids=[str(eid) for eid in record.exam_request_ids],
            metadata_=record.metadata,
            created_at=record.created_at,
            updated_at=record.updated_at
        )
    
    async def save(self, record: MedicalRecord) -> MedicalRecord:
        """Save medical record"""
        model = self._to_model(record)
        self.db.add(model)
        await self.db.flush()
        await self.db.refresh(model)
        return self._to_domain(model)
    
    async def get_by_id(self, record_id: UUID) -> Optional[MedicalRecord]:
        """Get medical record by ID"""
        stmt = select(MedicalRecordModel).where(MedicalRecordModel.id == record_id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def get_by_citizen(self, citizen_id: UUID, skip: int = 0, limit: int = 100) -> List[MedicalRecord]:
        """Get medical records by citizen"""
        stmt = select(MedicalRecordModel).where(MedicalRecordModel.citizen_id == citizen_id).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]
    
    async def get_by_appointment(self, appointment_id: UUID) -> Optional[MedicalRecord]:
        """Get medical record by appointment"""
        stmt = select(MedicalRecordModel).where(MedicalRecordModel.appointment_id == appointment_id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def get_by_doctor(self, doctor_id: UUID, skip: int = 0, limit: int = 100) -> List[MedicalRecord]:
        """Get medical records by doctor"""
        stmt = select(MedicalRecordModel).where(MedicalRecordModel.doctor_id == doctor_id).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]
    
    async def get_by_health_unit(self, health_unit_id: UUID, skip: int = 0, limit: int = 100) -> List[MedicalRecord]:
        """Get medical records by health unit"""
        stmt = select(MedicalRecordModel).where(MedicalRecordModel.health_unit_id == health_unit_id).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]
    
    async def search(self, filters: dict, skip: int = 0, limit: int = 100) -> tuple[List[MedicalRecord], int]:
        """Search medical records"""
        query = []
        
        if "citizen_id" in filters:
            query.append(MedicalRecordModel.citizen_id == filters["citizen_id"])
        if "doctor_id" in filters:
            query.append(MedicalRecordModel.doctor_id == filters["doctor_id"])
        if "health_unit_id" in filters:
            query.append(MedicalRecordModel.health_unit_id == filters["health_unit_id"])
        
        stmt = select(MedicalRecordModel)
        if query:
            stmt = stmt.where(and_(*query))
        
        count_stmt = select(func.count()).select_from(MedicalRecordModel)
        if query:
            count_stmt = count_stmt.where(and_(*query))
        count_result = await self.db.execute(count_stmt)
        total = count_result.scalar()
        
        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        records = [self._to_domain(m) for m in result.scalars().all()]
        
        return records, total
    
    async def update(self, record: MedicalRecord) -> MedicalRecord:
        """Update medical record"""
        stmt = select(MedicalRecordModel).where(MedicalRecordModel.id == record.id)
        result = await self.db.execute(stmt)
        model = result.scalar_one()
        
        model.diagnosis = record.diagnosis
        model.diagnosis_codes = record.diagnosis_codes
        model.treatment_plan = record.treatment_plan
        model.metadata_ = record.metadata
        model.updated_at = record.updated_at
        model.prescription_ids = [str(pid) for pid in record.prescription_ids]
        model.exam_request_ids = [str(eid) for eid in record.exam_request_ids]
        
        if record.vital_signs:
            model.vital_signs = {
                "blood_pressure_systolic": record.vital_signs.blood_pressure_systolic,
                "blood_pressure_diastolic": record.vital_signs.blood_pressure_diastolic,
                "heart_rate": record.vital_signs.heart_rate,
                "respiratory_rate": record.vital_signs.respiratory_rate,
                "temperature": record.vital_signs.temperature,
                "oxygen_saturation": record.vital_signs.oxygen_saturation,
                "weight": record.vital_signs.weight,
                "height": record.vital_signs.height,
                "bmi": record.vital_signs.bmi
            }
        
        await self.db.flush()
        await self.db.refresh(model)
        return self._to_domain(model)
