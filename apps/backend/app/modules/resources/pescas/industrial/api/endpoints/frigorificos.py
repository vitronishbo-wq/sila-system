from __future__ import annotations
from fastapi import APIRouter
router = APIRouter(prefix='/frigorificos', tags=['Pescas Industriais - Frigorificos'])

@router.get('/')
async def listar_frigorificos() -> list[dict[str, str]]:
    return []