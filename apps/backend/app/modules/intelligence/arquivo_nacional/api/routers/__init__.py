"""Routers FastAPI para API do módulo arquivo_nacional."""

from fastapi import APIRouter

from .documento_router import router as documento_router
from .plano_classificacao_router import router as plano_classificacao_router
from .processo_router import router as processo_router
from .tabela_temporalidade_router import router as tabela_temporalidade_router

router = APIRouter(prefix="/arquivo-nacional", tags=["Arquivo Nacional"])
router.include_router(documento_router, prefix="/documentos", tags=["Documentos"])
router.include_router(processo_router, prefix="/processos", tags=["Processos"])
router.include_router(
    plano_classificacao_router, prefix="/planos-classificacao", tags=["Planos de Classificação"]
)
router.include_router(
    tabela_temporalidade_router, prefix="/tabelas-temporalidade", tags=["Tabelas de Temporalidade"]
)
__all__ = ["router"]
