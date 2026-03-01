from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/pousadas", tags=["Turismo - Pousadas"])


@router.get("/")
async def listar_pousadas() -> list[dict[str, str]]:
    return []
