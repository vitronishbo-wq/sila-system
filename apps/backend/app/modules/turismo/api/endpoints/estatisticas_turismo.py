from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/estatisticas-turismo", tags=["Turismo - EstatisticasTurismo"])


@router.get("/")
async def listar_estatisticas_turismo() -> list[dict[str, str]]:
    return []
