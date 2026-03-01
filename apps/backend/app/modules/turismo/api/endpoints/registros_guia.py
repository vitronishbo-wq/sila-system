from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/registros-guia", tags=["Turismo - RegistrosGuia"])


@router.get("/")
async def listar_registros_guia() -> list[dict[str, str]]:
    return []
