from __future__ import annotations
from fastapi import APIRouter
router = APIRouter(prefix='/eventos', tags=['Turismo - Eventos'])

@router.get('/')
async def listar_eventos() -> list[dict[str, str]]:
    return []