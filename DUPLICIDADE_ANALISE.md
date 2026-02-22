# 🔍 ANÁLISE DE DUPLICIDADE DE DIRETÓRIOS - SILA BACKEND

**Data:** 22 Fevereiro 2026  
**Ferramenta:** Análise automatizada + find + grep

---

## 🚨 DUPLICIDADES CRÍTICAS IDENTIFICADAS

### 1. **INFRA vs INFRASTRUCTURE** 
| Aspecto | `app/infra/` | `app/infrastructure/` |
|---------|----------|--------------|
| **Tamanho** | 20 KB | 76 KB |
| **Conteúdo** | audit/audit_logger.py | repositories/, db/, models/ |
| **Importações** | 0 encontradas | 1 encontrada (seeds) |
| **Status** | 🔴 MORTO | 🟡 PARCIALMENTE ATIVO |
| **Ação** | **ELIMINAR** | **MANTER** |

---

### 2. **APPLICATION vs APP/APPLICATION**
| Aspecto | `application/` (raiz) | `app/application/` |
|---------|----------|--------------|
| **Tamanho** | 156 KB | 32 KB |
| **Conteúdo** | services/ (marriage, birth, death, certificate) | ports/, citizen_service |
| **Importações** | 0 (grep não encontrou) | 2 encontradas |
| **Status** | 🔴 ÓRFÃO (legacy) | 🟡 PRINCIPAL |
| **Ação** | **ELIMINAR** | **MANTER** |

---

### 3. **SEEDS vs APP/SEEDS**
| Aspecto | `seeds/` (raiz) | `app/seeds/` |
|---------|----------|--------------|
| **Tamanho** | 200 KB | 68 KB |
| **Conteúdo** | core/ (FUC, provinces, founding users) | roles.py, catalog.py, run_all.py |
| **Importações** | Provavelmente usados | Menos estruturado |
| **Status** | 🟢 PRODUÇÃO | 🟡 DUPLICADO |
| **Ação** | **MANTER** | **REVISAR** |

---

### 4. **INFRASTRUCTURE (raiz) vs APP/INFRASTRUCTURE**
| Aspecto | `infrastructure/` (raiz) | `app/infrastructure/` |
|---------|----------|--------------|
| **Tamanho** | Desconhecido | 76 KB |
| **Conteúdo** | repositories/ | repositories/, db/, models/ |
| **Status** | Sem análise | Principal |
| **Ação** | **INVESTIGAR** | **MANTER** |

---

### 5. **APPS/BACKEND NESTED**
| Diretório | Conteúdo | Ação |
|-----------|----------|------|
| `apps/backend/` → `apps/backend/app/` | Espelho da estrutura | 🔴 **ELIMINAR** |

---

## 📊 MAPEAMENTO DE RESPONSABILIDADES

```
app/
├── infra/              [20 KB]  🔴 MORTO - possui apenas audit_logger
├── infrastructure/     [76 KB]  🟢 ATIVO - repositories, db, models
├── application/        [32 KB]  🟢 ATIVO - ports, services
└── seeds/              [68 KB]  🟡 REVISAR - duplica with seeds/

ROOT/
├── infrastructure/     [???]    ⚠️  INVESTIGAR
├── application/        [156 KB] 🔴 MORTO - legacy civil registry services
├── seeds/              [200 KB] 🟢 ATIVO - FUC, territories, providers
└── apps/backend/       [RECURS] 🔴 MORTO - nested redundancy
```

---

## 🎯 RECOMENDAÇÕES PRIORITÁRIAS

### **P0 - ELIMINAR IMEDIATAMENTE**
```bash
rm -rf app/infra/              # 20 KB - Apenas 1 arquivo audit_logger.py
rm -rf apps/backend/           # Nested redundancy - copiar app/ se necessário
```

### **P1 - REVISAR + CONSOLIDAR Próximas 48h**
```bash
# Merge application/* -> app/application/*
cp -r application/services/* app/application/services/
rm -rf application/

# Consolidar seeds
# Analisar app/seeds vs seeds/core
# Reorganizar em seeds/ com estrutura clara
```

### **P2 - INVESTIGAÇÃO**
```bash
# infrastructure/ (raiz) vs app/infrastructure/
# Verificar se há código em infrastructure/
```

---

## 📋 ROTEIRO DE LIMPEZA

### **Fase 1: Limpeza estrutural (1h)**
1. Backup: `git add . && git commit -m "backup antes limpeza"`
2. Eliminar `app/infra/`
3. Eliminar `apps/backend/` (nested)
4. Eliminar `application/` (raiz)

### **Fase 2: Consolidação (2h)**
1. Consolidar funções de `application/services/*.py` → `app/application/`
2. Standardizar imports de `application.services` → `app.application.services`
3. Audit trail: `grep -r "from application" . --include="*.py"`

### **Fase 3: Validação (1h)**
```bash
pytest tests/  # Validar nada quebrou
python -m py_compile app/**/*.py  # Syntax check
```

---

## 🔗 IMPACTO EM IMPORTS

**Hoje (com duplicidade):**
```python
from application.services import BirthService
from app.infrastructure.models import CitizenModel
from app.infra.audit import audit_logger
```

**Depois (padronizado):**
```python
from app.application.services import BirthService
from app.infrastructure.models import CitizenModel
from app.core.audit import audit_logger  # ou app.infrastructure.audit
```

---

## 📌 CHECKLIST PÓS-LIMPEZA

- [ ] `app/infra/` removido
- [ ] `apps/backend/` removido  
- [ ] `application/` (raiz) removido
- [ ] Todos os imports atualizados
- [ ] Testes passam: `pytest tests/`
- [ ] `docker build` sucesso
- [ ] Deploy staging funciona

---

**Gerado:** 2026-02-22 | **Ferramentas:** find, grep, du, tree
