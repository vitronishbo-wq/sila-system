# 🚀 Guia de Execução: Migração modules/ → core/

**Duração**: ~1 hora para Fase 1 **Risco**: 🟢 Muito Baixo **Rollback**: Possível em < 5
minutos

---

## ⚡ Quick Start (5 minutos)

### Pré-requisitos

```bash
# 1. Estar em ~/dev/sila-system
cd ~/dev/sila-system

# 2. Git limpo
git status  # Deve estar limpo

# 3. Testes passando
pytest tests/ -q  # Todos passam?
```

### Backup Imediato

```bash
# Criar snapshot do estado atual
git commit --allow-empty -m "Checkpoint antes de migração Phase 1"

# Ou zip completo
tar czf backup_pre_migration.tar.gz apps/backend/
```

---

## 📋 FASE 1: Migração de `monitoring/` (45 min)

### Etapa 1: Analisar Estrutura

```bash
# 1. Analisar
python3 migration_analyzer.py

# 2. Classificar
python3 module_classifier.py

# 3. Revisar plano
cat MIGRATION_EXECUTIVE_PLAN.md | grep -A 50 "FASE 1"
```

**Saída esperada:**

```
32 módulos encontrados
monitoring: 37 arquivos, importado por 2 módulos
common: 26 arquivos, importado por 5 módulos
auth: 18 arquivos, importado por 5 módulos
...
```

---

### Etapa 2: Preparar Ambiente

```bash
# 1. Git branch
git checkout -b feature/migrate-monitoring

# 2. Verificar que monitoring existe
ls -la apps/backend/modules/monitoring/

# 3. Listar arquivos que importam monitoring
grep -r "from modules.monitoring" apps/backend/modules/
# Output:
#   modules/governance/...
#   modules/justice/...
```

---

### Etapa 3: Criar Estrutura em core/

```bash
# 1. Criar pastas
mkdir -p apps/backend/core/monitoring
mkdir -p apps/backend/core/monitoring/{sentry,metrics,logs}

# 2. Verificar
ls -la apps/backend/core/monitoring/

# 3. Criar __init__.py
touch apps/backend/core/monitoring/__init__.py
touch apps/backend/core/monitoring/sentry/__init__.py
touch apps/backend/core/monitoring/metrics/__init__.py
touch apps/backend/core/monitoring/logs/__init__.py
```

---

### Etapa 4: Copiar Arquivos

```bash
# 1. Listar arquivos antes
ls apps/backend/modules/monitoring/*.py | wc -l

# 2. Copiar (não mover ainda!)
cp apps/backend/modules/monitoring/*.py apps/backend/core/monitoring/

# 3. Copiar subpastas (se existir)
[ -d apps/backend/modules/monitoring/sentry ] && \
  cp -r apps/backend/modules/monitoring/sentry/* apps/backend/core/monitoring/sentry/

# 4. Verificar
ls apps/backend/core/monitoring/

# 5. Contar arquivos
ls apps/backend/core/monitoring/*.py | wc -l  # Deve ser igual ao passo 1
```

---

### Etapa 5: Testar Imports Sem Modificação

```bash
# 1. Validar sintaxe dos arquivos novos
python3 -m py_compile apps/backend/core/monitoring/*.py

# 2. Tentar fazer import (vai falhar por enquanto)
python3 -c "from core.monitoring import *" 2>&1 | head -5
# Esperado: ModuleNotFoundError (ainda não atualizamos imports)

# 3. Testes ainda devem passar (usando imports antigos)
pytest tests/ -k "monitoring" -v
```

---

### Etapa 6: Atualizar Imports Automaticamente

```bash
# 1. DRY RUN primeiro
python3 update_imports.py \
  --from "modules.monitoring" \
  --to "core.monitoring" \
  --dry-run \
  --recursive

# Saída esperada:
# 🔄 Iniciando atualização de imports...
#   De: modules.monitoring
#   Para: core.monitoring
# 📝 Atualizando 729 arquivos...
# RESULTADOS:
#   • Arquivos processados: 729
#   • Arquivos modificados: 2
#   • Total de mudanças: 3

# 2. Se OK, executar REAL com backup
python3 update_imports.py \
  --from "modules.monitoring" \
  --to "core.monitoring" \
  --backup \
  --recursive

# 3. Verificar backup criado
ls -la backup_migration_*/
```

---

### Etapa 7: Validar Integridade

```bash
# 1. Verificar que imports antigos não existem
grep -r "from modules.monitoring" apps/backend/  # Deve retornar 0

# 2. Verificar que imports novos existem
grep -r "from core.monitoring" apps/backend/ | wc -l  # Deve ser > 0

# 3. Validação automática
python3 validate_migration.py

# Saída esperada:
# ✓ imports ........... PASS
# ✓ duplicates ........ PASS
# ✓ syntax ............ PASS
# ✓ direct_imports .... PASS
# ✓ structure ......... PASS
# ✓ tests ............. PASS
```

---

### Etapa 8: Rodar Testes Completos

```bash
# 1. Testes de monitoramento
pytest tests/ -k monitoring -v

# 2. Testes que importam monitoring
pytest tests/ -k "governance or justice" -v

# 3. Toda a suite
pytest tests/ -x  # Parar no primeiro erro
```

**Esperado**: ✅ Todos passam

---

### Etapa 9: Remover Antigo (Opcional)

```bash
# APENAS se testes 100% OK

# 1. Backup da origem (já temos)
# 2. Remover módulo antigo
rm -rf apps/backend/modules/monitoring/

# 3. Verificar que não quebrou nada
pytest tests/ -k monitoring

# 4. Confirmar
ls apps/backend/modules/monitoring/  # Deve retornar: não encontrado
ls apps/backend/core/monitoring/     # Deve retornar: arquivos
```

---

### Etapa 10: Commit & Push

```bash
# 1. Ver mudanças
git status

# 2. Revisar diffs importantes
git diff apps/backend/modules/*/  | head -50

# 3. Adicionar
git add -A

# 4. Commit com descrição
git commit -m "chore: migrate monitoring from modules/ to core/

- Move 37 arquivos de modules/monitoring/ para core/monitoring/
- Atualiza imports em 2 módulos (governance, justice)
- Valida com pytest: 100% passando
- Estrutura: core/monitoring/{sentry,metrics,logs}"

# 5. Push
git push origin feature/migrate-monitoring

# 6. Criar PR para review
# (Colar link no Slack/Teams)
```

---

## 📋 FASE 2: Migração de `common/` (30 min)

Repetir Fase 1 mas com `common/`:

```bash
# Checklist rápido
git checkout main && git pull  # Sincronizar
git checkout -b feature/migrate-common

python3 update_imports.py \
  --from "modules.common" \
  --to "core.utils.common" \
  --backup --dry-run

# (Se OK)
python3 update_imports.py \
  --from "modules.common" \
  --to "core.utils.common" \
  --backup --recursive

python3 validate_migration.py

pytest tests/ -x

git add -A
git commit -m "chore: migrate common from modules/ to core/utils/"
git push
```

---

## 🚨 FASE 3: Migração de `auth/` (90 min - CRÍTICO)

⚠️ **Importado por 140 arquivos - fazer com cuidado**

```bash
# ANTES: Backup extra
cp -r apps/backend backup_auth_migration_$(date +%s)

git checkout main && git pull
git checkout -b feature/migrate-auth

# Step 1: DRY RUN
python3 update_imports.py \
  --from "modules.auth" \
  --to "core.auth" \
  --dry-run \
  --recursive

# Analisar output. Deve mostrar ~140 arquivos

# Step 2: REAL com backup automático
python3 update_imports.py \
  --from "modules.auth" \
  --to "core.auth" \
  --backup \
  --recursive

# Step 3: Validação agresiva
python3 validate_migration.py

# Step 4: Testes completos
pytest tests/test_auth -v
pytest tests/test_citizenship -v
pytest tests/test_documents -v
pytest tests/test_finance -v
pytest tests/test_dashboard -v
pytest tests/ -x

# Step 5: Se tudo OK
rm -rf apps/backend/modules/auth/
git add -A
git commit -m "chore: migrate auth from modules/ to core/ (CRITICAL)

- Move 18 arquivos de modules/auth/ para core/auth/
- Atualiza imports em 140+ arquivos across 5 domínios
- Testes: 100% passando
- Validação: PASS em todos os checks"

git push
```

---

## ✅ Checklist Completo

- [ ] Git branch criado
- [ ] Backup completo testado
- [ ] Estrutura criada em core/
- [ ] Arquivos copiados
- [ ] Imports atualizados (dry-run OK?)
- [ ] Validação automática: PASS
- [ ] Testes: 100% passando
- [ ] Estrutura antiga removida
- [ ] Commit message descritiva
- [ ] PR aberto para review
- [ ] Merge após aprovação

---

## 🆘 Troubleshooting

### Erro: `ImportError: cannot import name X from core.monitoring`

```bash
# Solução: Import atualizado mas arquivo não existe
ls apps/backend/core/monitoring/  # Verificar que arquivo existe

# Se não, copiar:
cp apps/backend/modules/monitoring/X.py apps/backend/core/monitoring/
```

### Erro: Arquivo duplicado em core/ E modules/

```bash
# Solução: Remover um
rm -rf apps/backend/modules/monitoring/

# Ou se problema em core:
rm -rf apps/backend/core/monitoring/
git checkout -- apps/backend/core/monitoring/  # Reverter
```

### Erro: Tests falhando após migração

```bash
# Step 1: Verificar o erro específico
pytest tests/ -x -v --tb=short

# Step 2: Se import error, validar:
python3 validate_migration.py --check-imports

# Step 3: Se import está OK, pode ser lógica:
# Revisar teste e import manualmente

# Step 4: Último recurso - rollback:
git reset --hard HEAD~1
```

### Erro: "Too many files to move"

```bash
# Se cp/mv não funciona com muitos arquivos:
find apps/backend/modules/monitoring -type f -name "*.py" | \
  xargs -I {} cp {} apps/backend/core/monitoring/
```

---

## 📊 Métricas Pós-Migração

```bash
# Contar arquivos
echo "core/: $(find apps/backend/core -name '*.py' | wc -l)"
echo "modules/: $(find apps/backend/modules -name '*.py' | wc -l)"

# Contar imports core vs modules
echo "from core.*: $(grep -r 'from core\.' apps/backend | wc -l)"
echo "from modules.*: $(grep -r 'from modules\.' apps/backend | wc -l)"

# Validar nenhum erro
python3 validate_migration.py --check-all
```

---

## 🎯 Próximo Passo

Após Fase 1 ✅:

1. PR aprovada?
2. Merge para main?
3. Deploy staging?
4. Começar Fase 2?

```bash
# Para Fase 2
git pull origin main
git checkout -b feature/migrate-common
# (Repetir etapas acima)
```

---

**Tempo Total Estimado**:

- Fase 1 (monitoring): 45 min
- Fase 2 (common): 30 min
- Fase 3 (auth): 90 min
- **Total: ~3 horas**

**Risco**: 🟢→🟠→🔴 (aumenta com cada fase) **Rollback**: < 5 min (git revert)
**Benefício**: ✅ Arquitetura mais clara e sustentável
