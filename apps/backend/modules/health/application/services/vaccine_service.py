"""Vaccine Service"""
from typing import Optional, List
from uuid import UUID
from datetime import date

from app.modules.saude_primaria.domain.models.vaccine import Vaccine, VaccineDose
from app.modules.saude_primaria.domain.enums import VaccineStatus


class VaccineService:
    """Application service for vaccine management"""
    
    async def register_vaccine_dose(
        self,
        citizen_id: UUID,
        vaccine_id: UUID,
        health_unit_id: UUID,
        applied_by: UUID,
        dose_number: int,
        batch_number: str,
        application_date: date,
        next_dose_date: Optional[date] = None,
        adverse_reactions: Optional[str] = None
    ) -> VaccineDose:
        """Register vaccine dose"""
        dose = VaccineDose(
            citizen_id=citizen_id,
            vaccine_id=vaccine_id,
            health_unit_id=health_unit_id,
            applied_by=applied_by,
            dose_number=dose_number,
            batch_number=batch_number,
            application_date=application_date,
            next_dose_date=next_dose_date,
            adverse_reactions=adverse_reactions
        )
        
        return dose
    
    def schedule_next_dose(self, dose: VaccineDose, next_date: date) -> VaccineDose:
        """Schedule next vaccine dose"""
        dose.schedule_next_dose(next_date)
        return dose
    
    def record_adverse_reaction(self, dose: VaccineDose, reaction: str) -> VaccineDose:
        """Record adverse reaction"""
        dose.record_reaction(reaction)
        return dose
