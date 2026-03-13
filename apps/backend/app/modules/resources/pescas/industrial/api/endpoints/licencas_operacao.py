from __future__ import annotations
from fastapi import APIRouter
router = APIRouter(prefix='/licencas-operacao', tags=['Pescas Industriais - LicencasOperacao'])

@router.get('/')
async def listar_licencas_operacao() -> list[dict[str, str]]:
    return []