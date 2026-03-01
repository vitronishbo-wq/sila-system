from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/atracao-turisticas", tags=["Turismo - AtracaoTuristicas"])


@router.get("/")
async def listar_atracao_turisticas() -> list[dict[str, str]]:
    return []
