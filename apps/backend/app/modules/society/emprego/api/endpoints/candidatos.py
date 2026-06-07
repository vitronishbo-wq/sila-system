from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.society.emprego.api.deps import get_candidato_service
from apps.backend.app.modules.society.emprego.api.schemas.candidato_schema import (
    CandidatoCreate,
    CandidatoDeactivate,
    CandidatoFilter,
    CandidatoResponse,
)
from apps.backend.app.modules.society.emprego.application.services.candidato_service import (
    CandidatoService,
)
from apps.backend.app.modules.society.emprego.exceptions import (
    CandidatoAlreadyExistsError,
    CandidatoNotFoundError,
    CitizenNotFoundError,
)

router = APIRouter(prefix="/candidatos", tags=["Emprego - Candidatos"])

candidato_service_dep = Depends(get_candidato_service)
filtros_dep = Depends()


@router.post("/", response_model=CandidatoResponse, status_code=status.HTTP_201_CREATED)
async def registrar_candidato(
    data: CandidatoCreate, service: CandidatoService = candidato_service_dep
):
    try:
        return await service.registrar_candidato(
            citizen_id=data.citizen_id,
            escolaridade=data.escolaridade,
            situacao=data.situacao,
            areas_interesse=data.areas_interesse,
        )
    except CitizenNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except CandidatoAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.get("/", response_model=list[CandidatoResponse])
async def listar_candidatos(
    filtros: CandidatoFilter = filtros_dep, service: CandidatoService = candidato_service_dep
):
    return await service.buscar_candidatos(
        escolaridade=filtros.escolaridade, situacao=filtros.situacao, area=filtros.area_interesse
    )


@router.get("/{candidato_id}", response_model=CandidatoResponse)
async def obter_candidato(
    candidato_id: UUID, service: CandidatoService = candidato_service_dep
):
    candidato = await service.obter_por_id(candidato_id)
    if not candidato:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Candidato nao encontrado"
        )
    return candidato


@router.post("/{candidato_id}/desativar", response_model=CandidatoResponse)
async def desativar_candidato(
    candidato_id: UUID,
    data: CandidatoDeactivate,
    service: CandidatoService = candidato_service_dep,
):
    try:
        return await service.desativar_candidato(
            candidato_id=candidato_id, motivo=data.motivo, actor_id=data.actor_id
        )
    except CandidatoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc