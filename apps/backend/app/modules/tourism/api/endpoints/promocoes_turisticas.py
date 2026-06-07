from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/promocoes-turisticas", tags=["Turismo - PromocoesTuristicas"])


@router.get("/")
async def listar_promocoes_turisticas() -> list[dict[str, str]]:
    return []
