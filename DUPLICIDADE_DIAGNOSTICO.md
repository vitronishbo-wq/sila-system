# 📊 DUPLICIDADE DE DIRETÓRIOS - DIAGNÓSTICO EXECUTIVO

## 🎯 ACHADOS PRINCIPAIS

### **DUPLICIDADES CRÍTICAS** ⚠️ 

| Tipo | Duplicada | Ativa | Tamanho | Importação | Ação |
|------|-----------|-------|---------|-----------|------|
| **Infra** | `app/infra/` | `app/infrastructure/` | 3.3 KB vs 27.5 KB | 🔴 NENHUMA | ❌ DELETE |
| **App Layer** | `application/` | `app/application/` | 115.6 KB vs 7.1 KB | 🔴 NENHUMA | ❌ DELETE |
| **Seeds** | `app/seeds/` | `seeds/` | 30.9 KB vs 130.9 KB | ✅ 6 refs | 🔄 CONSOLIDAR |
| **Nested** | `apps/backend/` | N/A | 7.7 KB | 🔴 NENHUMA | ❌ DELETE |

---

## 🗂️ ESTRUTURA HOJE vs RECOMENDADA

### TODAY (CAÓTICO)
```
apps/backend/
├── app/
│   ├── infra/              ← 🔴 MORTO (3.3 KB)
│   ├── infrastructure/     ← 🟢 REAL (27.5 KB)
│   ├── application/        ← 🟤 VAZIO (7.1 KB)
│   └── seeds/              ← 🟡 DUPLICADO (30.9 KB)
├── application/            ← 🔴 ÓRFÃO (115.6 KB)
├── infrastructure/         ← ⚠️  INVESTIGAR
├── seeds/                  ← 🟢 ATIVO (130.9 KB)
└── apps/backend/           ← 🔴 NESTED (7.7 KB)
```

### RECOMENDADO (LIMPO)
```
apps/backend/
└── app/
    ├── api/
    ├── application/        ← Consolidado (citizen_service, ports/)
    ├── core/
    ├── db/
    ├── domain/
    ├── infrastructure/     ← Única (repositories/, db/, models/)
    ├── modules/
    ├── schemas/
    ├── utils/
    └── seeds/              ← Única estrutura (core/, roles.py, etc)
```

---

## 📉 POTENCIAL DE LIMPEZA

| Item | Tamanho | Prioridade |
|------|---------|-----------|
| `rm app/infra/` | -3.3 KB | P0 🔴 |
| `rm application/` | -115.6 KB | P0 🔴 |
| `rm apps/backend/` | -7.7 KB | P0 🔴 |
| `consolidar app/seeds/ + seeds/` | -30.9 KB | P1 🟡 |
| **TOTAL** | **-157.5 KB** | |

---

## 🧭 PLANO DE EXECUÇÃO (4 horas)

### **Fase 1: Análise (30 min)**
```bash
# 1.1 Verificar quem importa cada pasta
grep -r "from app.infra" .
grep -r "from application" .
grep -r "from app.application" .
grep -r "from app.seeds" .
grep -r "from seeds" .

# 1.2 Listar arquivos em cada pasta
find app/infra -type f
find application -type f
find seeds/core -type f
```

### **Fase 2: Backup & Preservação (15 min)**
```bash
git add .
git commit -m "Pre-cleanup backup: duplicated directories identified"
git branch backup/pre-cleanup

# Copiar application/* para análise
cp -r application/services app/application/services_legacy
```

### **Fase 3: Limpeza (30 min)**
```bash
# P0 - Deletar pastas mortas
rm -rf app/infra/
rm -rf apps/backend/

# P0 - Mover legacy para novo local
cp -r application/services/* app/application/
rm -rf application/
```

### **Fase 4: Consolidação Seeds (1 hour)**
```bash
# Decidir: manter seeds/ e eliminar app/seeds/ OU consolidar em app/seeds/
# Opção A: seeds/ é produção
  rm -rf app/seeds/
  
# Opção B: app/seeds/ é padrão
  cp -r seeds/core app/seeds/
  rm -rf seeds/
```

### **Fase 5: Validação & Deploy (1.5 hours)**
```bash
# Syntax check
for f in $(find app -name "*.py"); do python -m py_compile "$f"; done

# Test imports
python -c "from app.application import *"
python -c "from app.infrastructure import *"

# Run unit tests
pytest tests/ -v

# Run integration tests  
pytest tests/integration/ -v
```

---

## ✅ CHECKLIST PÓS-IMPLEMENTAÇÃO

- [ ] `app/infra/` deletado
- [ ] `application/` (root) deletado  
- [ ] `apps/backend/` deletado
- [ ] `app/application/` consolidado com todos os services
- [ ] `app/infrastructure/` é única fonte de verdade
- [ ] `app/seeds/` ou `seeds/` consolidado (uma fonte)
- [ ] Todos imports atualizados (`grep -r "from application" .` = 0 resultados)
- [ ] `pytest tests/` passa 100%
- [ ] `docker build` sucesso
- [ ] Deploy staging validado
- [ ] Documentação atualizada

---

## 🔗 ARQUIVOS AFETADOS (Possível lista de mudanças)

```
seeds/seed_citizen_documents.py:
  from app.infrastructure.models... ✅ JÁ CORRETO
  
// Se houver mais imports de application/*:
app/api/**.py:
  from application.services import X 
  → from app.application.services import X
```

---

## 📌 NOTAS IMPORTANTES

1. **`app/infra/` vs `app/infrastructure/`**
   - `app/infra/` contém apenas `audit_logger.py` (3 KB)
   - `app/infrastructure/` é a verdadeira impl (27.5 KB)
   - **Resultado:** Eliminar `app/infra/`, mover audit para `app/core/audit/` ou `app/infrastructure/`

2. **`application/` vs `app/application/`**
   - `application/` (root) = legacy code (115.6 KB) com services civil registry
   - `app/application/` = novo pattern (7.1 KB) com ports & citizen_service
   - **Resultado:** Mover tudo funcional para `app/application/`, eliminar root

3. **`app/seeds/` vs `seeds/`**
   - Ambos existem com conteúdo diferente
   - `seeds/core/` tem seed_fuc_citizen, angola provinces (dados críticos)
   - `app/seeds/` tem roles, catalog, run_all
   - **Recomendação:** Padronizar em `seeds/` como raiz (dados), manter `app/` limpo

---

**Relatório Gerado:** 2026-02-22 22:00 UTC  
**Ferramentas:** Python analysis + find + grep + du
