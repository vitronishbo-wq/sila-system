from __future__ import annotations
from fastapi import APIRouter
router = APIRouter(prefix='/certificacoes-turisticas', tags=['Turismo - CertificacoesTuristicas'])

@router.get('/')
async def listar_certificacoes_turisticas() -> list[dict[str, str]]:
    return []