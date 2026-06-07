from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/estatisticas", tags=["Pescas Industriais - Estatisticas"])


@router.get("/")
async def listar_estatisticas() -> list[dict[str, str]]:
    return []
