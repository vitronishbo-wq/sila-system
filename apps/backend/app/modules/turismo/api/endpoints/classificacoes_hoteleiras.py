from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/classificacoes-hoteleiras", tags=["Turismo - ClassificacoesHoteleiras"])


@router.get("/")
async def listar_classificacoes_hoteleiras() -> list[dict[str, str]]:
    return []
