from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/operadores-turisticos", tags=["Turismo - OperadoresTuristicos"])


@router.get("/")
async def listar_operadores_turisticos() -> list[dict[str, str]]:
    return []
