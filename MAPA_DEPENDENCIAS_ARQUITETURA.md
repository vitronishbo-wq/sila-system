# 🗺️ MAPA DE DEPENDÊNCIAS - SILA SYSTEM

## Situação ATUAL (Problema)

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CAOS ARQUITETURAL                            │
│                                                                      │
│  ┌──────────────┐                                                   │
│  │  /modules/   │  ← 35 módulos (Arquitetura Spaghetti)            │
│  │  (Legacy)    │                                                   │
│  └──────────────┘                                                   │
│      ↓                                                              │
│   API em models/schemas + endpoints + routes (confuso!)            │
│   Services em root/ (27 módulos)                                    │
│   Sem domain, sem application layer                                 │
│                                                                      │
│  ┌──────────────┐                                                   │
│  │ /app/modules/│  ← 8 módulos (DDD/Clean - CORRETO)               │
│  │  (Novo)      │                                                   │
│  └──────────────┘                                                   │
│      ↓                                                              │
│   API em api/ (centralizado) ✓                                      │
│   Application em application/ ✓                                     │
│   Domain isolado ✓                                                  │
│                                                                      │
│  ⚠️  PROBLEMA: 2 ARQUITETURAS COEXISTINDO!                          │
│  ⚠️  Imports confusos, duplicação, inconsistência                   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Problemas de Dependência CRÍTICOS

### 1. **Identidade Civil - 3 APIs Conflitantes**

```
identidade_civil/
│
├── api/router.py                    ← Entry Point 1
│   ├── imports de routes
│   └── registra em FastAPI
│
├── application/api/router.py        ← Entry Point 2 (CONFLITO!)
│   ├── imports de queries
│   └── registra em FastAPI
│
└── presentation/api/router.py       ← Entry Point 3 (CONFLITO!)
    ├── imports de presenters
    └── registra em FastAPI

RESULTADO:
  Rotas duplicadas? Conflito de URL? Qual prevalece?
  FastAPI confuso, endpoints funcionam parcialmente
```

---

### 2. **User Model - Import Hell**

```
modules/identity/models/user.py
  ↓
  Importado por:
    ├── app/api/deps.py (correto ✓)
    ├── app/modules/identidade_civil/api/* (correto)
    ├── app/core/iam/models/user.py (DUPLICADO ❌)
    ├── seeds/core/seed_founding_users_sql.py (correto)
    └── 30+ outros lugares

PROBLEMA:
  app/core/iam/models/user.py é um clone antigo!
  Se alguém importar de lá → Classe diferente
  Isinstance checks falham
```

---

### 3. **IAM Client - Quadruplicado**

```
app/modules/bi/integrations/iam_client.py
  ├── def get_user_by_id(...)
  ├── def verify_token(...)
  └── def get_roles(...)

app/modules/service_requests/integrations/iam_client.py
  ├── def get_user_by_id(...)        ← Implementação diferente?
  ├── def verify_token(...)          ← Retry logic diferente?
  └── def get_roles(...)             ← Cache diferente?

app/modules/statistics/integrations/iam_client.py
  └── ... (idem)

app/modules/workflow/integrations/iam_client.py
  └── ... (idem)

RESULTADO:
  Autenticação inconsistente entre módulos
  Se fix bug em um → 3 outros ficam com bug
  Impossível manutenção
```

---

### 4. **Endpoints Fragmentados**

```
┌─────────────────────────────────┐
│    FastAPI Main App             │
│  main.py                        │
└──────────────┬──────────────────┘
               │
        ┌──────┴──────────┬──────────────┬──────────────┐
        │                 │              │              │
    ┌───▼───┐         ┌──▼──┐        ┌─▼──┐         ┌─▼──┐
    │app/api│         │modu-│        │app/│         │...?│
    │router │         │les/ │        │modu│         │     │
    │(19)   │         │(69) │        │les/│         │     │
    └───────┘         └─────┘        │(22)│         └─────┘
                                     └────┘

PROBLEMA:
  - app/api/router.py inclui alguns app/modules/ endpoints
  - modules/ endpoints em 69 arquivos diferentes
  - Alguns rotas registadas 2x (em legacy + novo)
  - Confusão total no OpenAPI spec
```

---

## Situação DESEJADA (Solução)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ARQUITETURA UNIFICADA                            │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    CORE Centralizado                         │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │   │
│  │  │   Config     │  │  DB/Session  │  │  IAM Client (1) │   │   │
│  │  └──────────────┘  └──────────────┘  └─────────────────┘   │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │   │
│  │  │  Security    │  │  DI Container│  │  Event Bus (1)  │   │   │
│  │  └──────────────┘  └──────────────┘  └─────────────────┘   │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │   │
│  │  │  Logging     │  │ Exceptions   │  │  Constants      │   │   │
│  │  └──────────────┘  └──────────────┘  └─────────────────┘   │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                               ▲                                      │
│                               │ (tudo importa de core/)             │
│                               │                                      │
│  ┌────────────────────────────┴────────────────────────────────┐   │
│  │  MÓDULOS Padronizados (padrão único)                        │   │
│  │                                                              │   │
│  │  Cada módulo:                                               │   │
│  │  ├── api/router.py           ← ÚNICO entry point            │   │
│  │  ├── application/services    ← Lógica de negócio            │   │
│  │  ├── application/use_cases   ← Caso de uso                  │   │
│  │  ├── domain/models           ← Entidades                    │   │
│  │  ├── domain/repositories     ← Interfaces                   │   │
│  │  ├── infrastructure/db       ← Implementações              │   │
│  │  └── tests/                  ← Testes                       │   │
│  │                                                              │   │
│  │  Exemplo: /modules/payment/, /modules/health/, etc         │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ✅ 1 arquitetura, 1 padrão, 1 forma de fazer                       │
│  ✅ Clear imports, no duplication, predictable                      │
│  ✅ Easy to onboard, test, maintain                                 │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Fluxo de Integração Entre Módulos (Desejado)

```
┌─────────────────────────────────────────────────────────────┐
│                  Módulo: SERVICE_REQUESTS                   │
│                                                              │
│  router.py                                                   │
│    ├── POST /requests           ← user submits request      │
│    └── GET /requests/{id}                                   │
│           │                                                 │
│           ▼                                                 │
│   application/use_cases/create_request.py                  │
│           │                                                 │
│           ├─→ domain/models/Request                        │
│           ├─→ domain/repositories/RequestRepository        │
│           │           │                                     │
│           │           ▼ (implementação em infrastructure)  │
│           │   infrastructure/db/request_repository.py      │
│           │                                                 │
│           ├─→ Core/Events: EventBus.publish('RequestCreated') ← GLOBAL
│           │           │                                     │
│           │           ▼ (outro módulo escuta)             │
│           │   /modules/notifications/listeners/            │
│           │   (auto recebe evento, cria notificação)      │
│           │                                                 │
│           └─→ Core/IAM: iam_client.get_user(user_id)      ← GLOBAL
│                           │                                 │
│                           └─→ cache hit ou call externo     │
│                                                              │
│  Resultado: Modulo integrado SEM import acoplado            │
└─────────────────────────────────────────────────────────────┘
```

---

## Matriz de Dependências (ANTES vs DEPOIS)

### ❌ ANTES (Atual)

```
identidade_civil     ← 3 apis (confuso)
├── api/router
├── application/api/router
└── presentation/api/router

service_requests     ← 1 api
├── api/router
└── (tudo OK)

payment (legacy)     ← 1 api (models-based)
├── endpoints/
├── services/ (root)
└── models/

Result: 
  - 122 entry points de rotas
  - Imports circulares possíveis
  - Testing difícil
  - Manutenção = nightmare
```

### ✅ DEPOIS (Desejado)

```
identidade_civil     ← 1 api (claro)
├── api/router       ← ÚNICO
├── application/services
├── domain/models
├── infrastructure/db
└── tests/

service_requests     ← 1 api (claro)
├── api/router       ← ÚNICO
├── application/services
├── domain/models
├── infrastructure/db
└── tests/

payment              ← 1 api (claro, mesmo padrão)
├── api/router       ← ÚNICO
├── application/services
├── domain/models
├── infrastructure/db
└── tests/

Result:
  - 35 entry points de rotas (um por módulo)
  - Sem imports circulares
  - Testing trivial
  - Manutenção fácil
```

---

## Ordem de Migração Recomendada

```
Fase 1: Fundação (core)
  1. Criar core/ centralizado
  2. Consolidar iam_client (4→1)
  3. Consolidar EventBus (2→1)

Fase 2: Piloto (5 módulos)
  1. payment/             (já meio limpo)
  2. citizenship/         (importante)
  3. health/              (crítico - saúde primária)
  4. education/           (governança)
  5. governance/          (reports)

Fase 3: Escalada (restantes modules/)
  1. Aplicar template a todos
  2. Mover app/modules/ → modules/ (gradual)

Fase 4: Deprecação (/app/modules/)
  1. Manter legacy 2 sprints
  2. Redirecionar imports
  3. Deletar quando 100% movido
```

---

## Impacto por Tipo de Problema

| Problema | Impacto Atual | Solução | Impacto Pós |
|----------|---------------|---------|-----------|
| 3 APIs em identidade_civil | Botões não reagem | Consolidar para 1 | ✅ Funciona |
| 4 iam_clients | Autenticação inconsistente | 1 central em core/ | ✅ Confiável |
| User model duplicado | Criar user falha | 1 módulo/identity | ✅ Simples |
| 122 rotas espalhadas | Confusão de endpoints | 35 rotas organizadas | ✅ Claro |
| EventBus fragmentado | Módulos desacoplados | 1 global | ✅ Integrado |
| Services em root | Sem camada app | Services em application/ | ✅ Estruturado |

---

## Checklist de Sanidade (Pós-Refator)

```
✅ Servidor sobe sem warnings
✅ Todas as rotas em OpenAPI spec corretas
✅ Criar usuário funciona
✅ Login com Sila_1983 funciona
✅ Botões do dashboard reagem
✅ Eventos entre módulos fluem
✅ Testes passam (100%)
✅ Sem imports circulares
✅ Performance baseline atingido
✅ Documentação atualizada
```

---

_SILA System - Consolidação Arquitetural_  
_Mapa de Dependências v1.0_
