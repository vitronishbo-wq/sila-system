from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/fluxo-turistico", tags=["Turismo - FluxoTuristico"])


@router.get("/")
async def listar_fluxo_turistico() -> list[dict[str, str]]:
    return []
