from __future__ import annotations
from fastapi import APIRouter
router = APIRouter(prefix='/ocupacao-hoteleira', tags=['Turismo - OcupacaoHoteleira'])

@router.get('/')
async def listar_ocupacao_hoteleira() -> list[dict[str, str]]:
    return []