# apps/backend/main.py
"""
SILA-System Backend – main.py (Versão 2025 – LIMPA E FUNCIONAL)
"""

import os
from pathlib import Path
from datetime import datetime, timezone
import logging

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

# ============================
# CARREGAMENTO DO .env
# ============================
backend_dir = Path(__file__).parent
project_root = backend_dir.parent.parent  # ~/dev/sila-system

env_path = project_root / ".env.development"
env_backup = backend_dir / ".env.development"

if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(env_path)
    print(f"[OK] Carregando configuração de: {env_path}")
elif env_backup.exists():
    from dotenv import load_dotenv
    load_dotenv(env_backup)
    print(f"[OK] Carregando configuração de: {env_backup}")

# ============================
# CONFIGURAÇÕES
# ============================
try:
    from config.settings import settings
except ImportError:
    print("Aviso: config.settings não encontrado → usando fallback")
    from pydantic import BaseSettings

    class Settings(BaseSettings):
        PROJECT_NAME: str = "SILA-System"
        VERSION: str = "1.0.0"
        ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
        DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
        LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        BACKEND_CORS_ORIGINS: list[str] = [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
            "http://localhost:8000",
            "http://172.31.59.209:5173",
        ]

        class Config:
            env_file = ".env.development"
            env_file_encoding = "utf-8"

    settings = Settings()

# ============================
# LOGGING
# ============================
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("sila-backend")

# ============================
# APP
# ============================
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Sistema Integrado Local de Administração",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    debug=settings.DEBUG,
)

# ============================
# MIDDLEWARES
# ============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.ENVIRONMENT == "production":
    from fastapi.middleware.trustedhost import TrustedHostMiddleware
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1"])

# ============================
# ENDPOINTS RAIZ
# ============================
@app.get("/", tags=["System"])
async def root():
    return {
        "message": "Bem-vindo ao SILA System API",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}

# ============================
# REGISTRO AUTOMÁTICO DE ROTAS (SEM DUPLICAÇÃO!)
# ============================
logger.info("\n" + "="*60)
logger.info("INICIANDO REGISTRO DE ROTAS DOS MÓDULOS")
logger.info("="*60)

MODULES = [
    ("auth",         "Auth"),
    ("dashboard",    "Dashboard"),
    ("identity",     "Identity"),
    ("documents",    "Documents"),
    ("service_hub",  "Service Hub"),
    ("notifications","Notifications"),
    ("citizenship",  "Citizenship"),
    ("justice",      "Justice"),
    ("registry",     "Registry"),
    ("reports",      "Reports"),
    ("health",       "Health"),
    ("location",     "Location"),
    ("statistics",   "Statistics"),
    ("urbanism",     "Urbanism"),
    ("sanitation",   "Sanitation"),
    ("education",    "Education"),
    ("governance",   "Governance"),
    ("integration",  "Integration"),
    ("complaints",   "Complaints"),
    ("commercial",   "Commercial"),
    ("appointments", "Appointments"),
    ("internal",     "Internal"),
]

for module_name, tag in MODULES:
    try:
        module = __import__(f"modules.{module_name}.endpoints.router", fromlist=["router"])
        router = module.router
        prefix = f"/api/v1/{module_name.replace('_', '-')}"
        app.include_router(router, prefix=prefix, tags=[tag])
        logger.info(f"Registered {tag} router → {prefix}")
    except ImportError as e:
        logger.warning(f"Warning {tag} router não encontrado: {e}")

logger.info("\n" + "="*60)
logger.info("REGISTRO DE ROTAS CONCLUÍDO")
logger.info("="*60 + "\n")

# ============================
# TRATAMENTO DE ERROS
# ============================
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Erro de validação", "errors": jsonable_encoder(exc.errors())},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Erro não tratado: {exc}", exc_info=True)
    detail = str(exc) if settings.DEBUG else "Erro interno do servidor"
    return JSONResponse(status_code=500, content={"detail": detail})

# ============================
# EXECUÇÃO DIRETA
# ============================
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )