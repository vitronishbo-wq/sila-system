from __future__ import annotations
from fastapi import APIRouter
router = APIRouter(prefix='/autos-infracao-turismo', tags=['Turismo - AutosInfracaoTurismo'])

@router.get('/')
async def listar_autos_infracao_turismo() -> list[dict[str, str]]:
    return []