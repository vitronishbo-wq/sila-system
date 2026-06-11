# Auditoria Executável — Acesso Governamental (Compacto)

**STATUS_ATUAL**
- total_endpoints: 1553
- endpoints_with_auth: 83 (≈5.3%)
- endpoints_with_permission: 45 (≈2.9%)
- endpoints_with_territorial: 70 (≈4.5%)
- Observação: `PolicyEngine.authorize()` aplica comportamento permissivo quando não existe policy registada — risco de exposição.

**ROLE**
- admin_super
- admin_central
- admin_provincial
- admin_municipal
- admin_communal
- citizen

**ESCOPOS**
- Serviços essenciais (códigos): BI, RC, SA, ED, AS, EN, EM, MO, TR, NO, LI, NIF
- Serviços centrais: doc_validation, service_mgmt

**MÓDULOS_VISÍVEIS** (exemplos — módulos com endpoints públicos/sem proteção detectada)
- api/router.py
- telecomunicacoes/api/health.py
- industry/api/endpoints/estabelecimentos_industriais.py
- identity/api/endpoints/biometrics.py
- educacao/api/endpoints/academic_identity.py

**MÓDULOS_BLOQUEADOS** (exemplos)
- wallet/router.py — auth_ratio: 1.0
- notifications/router.py — auth_ratio: 1.0
- economy/taxpayer/api/router.py — auth_ratio: 0.462
- educacao/api/endpoints/wizard_matricula.py — auth_ratio: 1.0

**CASOS (A → G) — PASSA / FALHA**
- CASO_A — Administrador Nacional: PASSA
  - Motivo: suporte para níveis centrais/super e políticas/helpers existem no código.
- CASO_B — Administrador Provincial (Huambo): FALHA
  - Motivo: grande número de endpoints nacionais sem restrição territorial (ex.: 1356 sem proteção detectada).
- CASO_C — Administrador Municipal (Caála): FALHA
  - Motivo: mesma razão que CASO_B.
- CASO_D — Diretor Escola: FALHA
  - Motivo: endpoints da área de Educação sem proteção detectados (≈69).
- CASO_E — Funcionário Escola: FALHA
  - Motivo: idem CASO_D.
- CASO_F — Técnico Assistência Social: FALHA
  - Motivo: endpoints de saúde/assistência sem restrições (ex.: `/ping`).
- CASO_G — Cidadão: FALHA
  - Motivo: muitos endpoints públicos e operações sensíveis expostas.

**TOP-50 (detalhes)**
- Ver tabela completa: [reports/TOP50_ACCESS_REVIEW.md](reports/TOP50_ACCESS_REVIEW.md)
- Ver snapshot detalhado (JSON): [reports/GOV_ACCESS_SNAPSHOT.json](reports/GOV_ACCESS_SNAPSHOT.json)

---
Observação: os componentes de RBAC e territorialidade existem em código (ver `apps/backend/app/core/constants.py`, `apps/backend/core/auth/policies/policy_engine.py`, `apps/backend/core/auth/guards/permission_guard.py`, `apps/backend/app/core/rbac/territorial_access.py`), porém a aplicação dos guards é inconsistente. Priorizar correções nos endpoints listados no TOP-50 e endurecer default do PolicyEngine.
