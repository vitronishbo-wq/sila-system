"""Citizenship router - Endpoints para Atualização de BI."""

from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Ajustado para o caminho centralizado que estamos a usar
from config.database import get_db
from modules.identity.models.user import User
from modules.citizenship.models.atualizacao_bi import AtualizacaoBI, AtualizacaoBIDocument

router = APIRouter(tags=["Citizenship"])

@router.get("/ping")
async def ping():
    return {"status": "citizenship ok", "message": "Módulo de Cidadania funcionando!"}

@router.get("/requests")
async def list_requests(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(AtualizacaoBI).order_by(AtualizacaoBI.data_criacao.desc())
    )
    requests = result.scalars().all()
    return [
        {
            "id": req.id,
            "nome_completo": req.nome_completo,
            "numero_documento": req.numero_documento,
            "status": req.status,
            "data_criacao": req.data_criacao.isoformat(),
        }
        for req in requests
    ]

# ... (restante do código mantido pois a lógica de negócio está correta)
