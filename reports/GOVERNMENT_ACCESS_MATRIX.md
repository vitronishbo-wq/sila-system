**ESTADO REAL**

- **Routers efetivamente montados**: auto-discovery e inclusão centralizada em [apps/backend/app/main.py](apps/backend/app/main.py#L1-L260) e [apps/backend/app/api/router.py](apps/backend/app/api/router.py#L1-L54). Routers de módulos encontrados (exemplos):
  - apps/backend/app/modules/educacao/api/router.py
  - apps/backend/app/modules/saude/api/router.py
  - apps/backend/app/modules/registo-civil/api/router.py
  - apps/backend/app/modules/payment/api/router.py
  - apps/backend/app/modules/tourism/api/router.py
  - apps/backend/app/modules/wallet/router.py
  - apps/backend/app/modules/notifications/router.py
  (lista parcial; discovery report em runtime: `discover_and_register_routers` – ver [apps/backend/app/main.py](apps/backend/app/main.py#L200-L230)).

- **Roles efetivamente existentes**: `UserRole` e enums definidos em [apps/backend/app/core/constants.py](apps/backend/app/core/constants.py#L29-L54) e mapeamentos por módulo em `governance.py` / `rbac/roles.py` (ex.: [apps/backend/app/modules/educacao/rbac/roles.py](apps/backend/app/modules/educacao/rbac/roles.py#L1-L62), [apps/backend/app/modules/saude/governance.py](apps/backend/app/modules/saude/governance.py#L1-L40)).

- **Permissões efetivamente aplicadas**: existe `PERMISSIONS_MATRIX` e `PermissionAction` em [apps/backend/app/core/constants.py](apps/backend/app/core/constants.py#L100-L120) que define matrizes por role. No entanto, não localizei chamadas generalizadas que apliquem automaticamente essa matriz a endpoints (poucas referências diretas). Resultado: definição SIM; aplicação transversal aos endpoints — PARCIAL.

- **Middlewares efetivamente ativos**: registrados em startup ([apps/backend/app/main.py](apps/backend/app/main.py#L120-L170)): `TrustEvaluationMiddleware`, `ObservabilityMiddleware`, `ASGIMetricsMiddleware`, `IdempotencyMiddleware` (opcional) e `setup_audit_middleware(app)` quando habilitado. Também existem middlewares de observability específicos por módulo (ex.: [apps/backend/app/modules/educacao/foundation/observability/middleware.py](apps/backend/app/modules/educacao/foundation/observability/middleware.py#L1-L84)).

- **Guards/Dependencies executados**: implementações de verificação territorial e admin existem em [apps/backend/app/core/rbac/territorial_access.py](apps/backend/app/core/rbac/territorial_access.py#L1-L183) e são exportadas via [apps/backend/app/core/rbac/__init__.py](apps/backend/app/core/rbac/__init__.py#L1-L27) (`require_territorial_access`, `verify_territorial_access`, `require_admin`). Porém não há evidência de uso consistente (ex.: `Depends(require_territorial_access(...))`) em todos os routers — ver nota abaixo.

- **Escopos territoriais efetivamente validados**: existe infra para hierarquia territorial (closure table) e helpers (`verify_same_territory_or_child`, `require_territorial_access`) — ver [apps/backend/app/core/rbac/territorial_access.py](apps/backend/app/core/rbac/territorial_access.py#L1-L183) e tipos em [apps/backend/app/core/constants.py](apps/backend/app/core/constants.py#L120-L140). Contudo, uso operacional nos endpoints é irregular: muitas rotinas e repositórios aceitam `municipio`/`provincia` como filtro (ex.: módulos de `tourism`, `educacao`), mas não há prova automática de que o `territory_id` do usuário seja aplicado automaticamente em todas as rotas.

-- Resposta direta (per item):

- `Existe no código?` — Routers: SIM; Roles: SIM; Permissões (definição): SIM; Permissões (aplicação uniforme): NÃO/Parcial; Middlewares: SIM; Guards (implementação): SIM; Guards (uso consistente): NÃO/Parcial; Territorial enforcement (infra): SIM; Territorial enforcement (endpoints aplicados): NÃO/Parcial.

**ESTADO ALVO FUTURO (resumido)**

- Objetivo: `MISSÃO: GOVERNMENT ACCESS GOVERNANCE` — ter para cada módulo uma MATRIZ (por papel: `cidadão`, `operador municipal`, `gestor municipal`, `operador provincial`, `gestor provincial`, `operador nacional`, `gestor nacional`, `super admin`) com ações (`leitura`,`criação`,`atualização`,`aprovação`,`administração`) e com enforcement automático por dependency (`require_territorial_access`) ou middleware.
- Espera-se também que para TODOS os endpoints que retornam dados territoriais haja verificação automática do `territory_id` do usuário (não apenas filtros passados por query), e que `PERMISSIONS_MATRIX` seja consultada centralmente para permitir/negar ações.

---
**Evidências (links rápidos)**
- Startup & router discovery: [apps/backend/app/main.py](apps/backend/app/main.py#L1-L260)
- RBAC / territorial checks: [apps/backend/app/core/rbac/territorial_access.py](apps/backend/app/core/rbac/territorial_access.py#L1-L183)
- Roles & permissions matrix: [apps/backend/app/core/constants.py](apps/backend/app/core/constants.py#L60-L120)
- Module role mappings (exemplos): [apps/backend/app/modules/educacao/rbac/roles.py](apps/backend/app/modules/educacao/rbac/roles.py#L1-L62), [apps/backend/app/modules/saude/governance.py](apps/backend/app/modules/saude/governance.py#L1-L40)

**Observação final**: inventário realizado apenas lendo artefactos de código — não alterei nenhum ficheiro do código, nem criei roles/permissões.
