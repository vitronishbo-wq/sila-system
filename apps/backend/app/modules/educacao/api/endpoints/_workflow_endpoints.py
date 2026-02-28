from __future__ import annotations

from typing import Any, Callable
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user


def build_workflow_router(
    *,
    tag: str,
    get_service: Callable,
    create_schema: Any,
    response_schema: Any,
    concluir_schema: Any,
    cancelar_schema: Any,
    routes: list[tuple[str, str]],
) -> APIRouter:
    router = APIRouter(tags=[tag])

    def actor_id(user: dict) -> UUID:
        user_id = user.get("user_id") if user else None
        if not user_id:
            return UUID(int=0)
        return UUID(user_id)

    def register_create(path: str, service_type: str) -> None:
        async def create(
            data: create_schema,
            service=Depends(get_service),
            _: dict = Depends(get_current_user),
        ):
            try:
                return await service.create_record(
                    service_type=service_type,
                    citizen_id=data.citizen_id,
                    instituicao_id=data.instituicao_id,
                    observacoes=data.observacoes,
                    metadata=data.metadata,
                )
            except ValueError as exc:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

        create.__name__ = f"create_{service_type}"
        router.add_api_route(path, create, methods=["POST"], response_model=response_schema, status_code=status.HTTP_201_CREATED)

    for path, service_type in routes:
        register_create(path, service_type)

    @router.get("/workflow/{record_id}", response_model=response_schema)
    async def get_record(record_id: UUID, service=Depends(get_service), _: dict = Depends(get_current_user)):
        item = await service.get_record(record_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registo nao encontrado")
        return item

    @router.get("/workflow/citizen/{citizen_id}", response_model=list[response_schema])
    async def list_by_citizen(
        citizen_id: UUID,
        service_type: str | None = None,
        service=Depends(get_service),
        _: dict = Depends(get_current_user),
    ):
        return await service.list_records(citizen_id, service_type)

    @router.post("/workflow/{record_id}/concluir", response_model=response_schema)
    async def conclude(
        record_id: UUID,
        data: concluir_schema,
        service=Depends(get_service),
        user: dict = Depends(get_current_user),
    ):
        try:
            return await service.conclude_record(record_id, actor_id(user), data.resumo)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    @router.post("/workflow/{record_id}/cancelar", response_model=response_schema)
    async def cancel(
        record_id: UUID,
        data: cancelar_schema,
        service=Depends(get_service),
        user: dict = Depends(get_current_user),
    ):
        try:
            return await service.cancel_record(record_id, actor_id(user), data.motivo)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    return router
