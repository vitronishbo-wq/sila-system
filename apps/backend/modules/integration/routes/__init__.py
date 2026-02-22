"""
Integration routes module.

Este módulo consolida todas as rotas de integração em um único router principal.
"""

from fastapi import APIRouter
from .a_p_i_gateway import router as api_gateway_router
from .conector_externo import router as conector_externo_router
from .sincronizacao_b_n_a import router as sincronizacao_bna_router
from .transformacao_dados import router as transformacao_dados_router

# Router principal que consolida todas as rotas de integração
router = APIRouter(tags=["Integration"])

# Incluir todas as rotas específicas
router.include_router(api_gateway_router)
router.include_router(conector_externo_router)
router.include_router(sincronizacao_bna_router)
router.include_router(transformacao_dados_router)


# Health check endpoint
@router.get("/ping")
async def ping():
    """Health check para o módulo integration"""
    return {"status": "ok", "module": "integration"}
