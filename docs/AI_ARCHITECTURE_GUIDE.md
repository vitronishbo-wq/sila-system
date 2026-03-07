# 🌌 Sila System - Enterprise AI Architecture Guide

Este documento é a **autoridade máxima** sobre a arquitetura do Sila System. Qualquer IA operando neste repositório deve seguir estas diretrizes para garantir a integridade do design DDD e a escalabilidade do sistema.

## 🏛️ 1. Arquitetura DDD (Domain-Driven Design)

O sistema segue o modelo de arquitetura em camadas (Layered Architecture) onde as dependências fluem estritamente para o centro (o Domínio).

### 📦 Estrutura Padrão de um Módulo DDD
Cada submódulo em `apps/backend/app/modules/` deve seguir rigorosamente esta estrutura:

```text
module_name/
 ├── domain/
 │   ├── entities.py       # Regras de negócio puras e estados
 │   ├── value_objects.py  # Objetos imutáveis
 │   ├── exceptions.py     # Exceções específicas do domínio
 │   └── services.py       # Lógica que envolve múltiplas entidades
 │
 ├── application/
 │   ├── commands.py       # Casos de uso de escrita (CQRS)
 │   ├── queries.py        # Casos de uso de leitura (CQRS)
 │   ├── services.py       # Orquestração de tarefas de aplicação
 │   └── dto.py            # Data Transfer Objects
 │
 ├── infrastructure/
 │   ├── repositories/     # Implementações SQLAlchemy/Redis
 │   ├── models.py         # Mapeamento de banco de dados
 │   └── mappers.py        # Conversão entre Modelos e Entidades
 │
 └── presentation/
     ├── router.py         # Endpoints FastAPI
     ├── schemas.py        # Pydantic (Request/Response)
     └── dependencies.py   # Injeção de dependência via FastAPI
```

### 🛡️ Regras de Dependência entre Camadas
As dependências são unidirecionais e voltadas para o Domínio. **A violação destas regras causará falha nos Guardrails.**

- **Presentation** → Depende de **Application** e **Domain**.
- **Application** → Depende de **Domain**.
- **Infrastructure** → Depende de **Domain** (para implementar interfaces de repositório).

**❌ PROIBIDO (NUNCA FAZER):**
- `Domain` → `Infrastructure` (Domínio nunca conhece detalhes de persistência).
- `Domain` → `FastAPI` ou `SQLAlchemy` (Domínio deve ser Python puro).
- Ciclos de dependência entre módulos (ex: `Módulo A` importa `Módulo B` e vice-versa).

---

## 🐍 2. Padrões de Código e Python

### 📍 Imports Absolutos
Para evitar loops de importação e inconsistências no runtime do Python, **use sempre imports absolutos** baseados na raiz `app`.

- **Correto (Absolute):**
  ```python
  from app.modules.patrimonio.domain.entities import Patrimonio
  ```
- **Incorreto (Relative):**
  ```python
  from ..domain.entities import Patrimonio
  ```

### ⚙️ Tipagem e Pydantic
- Use **Type Hints** em todas as funções e métodos.
- Use **Pydantic V2** para schemas de apresentação e configurações.
- Entidades de Domínio devem preferencialmente usar `@dataclass` ou classes puras para manter independência de frameworks.

---

## 🧪 3. Validação e Segurança da IA

### 🚨 Guardrails de Arquitetura
A IA tem permissão para modificar o código de forma agressiva, mas **deve validar a integridade** antes de submeter as mudanças:
1. Execute `make architecture-report` para regenerar mapa arquitetural, overlap, dependências e saúde dos módulos.
2. O pipeline deve incluir `python3 scripts/guardrails/check_module_registry_sync.py --modules-root apps/backend/app/modules`.
3. O pipeline deve incluir `python3 scripts/guardrails/check_architecture_guide_sync.py` para validar atualização do guia em mudanças reitoras.
4. Execute `make architecture-guardrails` para garantir que o DDD não foi quebrado.
5. Execute `make lint` para validar o estilo de código.
6. Se houver mudanças de esquema, gere o script Alembic em `apps/backend/alembic/versions`.
7. Execute `make migration-domain-report` para atualizar o inventário por domínio.
8. Em `apps/backend/app/main.py`, mantenha `app.include_router(saude_router)` para garantir montagem explícita de `saude_primaria`.

### 🧭 Auditoria de Sobreposição de Domínio (obrigatória antes de fusões)
Antes de consolidar, fundir ou mover módulos entre domínios, execute o scanner de sobreposição:

```bash
python3 scripts/domain_overlap_analysis.py \
  --modules-root apps/backend/app/modules \
  --output reports/domain_overlap_report.md
```

Este relatório deve ser usado como base para decisões de arquitetura e contém:
- `candidate module merges` (fusões candidatas)
- `conflicting domain boundaries` (fronteiras de domínio conflituosas)
- `recommended domain groups` (agrupamento recomendado por macro-domínio)
- módulos que partilham entidades, repositórios e cross-imports

**Regra operacional:** não mover módulos em lote sem primeiro gerar e revisar `reports/domain_overlap_report.md`.

### 🕸️ Mapa de Dependências entre Módulos (obrigatório)
Toda proposta de fusão/consolidação deve incluir o mapa de dependências:

```bash
python3 scripts/module_dependency_analysis.py \
  --modules-root apps/backend/app/modules \
  --output-md reports/module_dependencies.md \
  --output-json reports/module_dependency_graph.json
```

Objetivo:
- detectar `cross-imports` reais entre módulos
- prevenir ciclos de dependência (`circular imports`)
- validar ordem segura de migração por cluster

### 🧩 Registry Explícito de Módulos
O bootstrap de módulos deve usar `apps/backend/app/core/module_registry.py` como fonte única para:
- lista de módulos habilitados
- domínio federado por módulo
- escopo de bootstrap (`api`, `main`, `none`)
- metadados de roteamento (`prefix`, `tags`)

Regra operacional (2026-03-07):
- `apps/backend/app/api/router.py` deve montar módulos exclusivamente via `_mount_registry_modules()`.
- evitar adicionar imports manuais de routers de módulos no `api/router.py` (exceto canais core fora do registry).
- todo novo módulo deve entrar no `MODULES` com `bootstrap_scope` explícito; sem isso, é considerado não-publicado.
- validar sincronização com:
  ```bash
  python3 scripts/guardrails/check_module_registry_sync.py --modules-root apps/backend/app/modules
  ```

### 🗃️ Estratégia de Migrations por Domínio
As migrações devem seguir a estratégia em `docs/architecture/migration_strategy.md`.
Inventário automático:

```bash
python3 scripts/migration_domain_inventory.py \
  --output reports/migration_domain_inventory.md
```

### 🛡️ AI Safety Pipeline
Consulte o documento [AI_GUARDRAILS.md](./AI_GUARDRAILS.md) para detalhes técnicos sobre como rodar as ferramentas de proteção.

---

## 🧭 4. Governança do Guia (Mudanças Reitoras)

### ✅ Regra Obrigatória
Toda mudança **reitora de arquitetura** deve atualizar este arquivo **no mesmo PR/commit**.

### O que conta como mudança reitora
- criação/remoção/fusão de módulos
- alteração de fronteiras de domínio (bounded contexts/federation)
- mudança em regras de dependência entre camadas ou entre módulos
- introdução de novos mecanismos centrais (ex: `module_registry`, dependency graph, orchestration)
- alteração de guardrails obrigatórios ou pipeline arquitetural

### Entregáveis mínimos quando houver mudança reitora
1. atualizar este `AI_ARCHITECTURE_GUIDE.md` com regra operacional nova
2. atualizar `docs/architecture/module_federation_plan.md` (se afetar domínios/módulos)
3. regenerar relatórios arquiteturais aplicáveis em `reports/`
4. registrar impacto e risco da mudança (baixo/médio/alto)

### Manter este arquivo "inteligente"
- manter o guia **curto, normativo e executável** (comandos objetivos)
- evitar texto histórico longo; usar links para detalhes em outros documentos
- remover regras obsoletas quando novas regras substituírem as antigas
- garantir que exemplos de código/comandos estejam válidos no estado atual do repositório

### Checklist obrigatório para agentes
- [ ] a mudança alterou fronteira de domínio, dependência ou bootstrap de módulos?
- [ ] este guia foi atualizado no mesmo ciclo de alteração?
- [ ] os relatórios de arquitetura foram regenerados?
- [ ] a ordem segura foi respeitada: scan -> plan -> validate deps -> migrate -> merge gradual?

---
> [!IMPORTANT]
> A autonomia total da IA (`approval_policy = "never"`) é um privilégio que depende da conformidade total com este guia. Em caso de dúvida, consulte `TEMPLATE_DDD_MODULE.py`.
