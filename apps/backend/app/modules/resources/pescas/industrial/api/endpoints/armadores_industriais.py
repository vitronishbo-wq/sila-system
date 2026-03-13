from __future__ import annotations
from fastapi import APIRouter
router = APIRouter(prefix='/armadores-industriais', tags=['Pescas Industriais - ArmadoresIndustriais'])

@router.get('/')
async def listar_armadores_industriais() -> list[dict[str, str]]:
    return []