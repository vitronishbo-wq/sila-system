from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/rastreabilidade", tags=["Pescas Industriais - Rastreabilidade"])


@router.get("/")
async def listar_rastreabilidade() -> list[dict[str, str]]:
    return []
