from __future__ import annotations
from typing import Any, Callable
from uuid import UUID
from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic import ValidationError
from apps.backend.app.modules.economy.trade.external.domain.enums import StatusHabilitacao

def build_habilitacao_router(*, prefix: str, tag: str, get_service: Callable[..., Any], create_schema: type[Any], aprovacao_schema: type[Any], rejeicao_schema: type[Any], response_schema: type[Any], already_exists_error_cls: type[Exception], not_found_error_cls: type[Exception], invalid_state_error_cls: type[Exception]) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=[tag])

    def _validate_payload(schema_cls: type[Any], payload: dict[str, Any]) -> Any:
        try:
            return schema_cls.model_validate(payload)
        except ValidationError as exc:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.errors()) from exc

    @router.post('/', response_model=response_schema, status_code=status.HTTP_201_CREATED)
    async def solicitar(data: dict[str, Any]=Body(...), service: Any=Depends(get_service)):
        try:
            payload = _validate_payload(create_schema, data)
            return await service.solicitar(tipo_pessoa=payload.tipo_pessoa, razao_social=payload.razao_social, cnpj_cpf=payload.cnpj_cpf, numero_processo=payload.numero_processo, data_solicitacao=payload.data_solicitacao)
        except already_exists_error_cls as exc:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    @router.patch('/{item_id}/aprovar', response_model=response_schema)
    async def aprovar(item_id: UUID, data: dict[str, Any]=Body(...), service: Any=Depends(get_service)):
        try:
            payload = _validate_payload(aprovacao_schema, data)
            return await service.aprovar(item_id, numero_radar=payload.numero_radar, data_analise=payload.data_analise, data_validade=payload.data_validade)
        except not_found_error_cls as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
        except invalid_state_error_cls as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    @router.patch('/{item_id}/rejeitar', response_model=response_schema)
    async def rejeitar(item_id: UUID, data: dict[str, Any]=Body(...), service: Any=Depends(get_service)):
        try:
            payload = _validate_payload(rejeicao_schema, data)
            return await service.rejeitar(item_id, data_analise=payload.data_analise, motivo=payload.motivo)
        except not_found_error_cls as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
        except invalid_state_error_cls as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    @router.patch('/{item_id}/reabrir', response_model=response_schema)
    async def reabrir(item_id: UUID, service: Any=Depends(get_service)):
        try:
            return await service.reabrir(item_id)
        except not_found_error_cls as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
        except invalid_state_error_cls as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    @router.get('/{item_id}', response_model=response_schema)
    async def obter_por_id(item_id: UUID, service: Any=Depends(get_service)):
        try:
            return await service.obter_por_id(item_id)
        except not_found_error_cls as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

    @router.get('/', response_model=list[response_schema])
    async def listar(status_habilitacao: StatusHabilitacao | None=None, service: Any=Depends(get_service)):
        return await service.listar(status=status_habilitacao)
    return router