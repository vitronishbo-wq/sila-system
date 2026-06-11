**ESTADO REAL**

- **Resumo executável**: O projeto possui infra RBAC, enums de roles, `PERMISSIONS_MATRIX`, helpers de verificação territorial e discovery de routers. Contudo a aplicação consistente desses elementos aos endpoints não foi encontrada — portanto há gaps entre definição e enforcement.

**Gaps identificados**
- Definição vs Aplicação: `PERMISSIONS_MATRIX` existe ([apps/backend/app/core/constants.py](apps/backend/app/core/constants.py#L100-L120)) mas não há aplicação transversal visível nos routers.
- Dependências territoriais: `require_territorial_access` existe ([apps/backend/app/core/rbac/territorial_access.py](apps/backend/app/core/rbac/territorial_access.py#L1-L183)) mas uso em endpoints é irregular.
- Casos de demonstração sem integrações: integrações externas (AGT, Multicaixa, bancos, ministérios) estão referenciadas e suportadas por `ProviderRegistry` e `provider_router` — há suporte a mock/homologação (ver [apps/backend/app/platform/integration/provider_router.py](apps/backend/app/platform/integration/provider_router.py#L1-L155) e [apps/backend/app/platform/integration/provider_registry.py](apps/backend/app/platform/integration/provider_registry.py#L1-L200)).

**HOMOLOGAÇÃO INTERNA — integrações que bloqueiam produção mas NÃO devem bloquear demonstração**

- AGT
  - Integração em código: SIM (config: `AGT_BASE_URL`, provider registry entries) — ver [apps/backend/app/core/settings.py](apps/backend/app/core/settings.py#L100-L110) e [apps/backend/app/platform/integration/provider_registry.py](apps/backend/app/platform/integration/provider_registry.py#L120-L123).
  - Produção: geralmente SIM (exige credenciais e endpoints reais).
  - Homologação Interna (estratégias aceites): sandbox, mock, homologação. ProviderRegistry suporta `MOCK_LIVE` / `HOMOLOGATION` statuses.

- Multicaixa
  - Integração em código: SIM (`MULTICAIXA_BASE_URL` e provider registry) — ver [apps/backend/app/core/settings.py](apps/backend/app/core/settings.py#L100-L107) e provider registry.
  - Produção: SIM.
  - Homologação Interna: mock, sandbox, simulador — o projeto já contém telas/fluxos que referenciam Multicaixa no frontend (ex.: `apps/frontend/.../PaymentModal.tsx`).

- Bancos (recebíveis / comprovativos)
  - Integração: modelos suportam `provider` e receipts; podem ser simulados em demo.
  - Homologação Interna: mock / provider local / simulador.

- Ministérios externos / serviços nacionais (X-Road, Registo Civil, BI)
  - Integração: referências e providers estão previstos (`xroad_bi`, `registo_civil`, etc.).
  - Homologação Interna: sandbox / homologação institucional / mock.

**Estratégia recomendada por integração**
- Priorizar `ProviderRegistry` mocks para demonstrações (status `MOCK_LIVE`), usar `HOMOLOGATION` quando disponível para testes integrados, e manter `REAL` apenas em produção. Ferramentas úteis já no repositório: scripts de homologação (`scripts/homologation_institucional.py`) e `provider_router` com endpoints de evidência.

**Resultado final — Classificação (estado real)**
- **ACESSO_GOVERNAMENTAL**: PARCIAL  
  - Racional: modelos e roles existem, mas aplicação uniforme de autorização aos endpoints está incompleta.
- **TERRITORIALIDADE**: PARCIAL  
  - Racional: infra de territorialidade presente; enforcement inconsistente.
- **PRONTIDÃO_DEMO**: OK_COM_RESSALVAS  
  - Racional: `ProviderRegistry` e config permitem mocks/sandbox; demonstração factível com provisões de mock.
- **RISCO_EXECUTIVO**: MÉDIO  
  - Racional: dados sensíveis podem ser acedidos incorretamente se endpoints não aplicarem verificações territoriais/permissões.

**Ações de curto prazo (prioritárias)**
1. Fazer um sweep automatizado/semiautomático para identificar endpoints que retornam dados territoriais e aplicar `Depends(require_territorial_access(...))` onde falta.  
2. Introduzir um middleware/dep central que consulte `PERMISSIONS_MATRIX` em operações sensíveis (create/update/approve/admin) para uniformizar aplicação de permissões.  
3. Preparar um playbook de demonstração usando `ProviderRegistry` para colocar `multicaixa` e `agt` em `MOCK_LIVE` ou `HOMOLOGATION` para garantir que a demo não dependa de integrações externas.

**Evidências & links**
- Provider router / promotable statuses: [apps/backend/app/platform/integration/provider_router.py](apps/backend/app/platform/integration/provider_router.py#L1-L155)
- Provider registry entries (multicaixa, agt): [apps/backend/app/platform/integration/provider_registry.py](apps/backend/app/platform/integration/provider_registry.py#L120-L123)
- Configurações: [apps/backend/app/core/settings.py](apps/backend/app/core/settings.py#L100-L110)
