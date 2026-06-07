# /opt/sila-system/backend/main.py

import sys
from pathlib import Path

from fastapi import FastAPI

# Adiciona o diretório raiz do projeto ao path para importar a configuração
# Assume que a configuração está em /opt/sila-system/core/config.py
sys.path.append(str(Path(__file__).parent.parent))

# Importa a configuração (que contém as chaves BNA, etc.)
from core.config import settings

# --- APLICAÇÃO FASTAPI PRINCIPAL ---
app = FastAPI(
    title="SILA System API",
    version="2.0",
    description="Orquestrador Ultra-Avançado para Análise e Automação de Código.",
    debug=settings.DEBUG,
)


# --- ROTA DE SAÚDE (HEALTH CHECK) ---
@app.get("/health")
def health_check():
    """Endpoint para verificar o status operacional da API."""
    # Garante que a configuração BNA está carregada (Teste Rápido)
    bna_key_status = "Loaded" if settings.BNA_API_KEY else "Missing"

    return {
        "status": "operational",
        "api_version": app.version,
        "environment": settings.ENVIRONMENT,
        "bna_config": bna_key_status,
    }


# --- INCLUSÃO DE ROTAS DE MÓDULOS ---
# Aqui é onde você incluiria os routers de outros módulos (ex: auth, analytics)
# from apps.backend.app.modules.auth.router import auth_router
# app.include_router(auth_router, prefix="/v1/auth", tags=["Auth"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
