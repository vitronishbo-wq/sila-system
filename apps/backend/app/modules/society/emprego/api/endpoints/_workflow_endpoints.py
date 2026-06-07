from collections.abc import Callable
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status


def build_workflow_router(
    *,
    tag: str,
    get_service: Callable,
    create_schema: Any,
    action_schema: Any,
    cancel_schema: Any,
    response_schema: Any,
    routes: list[tuple[str, str]],
) -> APIRouter:
    router = APIRouter(tags=[tag])
    service_dep = Depends(get_service)

    def _register_create(path: str, service_type: str) -> None:

        async def _create(data: create_schema, service=service_dep):
            try:
                return await service.criar_registro(
                    service_type=service_type,
                    citizen_id=data.citizen_id,
                    observacoes=data.observacoes,
                    metadata=data.metadata,
                )
            except ValueError as exc:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

        _create.__name__ = f"create_{service_type}"
        router.add_api_route(
            path,
            _create,
            methods=["POST"],
            response_model=response_schema,
            status_code=status.HTTP_201_CREATED,
            operation_id=f"{tag}_workflow_create_{service_type}",
        )

    for path, service_type in routes:
        _register_create(path, service_type)

    @router.get(
        "/workflow/{item_id}",
        response_model=response_schema,
        operation_id=f"{tag}_workflow_get_item",
    )
    async def get_item(item_id: UUID, service=service_dep):
        item = await service.obter_por_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Registro nao encontrado"
            )
        return item

    @router.get(
        "/workflow/citizen/{citizen_id}",
        response_model=list[response_schema],
        operation_id=f"{tag}_workflow_list_items",
    )
    async def list_items(
        citizen_id: UUID, service_type: str | None = None, service=service_dep
    ):
        return await service.listar_por_cidadao(citizen_id, service_type)

    @router.post(
        "/workflow/{item_id}/concluir",
        response_model=response_schema,
        operation_id=f"{tag}_workflow_concluir_item",
    )
    async def concluir_item(item_id: UUID, data: action_schema, service=service_dep):
        try:
            return await service.concluir_registro(
                item_id=item_id, actor_id=data.actor_id, observacoes=data.observacoes
            )
        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    @router.post(
        "/workflow/{item_id}/cancelar",
        response_model=response_schema,
        operation_id=f"{tag}_workflow_cancelar_item",
    )
    async def cancelar_item(item_id: UUID, data: cancel_schema, service=service_dep):
        try:
            return await service.cancelar_registro(
                item_id=item_id, actor_id=data.actor_id, motivo=data.motivo
            )
        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return router
