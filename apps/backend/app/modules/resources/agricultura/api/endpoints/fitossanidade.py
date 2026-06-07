from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.resources.agricultura.api.deps import get_fitossanidade_service
from apps.backend.app.modules.resources.agricultura.api.schemas.ocorrencia_schema import (
    OcorrenciaCreate,
    OcorrenciaResponse,
)
from apps.backend.app.modules.resources.agricultura.application.services.fitossanidade_service import (
    FitossanidadeService,
)
from apps.backend.app.modules.resources.agricultura.domain.enums import StatusOcorrencia
from apps.backend.app.modules.resources.agricultura.exceptions import (
    OcorrenciaNotFoundError,
    PropriedadeNotFoundError,
)

router = APIRouter(prefix="/fitossanidade", tags=["Agricultura - fitossanidade"])
fitossanidade_service_dep = Depends(get_fitossanidade_service)


@router.post("/", response_model=OcorrenciaResponse, status_code=status.HTTP_201_CREATED)
async def registrar_ocorrencia(
    data: OcorrenciaCreate, service: FitossanidadeService = fitossanidade_service_dep
):
    try:
        return await service.registrar_ocorrencia(
            codigo_propriedade=data.codigo_propriedade,
            praga_doenca=data.praga_doenca,
            descricao=data.descricao,
            severidade=data.severidade,
            cultura_afetada=data.cultura_afetada,
            acao_recomendada=data.acao_recomendada,
        )
    except PropriedadeNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/{codigo_ocorrencia:path}/tratar", response_model=OcorrenciaResponse)
async def iniciar_tratamento(
    codigo_ocorrencia: str, service: FitossanidadeService = fitossanidade_service_dep
):
    try:
        return await service.iniciar_tratamento(codigo_ocorrencia)
    except OcorrenciaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_ocorrencia:path}/resolver", response_model=OcorrenciaResponse)
async def resolver_ocorrencia(
    codigo_ocorrencia: str, service: FitossanidadeService = fitossanidade_service_dep
):
    try:
        return await service.resolver(codigo_ocorrencia)
    except OcorrenciaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{codigo_ocorrencia:path}", response_model=OcorrenciaResponse)
async def obter_ocorrencia(
    codigo_ocorrencia: str, service: FitossanidadeService = fitossanidade_service_dep
):
    try:
        return await service.obter(codigo_ocorrencia)
    except OcorrenciaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[OcorrenciaResponse])
async def listar_ocorrencias(
    codigo_propriedade: str | None = None,
    status_ocorrencia: StatusOcorrencia | None = None,
    service: FitossanidadeService = fitossanidade_service_dep,
):
    return await service.listar(codigo_propriedade=codigo_propriedade, status=status_ocorrencia)
