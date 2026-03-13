from __future__ import annotations
from typing import Any, Callable
from uuid import UUID
from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic import ValidationError
from app.modules.economy.trade.external.domain.enums import StatusHabilitacao

def build_operador_logistico_router(*, prefix: str, tag: str, get_service: Callable[..., Any], create_schema: type[Any], habilitacao_schema: type[Any], suspensao_schema: type[Any], cancelamento_schema: type[Any], response_schema: type[Any], already_exists_error_cls: type[Exception], not_found_error_cls: type[Exception], invalid_state_error_cls: type[Exception]) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=[tag])

    def _validate_payload(schema_cls: type[Any], payload: dict[str, Any]) -> Any:
        try:
            return schema_cls.model_validate(payload)
        except ValidationError as exc:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.errors()) from exc

    @router.post('/', response_model=response_schema, status_code=status.HTTP_201_CREATED)
    async def cadastrar(data: dict[str, Any]=Body(...), service: Any=Depends(get_service)):
        try:
            payload = _validate_payload(create_schema, data)
            return await service.cadastrar(razao_social=payload.razao_social, cnpj_cpf=payload.cnpj_cpf, tipo_pessoa=payload.tipo_pessoa, endereco=payload.endereco, numero=payload.numero, bairro=payload.bairro, municipio=payload.municipio, provincia=payload.provincia, cep=payload.cep)
        except already_exists_error_cls as exc:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    @router.patch('/{item_id}/habilitar', response_model=response_schema)
    async def habilitar(item_id: UUID, data: dict[str, Any]=Body(...), service: Any=Depends(get_service)):
        try:
            payload = _validate_payload(habilitacao_schema, data)
            return await service.habilitar(item_id, numero_radar=payload.numero_radar, data_habilitacao=payload.data_habilitacao, data_validade=payload.data_validade)
        except not_found_error_cls as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
        except invalid_state_error_cls as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    @router.patch('/{item_id}/suspender', response_model=response_schema)
    async def suspender(item_id: UUID, data: dict[str, Any]=Body(...), service: Any=Depends(get_service)):
        try:
            payload = _validate_payload(suspensao_schema, data)
            return await service.suspender(item_id, data_suspensao=payload.data_suspensao, motivo=payload.motivo)
        except not_found_error_cls as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
        except invalid_state_error_cls as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    @router.patch('/{item_id}/cancelar', response_model=response_schema)
    async def cancelar(item_id: UUID, data: dict[str, Any]=Body(...), service: Any=Depends(get_service)):
        try:
            payload = _validate_payload(cancelamento_schema, data)
            return await service.cancelar(item_id, data_cancelamento=payload.data_cancelamento, motivo=payload.motivo)
        except not_found_error_cls as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
        except invalid_state_error_cls as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    @router.patch('/{item_id}/reabilitar', response_model=response_schema)
    async def reabilitar(item_id: UUID, service: Any=Depends(get_service)):
        try:
            return await service.reabilitar(item_id)
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
    async def listar(status_habilitacao: StatusHabilitacao | None=None, municipio: str | None=None, service: Any=Depends(get_service)):
        return await service.listar(status=status_habilitacao, municipio=municipio)
    return router