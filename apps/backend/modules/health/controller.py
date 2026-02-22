from datetime import datetime
from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.session import get_async_db as get_session
from core.security import get_current_user_id
from modules.common.schemas.api_responses import PingResponse

# Import Health module schemas
from modules.health.schemas.api_schemas import (
    AppointmentCreate,
    AppointmentResponse,
    CancelAppointmentResponse,
    HealthRecordCreate,
    HealthRecordResponse,
    HealthRecordsListResponse,
    HealthRecordUpdate,
    HealthServicesResponse,
    MedicalRecordResponse,
    UserAppointmentsResponse,
)

from modules.health.service import HealthService

router = APIRouter()

@router.get("/ping", response_model=PingResponse, tags=["Health"])
async def ping():
    return PingResponse(message="pong", timestamp=datetime.utcnow())

@router.post("/", response_model=HealthRecordResponse, status_code=status.HTTP_201_CREATED, tags=["Health"])
async def create_health_record(
    payload: HealthRecordCreate,
    db: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
) -> HealthRecordResponse:
    service = HealthService(db)
    return await service.create_health_record(UUID(current_user_id), payload)

@router.get("/", response_model=HealthRecordsListResponse, tags=["Health"])
async def list_health_records(
    db: AsyncSession = Depends(get_session),
) -> HealthRecordsListResponse:
    service = HealthService(db)
    return await service.list_health_records()

@router.get("/appointments/user", response_model=UserAppointmentsResponse, tags=["Health"])
async def get_user_appointments(
    status_filter: Optional[str] = None,
    db: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
) -> UserAppointmentsResponse:
    service = HealthService(db)
    return await service.list_user_appointments(
        user_id=UUID(current_user_id), status_filter=status_filter
    )

@router.patch("/appointments/{appointment_id}/cancel", response_model=CancelAppointmentResponse, tags=["Health"])
async def cancel_appointment(
    appointment_id: UUID,
    db: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
) -> CancelAppointmentResponse:
    service = HealthService(db)
    try:
        result = await service.cancel_appointment(UUID(current_user_id), str(appointment_id))
        if not result:
            raise HTTPException(status_code=404, detail="Agendamento não encontrado")
        return result
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))