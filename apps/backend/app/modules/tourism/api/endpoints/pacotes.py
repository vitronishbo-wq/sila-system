from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/pacotes", tags=["Turismo - Pacotes"])


@router.get("/")
async def listar_pacotes() -> list[dict[str, str]]:
    return []
