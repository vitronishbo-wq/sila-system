from __future__ import annotations
from fastapi import APIRouter
router = APIRouter(prefix='/certificacoes', tags=['Pescas Industriais - Certificacoes'])

@router.get('/')
async def listar_certificacoes() -> list[dict[str, str]]:
    return []