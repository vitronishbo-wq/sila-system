from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/agencias-viagens", tags=["Turismo - AgenciasViagens"])


@router.get("/")
async def listar_agencias_viagens() -> list[dict[str, str]]:
    return []
