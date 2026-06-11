from fastapi import APIRouter

from apps.backend.app.modules.educacao.rbac.admin_router import router as admin_router

router = APIRouter()
router.include_router(admin_router, prefix="/educacao/admin", tags=["educacao-admin"])
from fastapi import APIRouter

from apps.backend.app.modules.educacao.api.endpoints import (
    academic_identity_router,
    academic_wallet_router,
    boletins_router,
    certificados_router,
    concursos_router,
    emprego_router,
    emis_router,
    escolas_router,
    formacoes_router,
    fuc_router,
    inscricoes_router,
    marketplace_router,
    matricula_router,
    metrics_router,
    propinas_router,
    transfer_wizard_router,
    transferencias_router,
    transferencias_automacao_router,
    turmas_router,
    universidade_router,
    wizard_matricula_router,
)
from apps.backend.app.modules.educacao.api.vacancies_router import router as vacancies_router
from apps.backend.app.modules.educacao.marketplace.router import router as marketplace_aggregator_router

router = APIRouter(prefix="", tags=["Educacao"])

# ── Servicos canonicos (orientados ao cidadao) ──
router.include_router(wizard_matricula_router)
router.include_router(transfer_wizard_router)

# ── Identidade Educacional Nacional (FASE 3.2E) ──
router.include_router(academic_identity_router)
router.include_router(academic_wallet_router)

# ── Servicos legados (preservados para compatibilidade) ──
router.include_router(matricula_router)
router.include_router(inscricoes_router)
router.include_router(transferencias_router)
router.include_router(certificados_router)

# ── Workflow endpoints (subfluxos internos) ──
router.include_router(boletins_router)
router.include_router(transferencias_automacao_router)
router.include_router(propinas_router)
router.include_router(emprego_router)
router.include_router(concursos_router)
router.include_router(formacoes_router)
router.include_router(universidade_router)
router.include_router(vacancies_router)
router.include_router(metrics_router)
router.include_router(marketplace_router)
router.include_router(marketplace_aggregator_router)
router.include_router(emis_router)

# ── Cadastro de Escolas e Turmas (Fluxos 1 e 4 da demo) ──
router.include_router(escolas_router)
router.include_router(turmas_router)

# ── FUC - Associacao com Educacao (Fluxo 7 da demo) ──
router.include_router(fuc_router)
