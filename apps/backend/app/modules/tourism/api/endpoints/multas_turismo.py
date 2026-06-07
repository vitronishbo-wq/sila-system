from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/multas-turismo", tags=["Turismo - MultasTurismo"])


@router.get("/")
async def listar_multas_turismo() -> list[dict[str, str]]:
    return []
