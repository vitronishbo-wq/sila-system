from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/resorts", tags=["Turismo - Resorts"])


@router.get("/")
async def listar_resorts() -> list[dict[str, str]]:
    return []
