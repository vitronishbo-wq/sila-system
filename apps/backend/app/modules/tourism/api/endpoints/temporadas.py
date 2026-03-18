from __future__ import annotations
from fastapi import APIRouter
router = APIRouter(prefix='/temporadas', tags=['Turismo - Temporadas'])

@router.get('/')
async def listar_temporadas() -> list[dict[str, str]]:
    return []