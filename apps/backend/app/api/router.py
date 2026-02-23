from fastapi import APIRouter
from app.api.public.router import public_router
from app.api.citizen.router import citizen_router
# from app.api.backoffice.router import backoffice_router # Empty for now
from app.api.admin.router import admin_router
from app.api.public.rbac_test_routes import router as rbac_router

from app.citizen.api.router import router as fuc_router
from app.citizen.api.public_router import router as citizen_public_router
from app.presentation.api.citizen_document_routes import router as citizen_documents_router
from app.modules.financas.api.router import router as financas_router
from app.modules.taxpayer.api.router import router as taxpayer_router
from app.modules.identidade_civil.api.bi_routes import router as ic_bi_router
from app.modules.identidade_civil.api.atestados_routes import router as ic_atestados_router
from app.modules.identidade_civil.api.historico_routes import router as ic_historico_router
from app.modules.identidade_civil.api.validacao_routes import router as ic_validacao_router
from app.modules.identidade_civil.api.citizens.citizens_routes import router as ic_citizens_router
from app.modules.identidade_civil.api.documents.documents_routes import router as ic_documents_router
from app.modules.registo_civil.api.router import router as registo_civil_router
# from app.modules.saude_primaria.api.router import router as saude_primaria_router  # Disabled pending deps
from app.modules.service_requests.api.router import router as service_requests_router
from app.api.debug.routes import router as debug_router

api_router = APIRouter()

# Public Channel (Auth, Health) - Root level access
api_router.include_router(public_router)
api_router.include_router(rbac_router)  # RBAC testing endpoints
api_router.include_router(debug_router)

# Citizen Channel
api_router.include_router(citizen_router, prefix="/citizen")
api_router.include_router(citizen_public_router)  # Has its own /citizen prefix
api_router.include_router(citizen_documents_router)  # Documentos, Atestados, Faturas, Solicitações

# Backoffice Channel
# api_router.include_router(backoffice_router, prefix="/backoffice")

# Admin Channel
api_router.include_router(admin_router, prefix="/admin")

# FUC (Ficha Única do Cidadão) - Citizen Data Projection & Events
api_router.include_router(fuc_router, prefix="/v1/identidade-civil/citizens", tags=["Identidade Civil"])
api_router.include_router(financas_router, prefix="/v1/financas", tags=["Financas"])
api_router.include_router(taxpayer_router, prefix="/v1/agt", tags=["Taxpayer"])

# Identidade Civil - Ciclo de Vida do BI e Atestados
api_router.include_router(ic_bi_router, prefix="/v1", tags=["Identidade Civil"])
api_router.include_router(ic_atestados_router, prefix="/v1", tags=["Identidade Civil"])
api_router.include_router(ic_historico_router, prefix="/v1", tags=["Identidade Civil"])
api_router.include_router(ic_validacao_router, prefix="/v1", tags=["Identidade Civil"])

# Identidade Civil - CRUD de Cidadãos e Documentos
api_router.include_router(ic_citizens_router, prefix="/v1/identidade-civil", tags=["Identidade Civil"])
api_router.include_router(ic_documents_router, prefix="/v1/identidade-civil", tags=["Identidade Civil"])

# Compatibility mounts: some clients/tests expect the shorter `/v1/identidade` prefix
api_router.include_router(ic_citizens_router, prefix="/v1/identidade", tags=["Identidade Civil"])
api_router.include_router(ic_documents_router, prefix="/v1/identidade", tags=["Identidade Civil"])

# Registo Civil - Nascimento, Casamento, Óbito
api_router.include_router(registo_civil_router, prefix="/v1/registo-civil", tags=["Registo Civil"])

# Saúde Primária - Disabled pending dependencies
# api_router.include_router(saude_primaria_router, prefix="/v1/saude", tags=["Saude Primaria"])

# Service Requests - Pedidos de Serviço
api_router.include_router(service_requests_router, prefix="/v1", tags=["Service Requests"])




