from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/roteiros", tags=["Turismo - Roteiros"])


@router.get("/")
async def listar_roteiros() -> list[dict[str, str]]:
    return []
