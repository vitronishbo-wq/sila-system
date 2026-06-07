from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/receitas-turisticas", tags=["Turismo - ReceitasTuristicas"])


@router.get("/")
async def listar_receitas_turisticas() -> list[dict[str, str]]:
    return []
