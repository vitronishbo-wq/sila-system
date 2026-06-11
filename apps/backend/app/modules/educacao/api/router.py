
from fastapi import APIRouter

from apps.backend.app.modules.educacao.api.endpoints.academic_identity import router as academic_identity_router
from apps.backend.app.modules.educacao.api.endpoints.academic_wallet import router as academic_wallet_router
from apps.backend.app.modules.educacao.api.endpoints.boletins import router as boletins_router
from apps.backend.app.modules.educacao.api.endpoints.certificados import router as certificados_router
from apps.backend.app.modules.educacao.api.endpoints.concursos import router as concursos_router
from apps.backend.app.modules.educacao.api.endpoints.emprego import router as emprego_router
from apps.backend.app.modules.educacao.emis.api.endpoints import router as emis_router
from apps.backend.app.modules.educacao.api.endpoints.escolas_routes import router as escolas_router
from apps.backend.app.modules.educacao.api.endpoints.formacoes import router as formacoes_router
from apps.backend.app.modules.educacao.api.endpoints.fuc_routes import router as fuc_router
from apps.backend.app.modules.educacao.api.endpoints.inscricoes import router as inscricoes_router
from apps.backend.app.modules.educacao.api.endpoints.marketplace_endpoints import router as marketplace_router
from apps.backend.app.modules.educacao.api.endpoints.matricula_routes import router as matricula_router
from apps.backend.app.modules.educacao.api.endpoints.metrics_endpoints import router as metrics_router
from apps.backend.app.modules.educacao.api.endpoints.propinas import router as propinas_router
from apps.backend.app.modules.educacao.api.endpoints.transfer_wizard import router as transfer_wizard_router
from apps.backend.app.modules.educacao.api.endpoints.transferencias import router as transferencias_router
from apps.backend.app.modules.educacao.api.endpoints.transferencias_automacao import router as transferencias_automacao_router
from apps.backend.app.modules.educacao.api.endpoints.turmas_routes import router as turmas_router
from apps.backend.app.modules.educacao.api.endpoints.universidade import router as universidade_router
from apps.backend.app.modules.educacao.api.endpoints.wizard_matricula import router as wizard_matricula_router
from apps.backend.app.modules.educacao.api.vacancies_router import router as vacancies_router
from apps.backend.app.modules.educacao.marketplace.router import router as marketplace_aggregator_router
from apps.backend.app.modules.educacao.rbac.admin_router import router as admin_router


router = APIRouter(prefix="", tags=["Educacao"])

# Administrative routes
router.include_router(admin_router, prefix="/educacao/admin", tags=["educacao-admin"])

# Canonical services (citizen-oriented)
router.include_router(wizard_matricula_router)
router.include_router(transfer_wizard_router)

# National Educational Identity (PHASE 3.2E)
router.include_router(academic_identity_router)
router.include_router(academic_wallet_router)

# Legacy services (preserved for compatibility)
router.include_router(matricula_router)
router.include_router(inscricoes_router)
router.include_router(transferencias_router)
router.include_router(certificados_router)

# Internal sub-workflows
router.include_router(boletins_router)
router.include_router(transferencias_automacao_router)
router.include_router(propinas_router)
router.include_router(emprego_router)
router.include_router(concursos_router)
router.include_router(formacoes_router)
router.include_router(universidade_router)

# Marketplace and related services
router.include_router(vacancies_router)
router.include_router(metrics_router)
router.include_router(marketplace_router)
router.include_router(marketplace_aggregator_router)
router.include_router(emis_router)

# School and Class registration (Demo flows 1 and 4)
router.include_router(escolas_router)
router.include_router(turmas_router)

# FUC - Association with Education (Demo flow 7)
router.include_router(fuc_router)
