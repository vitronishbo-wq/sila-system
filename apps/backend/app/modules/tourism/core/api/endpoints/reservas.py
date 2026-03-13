from __future__ import annotations
from fastapi import APIRouter
router = APIRouter(prefix='/reservas', tags=['Turismo - Reservas'])

@router.get('/')
async def listar_reservas() -> list[dict[str, str]]:
    return []