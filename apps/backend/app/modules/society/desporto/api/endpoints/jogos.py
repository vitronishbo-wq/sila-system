from __future__ import annotations

from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.society.desporto.api.deps import get_jogo_service
from apps.backend.app.modules.society.desporto.api.schemas.jogo_schema import (
    JogoCreate,
    JogoResponse,
    JogoResultadoUpdate,
    JogoUpdate,
)
from apps.backend.app.modules.society.desporto.application.services.jogo_service import JogoService
from apps.backend.app.modules.society.desporto.domain.enums import StatusJogo

router = APIRouter(prefix="/jogos", tags=["Desporto - Jogos"])

jogo_service_dep = Depends(get_jogo_service)


@router.post("/", response_model=JogoResponse, status_code=status.HTTP_201_CREATED)
async def agendar_jogo(
    data: JogoCreate, service: JogoService = jogo_service_dep
) -> JogoResponse:
    try:
        return await service.agendar_jogo(
            competicao_id=data.competicao_id,
            clube_casa_id=data.clube_casa_id,
            clube_fora_id=data.clube_fora_id,
            data_jogo=data.data_jogo,
            local=data.local,
            municipio=data.municipio,
            provincia=data.provincia,
            codigo_obra_instalacao=data.codigo_obra_instalacao,
            atracao_turistica_id=data.atracao_turistica_id,
            publico_estimado=data.publico_estimado,
            observacoes=data.observacoes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{jogo_id}", response_model=JogoResponse)
async def obter_jogo(
    jogo_id: UUID, service: JogoService = jogo_service_dep
) -> JogoResponse:
    try:
        return await service.buscar_jogo(jogo_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[JogoResponse])
async def listar_jogos(
    competicao_id: UUID | None = None,
    clube_id: UUID | None = None,
    status_filtro: StatusJogo | None = None,
    data_inicio: date | None = None,
    data_fim: date | None = None,
    somente_ativos: bool = True,
    service: JogoService = jogo_service_dep,
) -> list[JogoResponse]:
    return await service.listar_jogos(
        competicao_id=competicao_id,
        clube_id=clube_id,
        status=status_filtro,
        data_inicio=data_inicio,
        data_fim=data_fim,
        somente_ativos=somente_ativos,
    )


@router.patch("/{jogo_id}", response_model=JogoResponse)
async def atualizar_jogo(
    jogo_id: UUID, data: JogoUpdate, service: JogoService = jogo_service_dep
) -> JogoResponse:
    try:
        return await service.atualizar_jogo(
            jogo_id=jogo_id,
            data_jogo=data.data_jogo,
            local=data.local,
            municipio=data.municipio,
            provincia=data.provincia,
            status=data.status,
            codigo_obra_instalacao=data.codigo_obra_instalacao,
            atracao_turistica_id=data.atracao_turistica_id,
            publico_estimado=data.publico_estimado,
            publico_presente=data.publico_presente,
            ativo=data.ativo,
            observacoes=data.observacoes,
        )
    except ValueError as exc:
        message = str(exc).lower()
        code = (
            status.HTTP_404_NOT_FOUND
            if "nao encontrado" in message
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=code, detail=str(exc)) from exc


@router.post("/{jogo_id}/resultado", response_model=JogoResponse)
async def registrar_resultado(
    jogo_id: UUID, data: JogoResultadoUpdate, service: JogoService = jogo_service_dep
) -> JogoResponse:
    try:
        return await service.registrar_resultado(
            jogo_id=jogo_id, placar_casa=data.placar_casa, placar_fora=data.placar_fora
        )
    except ValueError as exc:
        message = str(exc).lower()
        code = (
            status.HTTP_404_NOT_FOUND
            if "nao encontrado" in message
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=code, detail=str(exc)) from exc


@router.delete("/{jogo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_jogo(jogo_id: UUID, service: JogoService = jogo_service_dep) -> None:
    try:
        await service.remover_jogo(jogo_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc