from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/avaliacoes", tags=["Turismo - Avaliacoes"])


@router.get("/")
async def listar_avaliacoes() -> list[dict[str, str]]:
    return []
