from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/reclamacoes-turismo", tags=["Turismo - ReclamacoesTurismo"])


@router.get("/")
async def listar_reclamacoes_turismo() -> list[dict[str, str]]:
    return []
