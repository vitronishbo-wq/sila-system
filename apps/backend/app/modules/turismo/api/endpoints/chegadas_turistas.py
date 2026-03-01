from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/chegadas-turistas", tags=["Turismo - ChegadasTuristas"])


@router.get("/")
async def listar_chegadas_turistas() -> list[dict[str, str]]:
    return []
