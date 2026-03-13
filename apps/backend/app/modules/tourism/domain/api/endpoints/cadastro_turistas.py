from __future__ import annotations
from fastapi import APIRouter
router = APIRouter(prefix='/cadastro-turistas', tags=['Turismo - CadastroTuristas'])

@router.get('/')
async def listar_cadastro_turistas() -> list[dict[str, str]]:
    return []