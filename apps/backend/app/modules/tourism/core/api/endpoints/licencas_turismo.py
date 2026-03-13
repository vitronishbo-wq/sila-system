from __future__ import annotations
from fastapi import APIRouter
router = APIRouter(prefix='/licencas-turismo', tags=['Turismo - LicencasTurismo'])

@router.get('/')
async def listar_licencas_turismo() -> list[dict[str, str]]:
    return []