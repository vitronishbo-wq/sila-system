from typing import List, Optional, Dict, Any, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from datetime import datetime

from app.core.services.base_request_service import BaseRequestService
from app.modules.saude_primaria.infrastructure.db.healthcare_model import (
    HealthcareRequestModel, 
    MaternalRecordModel,
    PostNatalRecordModel,
    ChronicMonitoringModel,
    NutritionRecordModel,
    PsychologySessionModel,
    HealthAlertModel
)
from app.modules.saude_primaria.infrastructure.repositories.healthcare_repository import HealthcareRepository
from app.modules.saude_primaria.application.schemas import (
    HealthcareRequestCreate, 
    HealthcareRequestResponse, 
    HealthcareScheduleUpdate, 
    HealthcareStatusUpdate,
    HealthcareCancelRequest
)
from app.modules.saude_primaria.domain.enums import AppointmentStatus, HealthcareServiceType

class HealthcareService(BaseRequestService[HealthcareRequestModel, HealthcareRepository]):
    """Serviço de saúde primária assíncrono seguindo o padrão BaseRequestService."""
    
    def __init__(self, db: AsyncSession, **kwargs):
        super().__init__(
            db=db,
            repository=HealthcareRepository(db),
            audit_enabled=True,
            **kwargs
        )

    # ========== Abstract Methods ==========
    def get_repository(self) -> HealthcareRepository:
        return HealthcareRepository(self.db)

    def default_status(self) -> str:
        return AppointmentStatus.PENDING.value

    async def create_request_model(
        self,
        citizen_id: UUID,
        request_data: Dict[str, Any],
        **kwargs
    ) -> HealthcareRequestModel:
        """Instancia o model HealthcareRequestModel."""
        # Note: request_data here is expected to be the 'data' from creates
        data = request_data.get("data_obj") # Passamos o objeto Pydantic ou dict no create_request wrapper
        
        db_request = HealthcareRequestModel(
            citizen_id=citizen_id,
            service_type=data.service_type,
            preferred_date=data.preferred_date,
            health_unit_id=data.health_unit_id,
            clinical_notes=data.symptoms, 
            metadata_json=data.metadata 
        )
        
        # Mapeamento de registos especializados
        if data.maternal_record:
            db_request.maternal_record = MaternalRecordModel(**data.maternal_record.model_dump(exclude_unset=True))
        if data.post_natal_record:
            db_request.post_natal_record = PostNatalRecordModel(**data.post_natal_record.model_dump(exclude_unset=True))
        if data.chronic_monitoring:
            db_request.chronic_monitoring = ChronicMonitoringModel(**data.chronic_monitoring.model_dump(exclude_unset=True))
        if data.nutrition_record:
            db_request.nutrition_record = NutritionRecordModel(**data.nutrition_record.model_dump(exclude_unset=True))
        if data.psychology_session:
            db_request.psychology_session = PsychologySessionModel(**data.psychology_session.model_dump(exclude_unset=True))
        if data.health_alert:
            db_request.health_alert = HealthAlertModel(**data.health_alert.model_dump(exclude_unset=True))
            
        return db_request

    async def get_user_from_citizen_id(self, citizen_id: UUID) -> Optional[UUID]:
        return citizen_id

    # ========== Template Overrides ==========
    async def _validate_create_request(self, citizen_id: UUID, request_data: Dict[str, Any], **kwargs) -> None:
        data = request_data.get("data_obj")
        if data.preferred_date and data.preferred_date < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="A data preferencial não pode ser no passado."
            )

    # ========== Legacy/Wrapper Methods ==========
    async def create_request(self, citizen_id: UUID, data: HealthcareRequestCreate) -> HealthcareRequestResponse:
        """Wrapper para o método de template da base."""
        # Usamos o BaseRequestService.create_request
        saved = await super().create_request(
            citizen_id=citizen_id,
            created_by=citizen_id, # Assumindo que o cidadão cria para si
            request_data={"data_obj": data}
        )
        # Expor metadata para o Response schema
        setattr(saved, "metadata", getattr(saved, "metadata_json", None))
        return HealthcareRequestResponse.model_validate(saved)

    async def get_citizen_requests(self, citizen_id: UUID) -> List[HealthcareRequestResponse]:
        """Recuperação via repositório."""
        requests, _ = await self.list_requests(citizen_id=citizen_id)
        return [HealthcareRequestResponse.model_validate(req) for req in requests]

    async def schedule_request(self, request_id: UUID, schedule_data: HealthcareScheduleUpdate, professional_id: UUID) -> HealthcareRequestResponse:
        """Transição de estado para Agendado."""
        db_request = await self.repo.get_by_id(request_id)
        if not db_request:
            raise HTTPException(status_code=404, detail="Pedido não localizado.")
        
        old_status = str(db_request.status)
        db_request.status = AppointmentStatus.SCHEDULED
        db_request.scheduled_date = schedule_data.scheduled_date
        db_request.health_unit_id = schedule_data.health_unit_id
        db_request.clinical_notes = (db_request.clinical_notes or "") + f"\n[AGENDA - {professional_id}]: {datetime.now()}"

        saved = await self.repo.save(db_request)
        await self._post_status_change(saved, old_status, str(saved.status), professional_id)
        
        return HealthcareRequestResponse.model_validate(saved)

    async def update_status(self, request_id: UUID, status_data: HealthcareStatusUpdate, professional_id: UUID) -> HealthcareRequestResponse:
        """Gestão de estados do ciclo de vida clínico."""
        db_request = await self.repo.get_by_id(request_id)
        if not db_request:
            raise HTTPException(status_code=404, detail="Pedido não localizado.")

        old_status = str(db_request.status)
        db_request.status = status_data.status
        if status_data.clinical_notes:
            db_request.clinical_notes = (db_request.clinical_notes or "") + f"\n[STATUS_CHANGE - {professional_id}]: {status_data.clinical_notes}"
        
        saved = await self.repo.save(db_request)
        await self._post_status_change(saved, old_status, str(saved.status), professional_id)
        
        return HealthcareRequestResponse.model_validate(saved)

    async def cancel_request(self, request_id: UUID, cancel_data: HealthcareCancelRequest, performer_id: UUID) -> HealthcareRequestResponse:
        """Cancelamento com motivo obrigatório."""
        db_request = await self.repo.get_by_id(request_id)
        if not db_request:
            raise HTTPException(status_code=404, detail="Pedido não localizado.")
        
        old_status = str(db_request.status)
        db_request.status = AppointmentStatus.CANCELLED
        db_request.clinical_notes = (db_request.clinical_notes or "") + f"\n[CANCELADO POR {performer_id}]: {cancel_data.reason}"
        
        saved = await self.repo.save(db_request)
        await self._post_status_change(saved, old_status, str(saved.status), performer_id)
        
        return HealthcareRequestResponse.model_validate(saved)

    def get_services_catalog(self) -> List[Dict[str, str]]:
        """Mapeamento de Enums para catálogo."""
        return [
            {"code": s.value, "label": s.name.replace("_", " ").title()} 
            for s in HealthcareServiceType
        ]