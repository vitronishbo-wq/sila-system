from __future__ import annotations
from fastapi import APIRouter
router = APIRouter(prefix='/guias-turismo', tags=['Turismo - GuiasTurismo'])

@router.get('/')
async def listar_guias_turismo() -> list[dict[str, str]]:
    return []