"""
Governance module controller - FastAPI routes with full type safety.

This controller follows the OpenAPI contract and uses Pydantic schemas for validation.
All endpoints are properly typed with response_model for automatic Swagger documentation.
"""

from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.session import get_async_db as get_session
from core.security import get_current_user_id

# Import API response schemas
from modules.common.schemas.api_responses import PingResponse

# Import Governance module schemas
from modules.governance.schemas.api_schemas import (
    CouncilMeetingCreate,
    CouncilMeetingResponse,
    CouncilMeetingsListResponse,
    CouncilMeetingUpdate,
    DecisionCreate,
    DecisionResponse,
    DecisionsListResponse,
    DecisionUpdate,
    InstitutionCreate,
    InstitutionResponse,
    InstitutionsListResponse,
    InstitutionUpdate,
    MandateCreate,
    MandateResponse,
    MandatesListResponse,
    MandateUpdate,
)

# Import Governance service
from modules.governance.service import GovernanceService

# Create router
router = APIRouter()


# ============================================================================
# Governance Ping
# ============================================================================


@router.get(
    "/ping",
    response_model=PingResponse,
    summary="Ping",
    description="Health check do módulo governance.",
    tags=["Governance"],
)
async def ping():
    """Health check do módulo governance."""
    return PingResponse(message="pong", timestamp=datetime.now(timezone.utc))


# ============================================================================
# Institutions CRUD
# ============================================================================


@router.post(
    "/institutions",
    response_model=InstitutionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Institution",
    description="Cria uma nova instituição.",
    tags=["Governance - Institutions"],
)
async def create_institution(
    payload: InstitutionCreate,
    db: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
) -> InstitutionResponse:
    """
    Cria uma nova instituição.

    Args:
        payload: Dados da instituição
        db: Sessão do banco de dados
        current_user_id: ID do usuário autenticado

    Returns:
        InstitutionResponse: Instituição criada
    """
    service = GovernanceService(db)
    return await service.create_institution(payload)


@router.get(
    "/institutions",
    response_model=InstitutionsListResponse,
    summary="List Institutions",
    description="Lista todas as instituições.",
    tags=["Governance - Institutions"],
)
async def list_institutions(
    institution_type: Optional[str] = Query(
        None, description="Filter by institution type"
    ),
    parent_id: Optional[UUID] = Query(
        None, description="Filter by parent institution ID"
    ),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of records to return"
    ),
    db: AsyncSession = Depends(get_session),
) -> InstitutionsListResponse:
    """
    Lista todas as instituições.

    Args:
        institution_type: Filtrar por tipo de instituição
        parent_id: Filtrar por instituição pai
        skip: Número de registros a pular
        limit: Número máximo de registros a retornar
        db: Sessão do banco de dados

    Returns:
        InstitutionsListResponse: Lista de instituições
    """
    service = GovernanceService(db)
    return await service.list_institutions(
        institution_type=institution_type,
        parent_id=parent_id,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/institutions/{institution_id}",
    response_model=InstitutionResponse,
    summary="Get Institution",
    description="Busca uma instituição específica.",
    tags=["Governance - Institutions"],
)
async def get_institution(
    institution_id: UUID,
    db: AsyncSession = Depends(get_session),
) -> InstitutionResponse:
    """
    Busca uma instituição específica.

    Args:
        institution_id: ID da instituição
        db: Sessão do banco de dados

    Returns:
        InstitutionResponse: Instituição encontrada

    Raises:
        HTTPException: Se a instituição não for encontrada
    """
    service = GovernanceService(db)
    institution = await service.get_institution(institution_id)
    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Institution not found"
        )
    return institution


@router.put(
    "/institutions/{institution_id}",
    response_model=InstitutionResponse,
    summary="Update Institution",
    description="Atualiza uma instituição.",
    tags=["Governance - Institutions"],
)
async def update_institution(
    institution_id: UUID,
    payload: InstitutionUpdate,
    db: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
) -> InstitutionResponse:
    """
    Atualiza uma instituição.

    Args:
        institution_id: ID da instituição
        payload: Dados para atualização
        db: Sessão do banco de dados
        current_user_id: ID do usuário autenticado

    Returns:
        InstitutionResponse: Instituição atualizada

    Raises:
        HTTPException: Se a instituição não for encontrada
    """
    service = GovernanceService(db)
    institution = await service.update_institution(institution_id, payload)
    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Institution not found"
        )
    return institution


@router.delete(
    "/institutions/{institution_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Institution",
    description="Deleta uma instituição.",
    tags=["Governance - Institutions"],
)
async def delete_institution(
    institution_id: UUID,
    db: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
):
    """
    Deleta uma instituição.

    Args:
        institution_id: ID da instituição
        db: Sessão do banco de dados
        current_user_id: ID do usuário autenticado

    Raises:
        HTTPException: Se a instituição não for encontrada
    """
    service = GovernanceService(db)
    deleted = await service.delete_institution(institution_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Institution not found"
        )


# ============================================================================
# Mandates CRUD
# ============================================================================


@router.post(
    "/mandates",
    response_model=MandateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Mandate",
    description="Cria um novo mandato.",
    tags=["Governance - Mandates"],
)
async def create_mandate(
    payload: MandateCreate,
    db: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
) -> MandateResponse:
    """
    Cria um novo mandato.

    Args:
        payload: Dados do mandato
        db: Sessão do banco de dados
        current_user_id: ID do usuário autenticado

    Returns:
        MandateResponse: Mandato criado
    """
    service = GovernanceService(db)
    return await service.create_mandate(payload)


@router.get(
    "/mandates",
    response_model=MandatesListResponse,
    summary="List Mandates",
    description="Lista todos os mandatos.",
    tags=["Governance - Mandates"],
)
async def list_mandates(
    institution_id: Optional[UUID] = Query(
        None, description="Filter by institution ID"
    ),
    status_filter: Optional[str] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of records to return"
    ),
    db: AsyncSession = Depends(get_session),
) -> MandatesListResponse:
    """
    Lista todos os mandatos.

    Args:
        institution_id: Filtrar por instituição
        status_filter: Filtrar por status
        skip: Número de registros a pular
        limit: Número máximo de registros a retornar
        db: Sessão do banco de dados

    Returns:
        MandatesListResponse: Lista de mandatos
    """
    service = GovernanceService(db)
    return await service.list_mandates(
        institution_id=institution_id,
        status=status_filter,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/mandates/{mandate_id}",
    response_model=MandateResponse,
    summary="Get Mandate",
    description="Busca um mandato específico.",
    tags=["Governance - Mandates"],
)
async def get_mandate(
    mandate_id: UUID,
    db: AsyncSession = Depends(get_session),
) -> MandateResponse:
    """
    Busca um mandato específico.

    Args:
        mandate_id: ID do mandato
        db: Sessão do banco de dados

    Returns:
        MandateResponse: Mandato encontrado

    Raises:
        HTTPException: Se o mandato não for encontrado
    """
    service = GovernanceService(db)
    mandate = await service.get_mandate(mandate_id)
    if not mandate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Mandate not found"
        )
    return mandate


@router.put(
    "/mandates/{mandate_id}",
    response_model=MandateResponse,
    summary="Update Mandate",
    description="Atualiza um mandato.",
    tags=["Governance - Mandates"],
)
async def update_mandate(
    mandate_id: UUID,
    payload: MandateUpdate,
    db: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
) -> MandateResponse:
    """
    Atualiza um mandato.

    Args:
        mandate_id: ID do mandato
        payload: Dados para atualização
        db: Sessão do banco de dados
        current_user_id: ID do usuário autenticado

    Returns:
        MandateResponse: Mandato atualizado

    Raises:
        HTTPException: Se o mandato não for encontrado
    """
    service = GovernanceService(db)
    mandate = await service.update_mandate(mandate_id, payload)
    if not mandate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Mandate not found"
        )
    return mandate


@router.delete(
    "/mandates/{mandate_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Mandate",
    description="Deleta um mandato.",
    tags=["Governance - Mandates"],
)
async def delete_mandate(
    mandate_id: UUID,
    db: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
):
    """
    Deleta um mandato.

    Args:
        mandate_id: ID do mandato
        db: Sessão do banco de dados
        current_user_id: ID do usuário autenticado

    Raises:
        HTTPException: Se o mandato não for encontrado
    """
    service = GovernanceService(db)
    deleted = await service.delete_mandate(mandate_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Mandate not found"
        )


# ============================================================================
# Decisions CRUD
# ============================================================================


@router.post(
    "/decisions",
    response_model=DecisionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Decision",
    description="Cria uma nova decisão.",
    tags=["Governance - Decisions"],
)
async def create_decision(
    payload: DecisionCreate,
    db: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
) -> DecisionResponse:
    """
    Cria uma nova decisão.

    Args:
        payload: Dados da decisão
        db: Sessão do banco de dados
        current_user_id: ID do usuário autenticado

    Returns:
        DecisionResponse: Decisão criada
    """
    service = GovernanceService(db)
    return await service.create_decision(payload)


@router.get(
    "/decisions",
    response_model=DecisionsListResponse,
    summary="List Decisions",
    description="Lista todas as decisões.",
    tags=["Governance - Decisions"],
)
async def list_decisions(
    meeting_id: Optional[UUID] = Query(None, description="Filter by meeting ID"),
    status_filter: Optional[str] = Query(None, description="Filter by status"),
    decision_type: Optional[str] = Query(None, description="Filter by decision type"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of records to return"
    ),
    db: AsyncSession = Depends(get_session),
) -> DecisionsListResponse:
    """
    Lista todas as decisões.

    Args:
        meeting_id: Filtrar por reunião
        status_filter: Filtrar por status
        decision_type: Filtrar por tipo de decisão
        skip: Número de registros a pular
        limit: Número máximo de registros a retornar
        db: Sessão do banco de dados

    Returns:
        DecisionsListResponse: Lista de decisões
    """
    service = GovernanceService(db)
    return await service.list_decisions(
        meeting_id=meeting_id,
        status=status_filter,
        decision_type=decision_type,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/decisions/{decision_id}",
    response_model=DecisionResponse,
    summary="Get Decision",
    description="Busca uma decisão específica.",
    tags=["Governance - Decisions"],
)
async def get_decision(
    decision_id: UUID,
    db: AsyncSession = Depends(get_session),
) -> DecisionResponse:
    """
    Busca uma decisão específica.

    Args:
        decision_id: ID da decisão
        db: Sessão do banco de dados

    Returns:
        DecisionResponse: Decisão encontrada

    Raises:
        HTTPException: Se a decisão não for encontrada
    """
    service = GovernanceService(db)
    decision = await service.get_decision(decision_id)
    if not decision:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Decision not found"
        )
    return decision


@router.put(
    "/decisions/{decision_id}",
    response_model=DecisionResponse,
    summary="Update Decision",
    description="Atualiza uma decisão.",
    tags=["Governance - Decisions"],
)
async def update_decision(
    decision_id: UUID,
    payload: DecisionUpdate,
    db: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
) -> DecisionResponse:
    """
    Atualiza uma decisão.

    Args:
        decision_id: ID da decisão
        payload: Dados para atualização
        db: Sessão do banco de dados
        current_user_id: ID do usuário autenticado

    Returns:
        DecisionResponse: Decisão atualizada

    Raises:
        HTTPException: Se a decisão não for encontrada
    """
    service = GovernanceService(db)
    decision = await service.update_decision(decision_id, payload)
    if not decision:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Decision not found"
        )
    return decision


@router.delete(
    "/decisions/{decision_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Decision",
    description="Deleta uma decisão.",
    tags=["Governance - Decisions"],
)
async def delete_decision(
    decision_id: UUID,
    db: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
):
    """
    Deleta uma decisão.

    Args:
        decision_id: ID da decisão
        db: Sessão do banco de dados
        current_user_id: ID do usuário autenticado

    Raises:
        HTTPException: Se a decisão não for encontrada
    """
    service = GovernanceService(db)
    deleted = await service.delete_decision(decision_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Decision not found"
        )


# ============================================================================
# Council Meetings CRUD
# ============================================================================


@router.post(
    "/council-meetings",
    response_model=CouncilMeetingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Council Meeting",
    description="Cria uma nova reunião de conselho.",
    tags=["Governance - Council Meetings"],
)
async def create_council_meeting(
    payload: CouncilMeetingCreate,
    db: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
) -> CouncilMeetingResponse:
    """
    Cria uma nova reunião de conselho.

    Args:
        payload: Dados da reunião
        db: Sessão do banco de dados
        current_user_id: ID do usuário autenticado

    Returns:
        CouncilMeetingResponse: Reunião criada
    """
    service = GovernanceService(db)
    return await service.create_council_meeting(payload)


@router.get(
    "/council-meetings",
    response_model=CouncilMeetingsListResponse,
    summary="List Council Meetings",
    description="Lista todas as reuniões de conselho.",
    tags=["Governance - Council Meetings"],
)
async def list_council_meetings(
    council_id: Optional[UUID] = Query(None, description="Filter by council ID"),
    status_filter: Optional[str] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of records to return"
    ),
    db: AsyncSession = Depends(get_session),
) -> CouncilMeetingsListResponse:
    """
    Lista todas as reuniões de conselho.

    Args:
        council_id: Filtrar por conselho
        status_filter: Filtrar por status
        skip: Número de registros a pular
        limit: Número máximo de registros a retornar
        db: Sessão do banco de dados

    Returns:
        CouncilMeetingsListResponse: Lista de reuniões
    """
    service = GovernanceService(db)
    return await service.list_council_meetings(
        council_id=council_id,
        status=status_filter,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/council-meetings/{meeting_id}",
    response_model=CouncilMeetingResponse,
    summary="Get Council Meeting",
    description="Busca uma reunião de conselho específica.",
    tags=["Governance - Council Meetings"],
)
async def get_council_meeting(
    meeting_id: UUID,
    db: AsyncSession = Depends(get_session),
) -> CouncilMeetingResponse:
    """
    Busca uma reunião de conselho específica.

    Args:
        meeting_id: ID da reunião
        db: Sessão do banco de dados

    Returns:
        CouncilMeetingResponse: Reunião encontrada

    Raises:
        HTTPException: Se a reunião não for encontrada
    """
    service = GovernanceService(db)
    meeting = await service.get_council_meeting(meeting_id)
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Council meeting not found"
        )
    return meeting


@router.put(
    "/council-meetings/{meeting_id}",
    response_model=CouncilMeetingResponse,
    summary="Update Council Meeting",
    description="Atualiza uma reunião de conselho.",
    tags=["Governance - Council Meetings"],
)
async def update_council_meeting(
    meeting_id: UUID,
    payload: CouncilMeetingUpdate,
    db: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
) -> CouncilMeetingResponse:
    """
    Atualiza uma reunião de conselho.

    Args:
        meeting_id: ID da reunião
        payload: Dados para atualização
        db: Sessão do banco de dados
        current_user_id: ID do usuário autenticado

    Returns:
        CouncilMeetingResponse: Reunião atualizada

    Raises:
        HTTPException: Se a reunião não for encontrada
    """
    service = GovernanceService(db)
    meeting = await service.update_council_meeting(meeting_id, payload)
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Council meeting not found"
        )
    return meeting


@router.delete(
    "/council-meetings/{meeting_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Council Meeting",
    description="Deleta uma reunião de conselho.",
    tags=["Governance - Council Meetings"],
)
async def delete_council_meeting(
    meeting_id: UUID,
    db: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
):
    """
    Deleta uma reunião de conselho.

    Args:
        meeting_id: ID da reunião
        db: Sessão do banco de dados
        current_user_id: ID do usuário autenticado

    Raises:
        HTTPException: Se a reunião não for encontrada
    """
    service = GovernanceService(db)
    deleted = await service.delete_council_meeting(meeting_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Council meeting not found"
        )
