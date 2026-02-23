from app.core.observability import trace
"""Prescription Service"""
from typing import Optional, List
from uuid import UUID

from app.modules.saude_primaria.domain.models.prescription import Prescription, PrescriptionItem
from app.modules.saude_primaria.domain.enums import MedicationType
from app.modules.saude_primaria.application.ports.prescription_repository_port import PrescriptionRepositoryPort


class PrescriptionService:
    """Application service for prescription management"""
    
    def __init__(self, repository: PrescriptionRepositoryPort):
        self.repository = repository
    
    @trace()
    async def create_prescription(
        self,
        citizen_id: UUID,
        doctor_id: UUID,
        health_unit_id: UUID,
        items: List[dict],
        appointment_id: Optional[UUID] = None,
        clinical_notes: Optional[str] = None,
        recommendations: Optional[str] = None
    ) -> Prescription:
        """Create new prescription"""
        prescription_items = []
        for item in items:
            prescription_items.append(
                PrescriptionItem(
                    medication_code=item["medication_code"],
                    medication_name=item["medication_name"],
                    dosage=item["dosage"],
                    frequency=item["frequency"],
                    duration_days=item["duration_days"],
                    quantity=item["quantity"],
                    unit=item["unit"],
                    notes=item.get("notes"),
                    medication_type=MedicationType(item.get("medication_type", "USO_OCASIONAL"))
                )
            )
        
        prescription = Prescription(
            citizen_id=citizen_id,
            doctor_id=doctor_id,
            health_unit_id=health_unit_id,
            appointment_id=appointment_id,
            items=prescription_items,
            clinical_notes=clinical_notes,
            recommendations=recommendations
        )
        
        return await self.repository.save(prescription)
    
    @trace()
    async def get_prescription(self, prescription_id: UUID) -> Optional[Prescription]:
        """Get prescription by ID"""
        return await self.repository.get_by_id(prescription_id)
    
    @trace()
    async def list_citizen_prescriptions(self, citizen_id: UUID, skip: int = 0, limit: int = 100) -> List[Prescription]:
        """List citizen prescriptions"""
        return await self.repository.get_by_citizen(citizen_id, skip, limit)
    
    @trace()
    async def get_active_prescriptions(self, citizen_id: UUID) -> List[Prescription]:
        """Get active prescriptions for citizen"""
        return await self.repository.get_active_by_citizen(citizen_id)
    
    @trace()
    async def dispense_prescription(self, prescription_id: UUID, items_dispensed: Optional[List[str]] = None) -> Prescription:
        """Dispense prescription"""
        prescription = await self.repository.get_by_id(prescription_id)
        if not prescription:
            raise ValueError(f"Prescription {prescription_id} not found")
        
        prescription.dispense(items_dispensed)
        return await self.repository.update(prescription)
    
    @trace()
    async def cancel_prescription(self, prescription_id: UUID, reason: str, cancelled_by: UUID) -> Prescription:
        """Cancel prescription"""
        prescription = await self.repository.get_by_id(prescription_id)
        if not prescription:
            raise ValueError(f"Prescription {prescription_id} not found")
        
        prescription.cancel(reason, cancelled_by)
        return await self.repository.update(prescription)
    
    @trace()
    async def check_expired_prescriptions(self) -> List[Prescription]:
        """Check for expired prescriptions"""
        return await self.repository.get_expired()
    
    @trace()
    async def search_prescriptions(self, filters: dict, skip: int = 0, limit: int = 100) -> tuple[List[Prescription], int]:
        """Search prescriptions"""
        return await self.repository.search(filters, skip, limit)
