from collections.abc import Callable
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.api.deps import get_current_user, get_db
from apps.backend.app.modules.educacao.infrastructure.models.escola_model import EscolaModel
from apps.backend.app.core.rbac.territorial_access import verify_territorial_access


async def _check_instituicao_territory(instituicao_id: Any, user: dict, db: AsyncSession) -> None:
    if instituicao_id is None:
        return
    try:
        inst_id = UUID(str(instituicao_id))
    except (ValueError, TypeError):
        return
    escola = await db.get(EscolaModel, inst_id)
    if escola:
        await verify_territorial_access(user=user, resource_territory_id=getattr(escola, "territory_id", None), db=db)


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
            data: dict[str, Any] = Body(...),
            service: Any = Depends(get_service),
            user: dict = Depends(get_current_user),
            db: AsyncSession = Depends(get_db),
        ):
            await _check_instituicao_territory(data.get("instituicao_id"), user, db)
            try:
                return await service.create_record(
                    service_type=service_type,
                    citizen_id=data.get("citizen_id"),
                    instituicao_id=data.get("instituicao_id"),
                    observacoes=data.get("observacoes"),
                    metadata=data.get("metadata"),
                )
            except ValueError as exc:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

        create.__name__ = f"create_{service_type}"
        router.add_api_route(
            path,
            create,
            methods=["POST"],
            response_model=response_schema,
            status_code=status.HTTP_201_CREATED,
        )

    for path, service_type in routes:
        register_create(path, service_type)

    @router.get("/workflow/{record_id}", response_model=response_schema)
    async def get_record(
        record_id: UUID,
        service: Any = Depends(get_service),
        user: dict = Depends(get_current_user),
    ):
        item = await service.get_record(record_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Registo nao encontrado"
            )
        return item

    @router.get("/workflow/citizen/{citizen_id}", response_model=list[response_schema])
    async def list_by_citizen(
        citizen_id: UUID,
        service_type: str | None = None,
        service: Any = Depends(get_service),
        user: dict = Depends(get_current_user),
    ):
        return await service.list_records(citizen_id, service_type)

    @router.post("/workflow/{record_id}/concluir", response_model=response_schema)
    async def conclude(
        record_id: UUID,
        data: dict[str, Any] = Body(...),
        service: Any = Depends(get_service),
        user: dict = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):
        item = await service.get_record(record_id)
        if item and hasattr(item, "get"):
            await _check_instituicao_territory(item.get("instituicao_id"), user, db)
        try:
            return await service.conclude_record(record_id, user.get("user_id"), data.get("resumo"))
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    @router.post("/workflow/{record_id}/cancelar", response_model=response_schema)
    async def cancel(
        record_id: UUID,
        data: dict[str, Any] = Body(...),
        service: Any = Depends(get_service),
        user: dict = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):
        item = await service.get_record(record_id)
        if item and hasattr(item, "get"):
            await _check_instituicao_territory(item.get("instituicao_id"), user, db)
        try:
            return await service.cancel_record(record_id, user.get("user_id"), data.get("motivo"))
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return router
