from __future__ import annotations
from fastapi import APIRouter
router = APIRouter(prefix='/cadastur', tags=['Turismo - Cadastur'])

@router.get('/')
async def listar_cadastur() -> list[dict[str, str]]:
    return []