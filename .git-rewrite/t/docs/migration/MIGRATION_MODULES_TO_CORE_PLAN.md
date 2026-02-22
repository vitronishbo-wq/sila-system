# 📋 PLANO DE MIGRAÇÃO: modules/ → core/ v1.0

**Objetivo Etapa 5**: Consolidar os módulos técnicos em uma camada core/ mais clara e
institucional

**Data**: 16 de Novembro de 2025 **Status**: 🔄 Planejamento **Versão**: 1.0

---

## 🎯 Objetivo Executivo

Reorganizar a estrutura do backend para:

- ✅ Consolidar `modules/` em `core/` (camada técnica)
- ✅ Atualizar imports consistentemente
- ✅ Preparar documentação para onboarding

---

## 📁 Análise da Estrutura Atual

### Backend - Situação Atual

```
apps/backend/
├── modules/              ← Módulos de negócio (location, training, etc)
├── core/                 ← Camada técnica (apenas config.py)
├── app/                  ← Aplicação FastAPI
├── api/                  ← Rotas API
├── config/               ← Configuração
└── tests/                ← Testes
```

### Problemas Identificados

| Problema                   | Impacto            | Prioridade |
| -------------------------- | ------------------ | ---------- |
| `core/` muito vazio        | Confusão sobre uso | 🔴 Alto    |
| `modules/` mistura negócio | Difícil navegar    | 🔴 Alto    |
| Imports inconsistentes     | Erros de import    | 🟡 Médio   |
| Sem documentação           | Onboarding difícil | 🟡 Médio   |
| Paths relativos variados   | Bugs em deploy     | 🟡 Médio   |

---

## 🔄 Plano de Migração - 3 Fases

### FASE 1: Preparação e Análise (Hoje)

**Atividades**:

1. ✅ Mapear estrutura atual
2. ⏳ Definir padrão de organização
3. ⏳ Criar roteiros migração
4. ⏳ Preparar scripts automatizados

**Entregáveis**:

- Documento de mapeamento
- Guia de padrões
- Scripts de migração

---

### FASE 2: Consolidação (Próxima semana)

**Atividades**:

1. ⏳ Criar nova estrutura `core/`
2. ⏳ Migrar módulos técnicos
3. ⏳ Atualizar imports
4. ⏳ Executar testes

**Entregáveis**:

- Código migrado
- Testes verdes
- Logs de migração

---

### FASE 3: Documentação e Validação (Semana +2)

**Atividades**:

1. ⏳ Escrever documentação
2. ⏳ Criar exemplos
3. ⏳ Validar com time
4. ⏳ Deploy em staging

**Entregáveis**:

- Documentação completa
- Exemplos de uso
- Onboarding guide

---

## 📊 Estrutura Proposta - core/

### Novo Layout

```
apps/backend/core/
├── __init__.py
├── config/                      ← Configuração (MOVER DAQUI)
│   ├── __init__.py
│   ├── settings.py             ← Config centralizada
│   ├── environments.py         ← Dev/Staging/Prod
│   └── validators.py           ← Validação de config
│
├── base/                        ← Base para todas as classes
│   ├── __init__.py
│   ├── base_model.py           ← BaseModel para ORM
│   ├── base_schema.py          ← BaseSchema para Pydantic
│   ├── base_service.py         ← BaseService padrão
│   ├── base_repository.py      ← BaseRepository padrão
│   └── base_exceptions.py      ← Exceções base
│
├── database/                    ← Camada de dados
│   ├── __init__.py
│   ├── connection.py           ← Pool de conexões
│   ├── migrations.py           ← Alembic integration
│   ├── session.py              ← Session management
│   └── utils.py                ← Utilitários DB
│
├── auth/                        ← Autenticação e segurança
│   ├── __init__.py
│   ├── jwt.py                  ← JWT handling
│   ├── permissions.py          ← Permission system
│   ├── decorators.py           ← Auth decorators
│   └── constants.py            ← Auth constants
│
├── exceptions/                  ← Exceções customizadas
│   ├── __init__.py
│   ├── application.py          ← App exceptions
│   ├── domain.py               ← Domain exceptions
│   ├── handlers.py             ← Exception handlers
│   └── constants.py            ← Error codes
│
├── logging/                     ← Sistema de logging
│   ├── __init__.py
│   ├── configurator.py         ← Log config
│   ├── formatters.py           ← Log formatters
│   ├── middleware.py           ← Request logging
│   └── constants.py            ← Log levels
│
├── monitoring/                  ← Observabilidade
│   ├── __init__.py
│   ├── metrics.py              ← Prometheus metrics
│   ├── tracing.py              ← Distributed tracing
│   ├── health.py               ← Health checks
│   └── alerts.py               ← Alert system
│
├── utils/                       ← Utilitários
│   ├── __init__.py
│   ├── datetime.py             ← Date/time utils
│   ├── string.py               ← String utils
│   ├── validation.py           ← Validators
│   ├── serializers.py          ← Serialization
│   └── constants.py            ← App constants
│
├── middleware/                  ← Middleware FastAPI
│   ├── __init__.py
│   ├── correlation.py          ← Correlation ID
│   ├── error_handler.py        ← Error handling
│   ├── security.py             ← Security checks
│   └── performance.py          ← Performance tracking
│
└── doc/                         ← Documentação interna
    ├── __init__.py
    ├── STRUCTURE.md            ← Este documento
    ├── MIGRATION.md            ← Guia de migração
    ├── PATTERNS.md             ← Padrões de código
    ├── API_CONVENTIONS.md      ← Convenções API
    └── EXAMPLES.md             ← Exemplos de uso
```

### Estrutura Mantida - modules/

```
apps/backend/modules/
├── __init__.py
├── citizenship/               ← Módulo de negócio
├── training/                  ← Módulo de negócio
├── [outros módulos]/          ← Módulos de negócio
│
└── common/                    ← Utilitários compartilhados (opcional, pode ir para core/)
    ├── __init__.py
    ├── exceptions/
    ├── bases/
    └── utils/
```

---

## 🔀 Mapeamento de Migração

### O que Move para `core/`?

| Item            | Origem            | Destino            | Prioridade |
| --------------- | ----------------- | ------------------ | ---------- |
| `config.py`     | `core/`           | `core/config/`     | 🔴 Alto    |
| Exceções base   | `modules/common/` | `core/exceptions/` | 🔴 Alto    |
| Base classes    | `modules/common/` | `core/base/`       | 🔴 Alto    |
| Auth utilities  | `app/` ou `api/`  | `core/auth/`       | 🔴 Alto    |
| Logging setup   | scripts           | `core/logging/`    | 🟡 Médio   |
| Monitoring      | `observability/`  | `core/monitoring/` | 🟡 Médio   |
| Middleware      | `app/`            | `core/middleware/` | 🟡 Médio   |
| Utils genéricos | diversos          | `core/utils/`      | 🟡 Médio   |

### O que Permanece em `modules/`?

| Item                | Motivo                 | Exemplo              |
| ------------------- | ---------------------- | -------------------- |
| Modelos de negócio  | Específicos do domínio | `citizenship.models` |
| Rotas de negócio    | Específicas do domínio | `citizenship.routes` |
| Serviços de negócio | Lógica de domínio      | `training.services`  |
| Schemas de domínio  | Validação específica   | `location.schemas`   |

---

## 📝 Padrões de Import

### ❌ Evitar (Antigos)

```python
# Caminhos relativos
from ...config import settings
from app.config import settings

# Imports inconsistentes
from modules.common.exceptions import BaseException
import core.config

# Paths absolutas do SO
from /opt/sila-system/apps/backend/core import config
```

### ✅ Usar (Novos)

```python
# Imports absolutos
from core.config import settings
from core.exceptions import ApplicationError
from core.auth import get_current_user
from core.database import get_db

# Opcional: shortcuts
from core import config, exceptions, auth

# Do modules
from modules.citizenship.models import Citizen
from modules.training.services import TrainingService
```

---

## 🔧 Scripts de Migração

### Script 1: Analisar Imports Atuais

```python
#!/usr/bin/env python3
"""Analisa imports atuais e gera relatório."""

def analyze_imports():
    """Mapeia todos os imports encontrados"""
    # Procurar padrões:
    # - from modules.* import
    # - from core.* import
    # - from app.* import
    # - Imports relativos (../config, etc)

    return report
```

### Script 2: Migrar Estrutura

```python
#!/usr/bin/env python3
"""Move arquivos para nova estrutura."""

def migrate_structure():
    """Copia arquivos para core/"""
    # 1. Criar estrutura
    # 2. Copiar arquivos
    # 3. Manter backups
    # 4. Validar integridade

    return migration_log
```

### Script 3: Atualizar Imports

```python
#!/usr/bin/env python3
"""Atualiza imports em todos os arquivos."""

def update_imports():
    """Substitui imports antigos pelos novos"""
    # Mapear:
    # from modules.common.exceptions -> from core.exceptions
    # from app.config -> from core.config
    # from core.config import Config -> from core.config import settings

    return update_report
```

---

## 📚 Documentação Necessária

### 1. STRUCTURE.md

- Explicar organização
- Diagrama de dependências
- O que vai onde

### 2. MIGRATION.md

- Passo a passo da migração
- Como eles podem migrar seus módulos
- Checklist de validação

### 3. PATTERNS.md

- Padrão de imports
- Estrutura de módulo padrão
- Convenções de nomenclatura

### 4. API_CONVENTIONS.md

- Como estruturar uma rota
- Como estruturar um serviço
- Como estruturar um modelo

### 5. EXAMPLES.md

- Exemplo de módulo simples
- Exemplo de módulo complexo
- Exemplo de testes

### 6. ONBOARDING.md

- Primeiros passos
- Criar um módulo
- Testar alterações

---

## ✅ Checklist de Validação

### Pré-Migração

- [ ] Backup de todo código
- [ ] Testes verdes
- [ ] Imports documentados
- [ ] Team alinhado

### Durante Migração

- [ ] Estrutura `core/` criada
- [ ] Arquivos copiados
- [ ] Imports atualizados
- [ ] Testes rodando
- [ ] Sem erros de import

### Pós-Migração

- [ ] Documentação completa
- [ ] Exemplos funcionando
- [ ] Time consegue navegar
- [ ] Deploy sem problemas

---

## 🚀 Próximas Ações

### Hoje (Etapa 5a - Planejamento)

1. ✅ Criar plano (este documento)
2. ⏳ Mapear estrutura atual
3. ⏳ Definir ferramentas
4. ⏳ Preparar scripts

### Próxima semana (Etapa 5b - Consolidação)

5. ⏳ Criar nova `core/`
6. ⏳ Migrar arquivos
7. ⏳ Atualizar imports
8. ⏳ Validar testes

### Semana +2 (Etapa 5c - Documentação)

9. ⏳ Escrever guias
10. ⏳ Criar exemplos
11. ⏳ Validar com team
12. ⏳ Deploy em staging

---

## 📞 Impacto em Outras Áreas

| Área       | Impacto               | Ação                        |
| ---------- | --------------------- | --------------------------- |
| **Tests**  | Importações mudam     | Atualizar path nos testes   |
| **CI/CD**  | Paths em scripts      | Atualizar scripts de build  |
| **Docker** | PYTHONPATH muda       | Verificar Dockerfile        |
| **IDE**    | Imports em red        | Reindexar VSCode            |
| **Docs**   | Paths de exemplo      | Atualizar toda documentação |
| **Team**   | Aprende novos imports | Fazer apresentação          |

---

## 🎓 Benefícios Esperados

### Depois da Migração

✨ **Organização**

- Código técnico separado do negócio
- Estrutura clara e previsível
- Fácil encontrar coisas

✨ **Manutenibilidade**

- Atualizações centralizadas
- Menos duplicação
- Reutilização facilitada

✨ **Onboarding**

- Novos devs entendem estrutura
- Documentação clara
- Exemplos práticos

✨ **Testes**

- Mocking mais fácil
- Testes mais rápidos
- Cobertura maior

✨ **Deploy**

- Menos bugs de path
- CI/CD mais confiável
- Rollback seguro

---

## 📊 Timeline Estimada

```
HOJE       ┌─ Análise + Planning
           │
SEG 17-21  ├─ Criar core/
           ├─ Migrar arquivos
           └─ Atualizar imports
           │
SEG 24-28  ├─ Testes completos
           ├─ Documentação
           └─ Validação
           │
DEZ 01     └─ Deploy em staging
```

---

## 🤝 Responsabilidades

| Papel            | Tarefa            | Prazo        |
| ---------------- | ----------------- | ------------ |
| **Arquiteto**    | Validar estrutura | Hoje         |
| **Dev Lead**     | Revisar plano     | Hoje         |
| **Backend Team** | Executar migração | Próx. semana |
| **QA**           | Testar tudo       | Semana +2    |
| **DevOps**       | Atualizar deploy  | Semana +2    |
| **Tech Writer**  | Documentação      | Semana +2    |

---

## 📋 Referências

- [Estrutura DDD](https://example.com)
- [Python Package Structure](https://example.com)
- [FastAPI Best Practices](https://example.com)
- [Import Patterns Python](https://example.com)

---

**Versão**: 1.0 **Data**: 16 de Novembro de 2025 **Status**: 🔄 Em Planejamento
**Próximo Review**: 17 de Novembro de 2025
