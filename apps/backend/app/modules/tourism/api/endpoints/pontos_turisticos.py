from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/pontos-turisticos", tags=["Turismo - PontosTuristicos"])


@router.get("/")
async def listar_pontos_turisticos() -> list[dict[str, str]]:
    return []
