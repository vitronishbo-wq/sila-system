from __future__ import annotations
from fastapi import APIRouter
router = APIRouter(prefix='/embarcacoes-industriais', tags=['Pescas Industriais - EmbarcacoesIndustriais'])

@router.get('/')
async def listar_embarcacoes_industriais() -> list[dict[str, str]]:
    return []