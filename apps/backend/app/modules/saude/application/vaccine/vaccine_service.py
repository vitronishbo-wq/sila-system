from __future__ import annotations

from datetime import date
from uuid import UUID

from apps.backend.app.core.observability import trace
from apps.backend.app.modules.saude.application.ports import (
    JuventudeServicePort,
    WorkflowServicePort,
)
from apps.backend.app.modules.saude.domain.entities.vaccine import VaccineDose


class VaccineService:
    """Application service for vaccine management."""

    def __init__(
        self,
        juventude_service: JuventudeServicePort | None = None,
        workflow_service: WorkflowServicePort | None = None,
    ) -> None:
        self.juventude_service = juventude_service
        self.workflow_service = workflow_service

    @trace()
    async def register_vaccine_dose(
        self,
        citizen_id: UUID,
        vaccine_id: UUID,
        health_unit_id: UUID,
        applied_by: UUID,
        dose_number: int,
        batch_number: str,
        application_date: date,
        next_dose_date: date | None = None,
        adverse_reactions: str | None = None,
        vaccine_name: str | None = None,
        dose_label: str | None = None,
    ) -> VaccineDose:
        """Register vaccine dose."""
        dose = VaccineDose(
            citizen_id=citizen_id,
            vaccine_id=vaccine_id,
            health_unit_id=health_unit_id,
            applied_by=applied_by,
            dose_number=dose_number,
            batch_number=batch_number,
            application_date=application_date,
            next_dose_date=next_dose_date,
            adverse_reactions=adverse_reactions,
        )
        dose.metadata["integracoes"] = {"juventude": False}
        if self.juventude_service:
            jovem = await self.juventude_service.get_jovem_profile(citizen_id)
            if jovem:
                nome = vaccine_name or str(vaccine_id)
                dose_desc = dose_label or f"{dose_number}a dose"
                await self.juventude_service.atualizar_carteira_vacinacao(
                    citizen_id=citizen_id,
                    vacinas=[
                        {
                            "nome": nome,
                            "dose": dose_desc,
                            "data": application_date.isoformat(),
                            "lote": batch_number,
                        }
                    ],
                )
                dose.metadata["integracoes"]["juventude"] = True
                if dose_number >= 2:
                    meta = f"VACINACAO_{nome.upper().replace(' ', '_')}_COMPLETA"
                    await self.juventude_service.registrar_meta_saude_alcancada(
                        citizen_id=citizen_id, meta=meta, data_referencia=application_date
                    )
        if self.workflow_service:
            await self.workflow_service.abrir_fluxo(
                tipo_fluxo="vacinacao",
                entity_id=dose.id,
                actor_id=applied_by,
                health_unit_id=health_unit_id,
                citizen_id=citizen_id,
                detalhes={"reason": f"Aplicacao de vacina {vaccine_name or vaccine_id}"},
            )
        return dose

    def schedule_next_dose(self, dose: VaccineDose, next_date: date) -> VaccineDose:
        """Schedule next vaccine dose."""
        dose.schedule_next_dose(next_date)
        return dose

    def record_adverse_reaction(self, dose: VaccineDose, reaction: str) -> VaccineDose:
        """Record adverse reaction."""
        dose.record_reaction(reaction)
        return dose
