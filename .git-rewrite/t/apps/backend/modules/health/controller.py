"""
Health module controller - FastAPI routes with full type safety.

This controller follows the OpenAPI contract and uses Pydantic schemas for validation.
All endpoints are properly typed with response_model for automatic Swagger documentation.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.session import get_async_db as get_session
from core.security import get_current_user_id

# Import API response schemas
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

# Import Health service
from modules.health.service import HealthService

# Create router
router = APIRouter()


# ============================================================================
# Health Ping
# ============================================================================


@router.get(
    "/ping",
    response_model=PingResponse,
    summary="Ping",
    description="Health check do módulo health.",
    tags=["Health"],
)
async def ping():
    """Health check do módulo health."""
    return PingResponse(message="pong", timestamp=datetime.utcnow())


# ============================================================================
# Health Records CRUD
# ============================================================================


@router.post(
    "/",
    response_model=HealthRecordResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Health Record",
    description="Cria um novo registro de saúde.",
    tags=["Health"],
)
async def create_health_record(
    payload: HealthRecordCreate,
    db: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
) -> HealthRecordResponse:
    """
    Cria um novo registro de saúde.

    Args:
        payload: Dados do registro de saúde
        db: Sessão do banco de dados
        current_user_id: ID do usuário autenticado

    Returns:
        HealthRecordResponse: Registro criado
    """
    from uuid import UUID

    service = HealthService(db)
    return await service.create_health_record(UUID(current_user_id), payload)


@router.get(
    "/",
    response_model=HealthRecordsListResponse,
    summary="List Health Records",
    description="Lista todos os registros de saúde.",
    tags=["Health"],
)
async def list_health_records(
    db: AsyncSession = Depends(get_session),
) -> HealthRecordsListResponse:
    """
    Lista todos os registros de saúde.

    Args:
        db: Sessão do banco de dados

    Returns:
        HealthRecordsListResponse: Lista de registros
    """
    service = HealthService(db)
    return await service.list_health_records()


@router.get(
    "/{record_id}",
    response_model=HealthRecordResponse,
    summary="Get Health Record",
    description="Busca um registro de saúde específico.",
    tags=["Health"],
)
async def get_health_record(
    record_id: UUID,
    db: AsyncSession = Depends(get_session),
) -> HealthRecordResponse:
    """
    Busca um registro de saúde específico.

    Args:
        record_id: ID do registro
        db: Sessão do banco de dados

    Returns:
        HealthRecordResponse: Registro encontrado

    Raises:
        HTTPException: Se o registro não for encontrado
    """
    service = HealthService(db)
    record = await service.get_health_record(record_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Health record not found"
        )
    return record


@router.put(
    "/{record_id}",
    response_model=HealthRecordResponse,
    summary="Update Health Record",
    description="Atualiza um registro de saúde.",
    tags=["Health"],
)
async def update_health_record(
    record_id: UUID,
    payload: HealthRecordUpdate,
    db: AsyncSession = Depends(get_session),
) -> HealthRecordResponse:
    """
    Atualiza um registro de saúde.

    Args:
        record_id: ID do registro
        payload: Dados para atualização
        db: Sessão do banco de dados

    Returns:
        HealthRecordResponse: Registro atualizado

    Raises:
        HTTPException: Se o registro não for encontrado
    """
    service = HealthService(db)
    record = await service.update_health_record(record_id, payload)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Health record not found"
        )
    return record


@router.delete(
    "/{record_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Health Record",
    description="Deleta um registro de saúde.",
    tags=["Health"],
)
async def delete_health_record(
    record_id: UUID,
    db: AsyncSession = Depends(get_session),
):
    """
    Deleta um registro de saúde.

    Args:
        record_id: ID do registro
        db: Sessão do banco de dados

    Raises:
        HTTPException: Se o registro não for encontrado
    """
    service = HealthService(db)
    deleted = await service.delete_health_record(record_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Health record not found"
        )


# ============================================================================
# Health Services
# ============================================================================


@router.get(
    "/services",
    response_model=HealthServicesResponse,
    summary="Get Health Services",
    description="Retorna lista de serviços médicos disponíveis.\n\nArgs:\n    category: Filtrar por categoria específica\n    status_filter: Filtrar por status de disponibilidade\n\nRequer autenticação JWT.",
    tags=["Health"],
)
async def get_health_services(
    category: Optional[str] = None,
    status_filter: Optional[str] = None,
    db: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
) -> HealthServicesResponse:
    """
    Retorna lista de serviços médicos disponíveis.

    Args:
        category: Filtrar por categoria específica
        status_filter: Filtrar por status de disponibilidade
        db: Sessão do banco de dados
        current_user_id: ID do usuário autenticado

    Returns:
        HealthServicesResponse: Lista de serviços médicos
    """
    service = HealthService(db)
    return await service.list_health_services(
        category=category, status_filter=status_filter
    )


# ============================================================================
# Appointments
# ============================================================================


@router.post(
    "/appointments",
    response_model=AppointmentResponse,
    summary="Schedule Appointment",
    description="Agenda uma consulta ou exame médico.\n\nArgs:\n    appointment_data: Dados do agendamento (serviceId, scheduledDate, notes)\n\nRequer autenticação JWT.",
    tags=["Health"],
)
async def schedule_appointment(
    payload: AppointmentCreate,
    db: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
) -> AppointmentResponse:
    """
    Agenda uma consulta ou exame médico.

    Args:
        payload: Dados do agendamento
        db: Sessão do banco de dados
        current_user_id: ID do usuário autenticado

    Returns:
        AppointmentResponse: Agendamento criado

    Raises:
        HTTPException: Se o serviço não for encontrado
    """
    from uuid import UUID

    service = HealthService(db)
    try:
        return await service.create_appointment(UUID(current_user_id), payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/appointments/user",
    response_model=UserAppointmentsResponse,
    summary="Get User Appointments",
    description="Retorna agendamentos médicos do usuário autenticado.\n\nArgs:\n    status_filter: Filtrar por status específico\n\nRequer autenticação JWT.",
    tags=["Health"],
)
async def get_user_appointments(
    status_filter: Optional[str] = None,
    db: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
) -> UserAppointmentsResponse:
    """
    Retorna agendamentos médicos do usuário autenticado.

    Args:
        status_filter: Filtrar por status específico
        db: Sessão do banco de dados
        current_user_id: ID do usuário autenticado

    Returns:
        UserAppointmentsResponse: Lista de agendamentos do usuário
    """
    from uuid import UUID

    service = HealthService(db)
    return await service.list_user_appointments(
        user_id=UUID(current_user_id), status_filter=status_filter
    )


@router.patch(
    "/appointments/{appointment_id}/cancel",
    response_model=CancelAppointmentResponse,
    summary="Cancel Appointment",
    description="Cancela um agendamento médico.\n\nArgs:\n    appointment_id: ID do agendamento a ser cancelado\n\nRequer autenticação JWT.",
    tags=["Health"],
)
async def cancel_appointment(
    appointment_id: str,
    db: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
) -> CancelAppointmentResponse:
    """
    Cancela um agendamento médico.

    Args:
        appointment_id: ID do agendamento a ser cancelado
        db: Sessão do banco de dados
        current_user_id: ID do usuário autenticado

    Returns:
        CancelAppointmentResponse: Confirmação de cancelamento

    Raises:
        HTTPException: Se o agendamento não for encontrado ou não pertencer ao usuário
    """
    from uuid import UUID

    service = HealthService(db)
    try:
        result = await service.cancel_appointment(UUID(current_user_id), appointment_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agendamento não encontrado",
            )
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


# ============================================================================
# Medical Records
# ============================================================================


@router.get(
    "/records/{appointment_id}",
    response_model=MedicalRecordResponse,
    summary="Get Medical Record",
    description="Retorna prontuário médico de um atendimento.\n\nArgs:\n    appointment_id: ID do agendamento relacionado\n\nRequer autenticação JWT.",
    tags=["Health"],
)
async def get_medical_record(
    appointment_id: str,
    db: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
) -> MedicalRecordResponse:
    """
    Retorna prontuário médico de um atendimento.

    Args:
        appointment_id: ID do agendamento relacionado
        db: Sessão do banco de dados
        current_user_id: ID do usuário autenticado

    Returns:
        MedicalRecordResponse: Prontuário médico

    Raises:
        HTTPException: Se o agendamento não for encontrado ou não pertencer ao usuário
    """
    from uuid import UUID

    service = HealthService(db)
    try:
        record = await service.get_medical_record(UUID(current_user_id), appointment_id)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prontuário médico não encontrado",
            )
        return record
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
