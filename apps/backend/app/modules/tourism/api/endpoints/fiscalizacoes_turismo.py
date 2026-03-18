from __future__ import annotations
from fastapi import APIRouter
router = APIRouter(prefix='/fiscalizacoes-turismo', tags=['Turismo - FiscalizacoesTurismo'])

@router.get('/')
async def listar_fiscalizacoes_turismo() -> list[dict[str, str]]:
    return []