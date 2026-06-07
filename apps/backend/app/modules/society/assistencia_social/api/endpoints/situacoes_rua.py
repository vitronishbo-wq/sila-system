from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, status

from apps.backend.app.modules.society.assistencia_social.api.deps import get_situacao_rua_service
from apps.backend.app.modules.society.assistencia_social.api.endpoints._errors import (
    raise_http_for_value_error,
)
from apps.backend.app.modules.society.assistencia_social.api.schemas.situacao_rua_schema import (
    SituacaoRuaCreate,
    SituacaoRuaResponse,
)
from apps.backend.app.modules.society.assistencia_social.application.services.situacao_rua_service import (
    SituacaoRuaService,
)

router = APIRouter(prefix="/situacoes-rua", tags=["Assistencia Social - Situacao Rua"])

situacao_rua_service_dep = Depends(get_situacao_rua_service)


@router.post("/", response_model=SituacaoRuaResponse, status_code=status.HTTP_201_CREATED)
async def registrar_situacao_rua(
    data: SituacaoRuaCreate, service: SituacaoRuaService = situacao_rua_service_dep
) -> SituacaoRuaResponse:
    try:
        return await service.registrar_situacao(
            beneficiario_id=data.beneficiario_id, localizacao=data.localizacao, motivo=data.motivo
        )
    except ValueError as exc:
        raise_http_for_value_error(exc)


@router.get("/{situacao_id}", response_model=SituacaoRuaResponse)
async def obter_situacao_rua(
    situacao_id: UUID, service: SituacaoRuaService = situacao_rua_service_dep
) -> SituacaoRuaResponse:
    try:
        return await service.buscar_situacao(situacao_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)


@router.get("/", response_model=list[SituacaoRuaResponse])
async def listar_situacoes_rua(
    beneficiario_id: UUID | None = None,
    service: SituacaoRuaService = situacao_rua_service_dep,
) -> list[SituacaoRuaResponse]:
    return await service.listar_situacoes(beneficiario_id=beneficiario_id)


@router.patch("/{situacao_id}/encerrar", response_model=SituacaoRuaResponse)
async def encerrar_situacao_rua(
    situacao_id: UUID, service: SituacaoRuaService = situacao_rua_service_dep
) -> SituacaoRuaResponse:
    try:
        return await service.encerrar_situacao(situacao_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)


@router.delete("/{situacao_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_situacao_rua(
    situacao_id: UUID, service: SituacaoRuaService = situacao_rua_service_dep
) -> None:
    try:
        await service.remover_situacao(situacao_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)