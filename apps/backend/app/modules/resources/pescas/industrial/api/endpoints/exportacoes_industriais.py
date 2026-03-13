from __future__ import annotations
from fastapi import APIRouter
router = APIRouter(prefix='/exportacoes-industriais', tags=['Pescas Industriais - ExportacoesIndustriais'])

@router.get('/')
async def listar_exportacoes_industriais() -> list[dict[str, str]]:
    return []