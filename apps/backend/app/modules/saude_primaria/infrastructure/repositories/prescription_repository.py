"""Prescription Repository Implementation"""
from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from datetime import date

from app.modules.saude_primaria.domain.models.prescription import Prescription
from app.modules.saude_primaria.application.ports.prescription_repository_port import PrescriptionRepositoryPort
from app.modules.saude_primaria.infrastructure.models.prescription_model import PrescriptionModel
from app.modules.saude_primaria.domain.enums import PrescriptionStatus


class PrescriptionRepository(PrescriptionRepositoryPort):
    """Prescription repository implementation"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    def _to_domain(self, model: PrescriptionModel) -> Prescription:
        """Convert model to domain"""
        from app.modules.saude_primaria.domain.models.prescription import PrescriptionItem
        from app.modules.saude_primaria.domain.enums import MedicationType
        
        items = []
        for item_dict in (model.items or []):
            items.append(
                PrescriptionItem(
                    medication_code=item_dict["medication_code"],
                    medication_name=item_dict["medication_name"],
                    dosage=item_dict["dosage"],
                    frequency=item_dict["frequency"],
                    duration_days=item_dict["duration_days"],
                    quantity=item_dict["quantity"],
                    unit=item_dict["unit"],
                    notes=item_dict.get("notes"),
                    medication_type=MedicationType(item_dict.get("medication_type", "USO_OCASIONAL"))
                )
            )
        
        return Prescription(
            id=model.id,
            prescription_number=model.prescription_number,
            citizen_id=model.citizen_id,
            doctor_id=model.doctor_id,
            appointment_id=model.appointment_id,
            health_unit_id=model.health_unit_id,
            items=items,
            clinical_notes=model.clinical_notes,
            recommendations=model.recommendations,
            issue_date=model.issue_date,
            expiry_date=model.expiry_date,
            status=PrescriptionStatus(model.status),
            workflow_instance_id=model.workflow_instance_id,
            metadata=model.metadata_,
            created_at=model.created_at,
            updated_at=model.updated_at,
            dispensed_at=model.dispensed_at
        )
    
    def _to_model(self, prescription: Prescription) -> PrescriptionModel:
        """Convert domain to model"""
        items_dict = [
            {
                "medication_code": item.medication_code,
                "medication_name": item.medication_name,
                "dosage": item.dosage,
                "frequency": item.frequency,
                "duration_days": item.duration_days,
                "quantity": item.quantity,
                "unit": item.unit,
                "notes": item.notes,
                "medication_type": item.medication_type.value
            }
            for item in prescription.items
        ]
        
        return PrescriptionModel(
            id=prescription.id,
            prescription_number=prescription.prescription_number,
            citizen_id=prescription.citizen_id,
            doctor_id=prescription.doctor_id,
            appointment_id=prescription.appointment_id,
            health_unit_id=prescription.health_unit_id,
            items=items_dict,
            clinical_notes=prescription.clinical_notes,
            recommendations=prescription.recommendations,
            issue_date=prescription.issue_date,
            expiry_date=prescription.expiry_date,
            status=prescription.status.value,
            workflow_instance_id=prescription.workflow_instance_id,
            metadata_=prescription.metadata,
            created_at=prescription.created_at,
            updated_at=prescription.updated_at,
            dispensed_at=prescription.dispensed_at
        )
    
    async def save(self, prescription: Prescription) -> Prescription:
        """Save prescription"""
        model = self._to_model(prescription)
        self.db.add(model)
        await self.db.flush()
        await self.db.refresh(model)
        return self._to_domain(model)
    
    async def get_by_id(self, prescription_id: UUID) -> Optional[Prescription]:
        """Get prescription by ID"""
        stmt = select(PrescriptionModel).where(PrescriptionModel.id == prescription_id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def get_by_citizen(self, citizen_id: UUID, skip: int = 0, limit: int = 100) -> List[Prescription]:
        """Get prescriptions by citizen"""
        stmt = select(PrescriptionModel).where(PrescriptionModel.citizen_id == citizen_id).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]
    
    async def get_by_doctor(self, doctor_id: UUID, skip: int = 0, limit: int = 100) -> List[Prescription]:
        """Get prescriptions by doctor"""
        stmt = select(PrescriptionModel).where(PrescriptionModel.doctor_id == doctor_id).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]
    
    async def get_active_by_citizen(self, citizen_id: UUID) -> List[Prescription]:
        """Get active prescriptions for citizen"""
        stmt = select(PrescriptionModel).where(
            and_(
                PrescriptionModel.citizen_id == citizen_id,
                PrescriptionModel.status == PrescriptionStatus.ACTIVE.value
            )
        )
        result = await self.db.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]
    
    async def get_by_appointment(self, appointment_id: UUID) -> List[Prescription]:
        """Get prescriptions by appointment"""
        stmt = select(PrescriptionModel).where(PrescriptionModel.appointment_id == appointment_id)
        result = await self.db.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]
    
    async def get_expired(self) -> List[Prescription]:
        """Get expired prescriptions"""
        today = date.today()
        stmt = select(PrescriptionModel).where(
            and_(
                PrescriptionModel.expiry_date < today,
                PrescriptionModel.status != PrescriptionStatus.CANCELLED.value
            )
        )
        result = await self.db.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]
    
    async def search(self, filters: dict, skip: int = 0, limit: int = 100) -> tuple[List[Prescription], int]:
        """Search prescriptions"""
        query = []
        
        if "citizen_id" in filters:
            query.append(PrescriptionModel.citizen_id == filters["citizen_id"])
        if "doctor_id" in filters:
            query.append(PrescriptionModel.doctor_id == filters["doctor_id"])
        if "status" in filters:
            query.append(PrescriptionModel.status == filters["status"])
        
        stmt = select(PrescriptionModel)
        if query:
            stmt = stmt.where(and_(*query))
        
        count_stmt = select(func.count()).select_from(PrescriptionModel)
        if query:
            count_stmt = count_stmt.where(and_(*query))
        count_result = await self.db.execute(count_stmt)
        total = count_result.scalar()
        
        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        prescriptions = [self._to_domain(m) for m in result.scalars().all()]
        
        return prescriptions, total
    
    async def update(self, prescription: Prescription) -> Prescription:
        """Update prescription"""
        stmt = select(PrescriptionModel).where(PrescriptionModel.id == prescription.id)
        result = await self.db.execute(stmt)
        model = result.scalar_one()
        
        model.status = prescription.status.value
        model.metadata_ = prescription.metadata
        model.updated_at = prescription.updated_at
        model.dispensed_at = prescription.dispensed_at
        
        await self.db.flush()
        await self.db.refresh(model)
        return self._to_domain(model)
    
    async def delete(self, prescription_id: UUID) -> bool:
        """Delete prescription"""
        stmt = select(PrescriptionModel).where(PrescriptionModel.id == prescription_id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model:
            await self.db.delete(model)
            await self.db.flush()
            return True
        return False
