# 📊 ETAPA 1.5: ATUALIZAÇÃO DE REFERÊNCIAS CRUZADAS

**Data**: Novembro 13, 2025 **Status**: ⏳ EM PROGRESSO **Parte da Fase**: Fase 1 -
Reorganização do Layout

---

## 🎯 Objetivo

Atualizar todas as referências, imports e caminhos que apontam para a estrutura antiga
(`scripts/`, `backend/`, `frontend/`) para a nova estrutura reorganizada (`automation/`,
`apps/backend/`, `apps/frontend/`, `docs/`).

---

## 📋 Análise de Referências Encontradas

### ✅ 1. Arquivos Python com Referências `scripts/`

**Total encontrado**: 20+ arquivos

**Padrões identificados**:

- Comandos de execução em strings (comentários/prints):
  `"python scripts/generate_adr.py"`
- Referências relativas em listas: `"scripts/preencher_env_critico.py"`
- Instruções em docstrings

**Arquivos principais**:

- `scripts/adr/generate_adr.py` - Referências internas
- `scripts/adr/generate_index.py` - Referências internas
- `scripts/adr/validate_adr.py` - Referências internas
- `ci/run_tests.py` - Import de scripts
- `automation/maintenance/unify_passwords.py` - Referências em lists

**Risco**: Baixo a Médio (são principalmente strings/comentários)

---

### ✅ 2. CI/CD YAML com Referências `scripts/`

**Total encontrado**: 14 arquivos `.yml`

**Pipeline files**:

- `.github/workflows/msic-cicd.yml`:

  - `scripts/build_frontend.sh` → `automation/maintenance/build_frontend.sh`
  - `scripts/deploy_staging.sh` → `automation/deployment/deploy_staging.sh`
  - `scripts/backup_database.sh` → ❓ Não localizado (verificar)

- `.github/workflows/config-validation.yml`:

  - `python scripts/validate_config.py` → Arquivo não localizado

- `.github/workflows/deploy-dev.yml`:

  - `scripts/smoke_login.sh` → `automation/testing/smoke_login.sh`

- `.github/workflows/config-migration.yml`:

  - `python scripts/migrate_and_validate.py` → Arquivo não localizado

- `.github/workflows/security-scan.yml`:
  - `python scripts/security_audit.py` → Arquivo não localizado

**Risco**: 🔴 ALTO (CI/CD pipelines críticos)

---

### ✅ 3. Shell Scripts Raiz com Referências

**Total encontrado**: 50+ referências

**Scripts principais**:

- `sila.sh`:

  - `./scripts/listar_codigo.sh` → `./automation/utils/listar_codigo.sh`

- `sila_start.sh`:

  - `scripts/build_frontend.sh` → `automation/maintenance/build_frontend.sh`
  - `find scripts/ -type f -name "*.sh"` → `find automation/ -type f -name "*.sh"`

- `cleanup_project.sh`:

  - Referências a `scripts/docker-compose.yml`

- `cleanup_obsolete.sh`:
  - 10+ referências em listas a `scripts/[arquivo].py`

**Risco**: 🔴 ALTO (scripts de inicialização)

---

### ✅ 4. Docker/Compose com Referências

**Total encontrado**: 5+ referências

**Arquivo**:

- `infrastructure/docker/docker-compose.yml`:
  - `../../backend/scripts/init-db.sql` → Verificar localização correta

**Risco**: Médio (checar se arquivo existe em nova localização)

---

### ✅ 5. Referências a `backend/` e `frontend/`

**Status**:

- `backend/` no raiz: Contém apenas cache/env (compatibilidade mantida)
- `frontend/` no raiz: Contém apenas cache/env (compatibilidade mantida)
- `apps/backend/` e `apps/frontend/`: Contêm arquivos reais

**Risco**: Baixo (estrutura dual mantém compatibilidade)

---

## 🔍 Mapeamento de Migração

### Grupo 1: Scripts de Utilidade

```
scripts/generate_adr.py              → automation/utils/ (ou automation/docs/)
scripts/generate_index.py            → automation/utils/ (ou automation/docs/)
scripts/validate_adr.py              → automation/testing/
scripts/build_frontend.sh            → automation/maintenance/
scripts/listar_codigo.sh             → automation/utils/
scripts/smoke_login.sh               → automation/testing/
scripts/deploy_staging.sh            → automation/deployment/
```

### Grupo 2: Scripts CI/CD

```
REFERÊNCIAS EM:
  - .github/workflows/msic-cicd.yml
  - .github/workflows/deploy-dev.yml
  - .github/workflows/config-validation.yml
  - .github/workflows/config-migration.yml
  - .github/workflows/security-scan.yml

PADRÃO DE CORREÇÃO:
  - scripts/SCRIPT.sh          → automation/[category]/SCRIPT.sh
  - python scripts/FILE.py     → python automation/[category]/FILE.py
  - chmod +x scripts/*.sh      → chmod +x automation/**/*.sh
```

### Grupo 3: Scripts de Inicialização

```
ARQUIVOS RAIZ A ATUALIZAR:
  - sila.sh
  - sila_start.sh
  - cleanup_project.sh
  - cleanup_obsolete.sh
  - init_project.ps1
```

---

## ✅ Plano de Ação

### Fase 1: Verificação de Arquivos Faltantes

- [ ] Localizar `scripts/backup_database.sh`
- [ ] Localizar `scripts/validate_config.py`
- [ ] Localizar `scripts/migrate_and_validate.py`
- [ ] Localizar `scripts/security_audit.py`
- [ ] Verificar `backend/scripts/init-db.sql`

### Fase 2: Atualização de CI/CD Workflows

**Arquivos a atualizar**:

1. `.github/workflows/msic-cicd.yml`

   - `scripts/build_frontend.sh` → `automation/maintenance/build_frontend.sh`
   - `scripts/deploy_staging.sh` → `automation/deployment/deploy_staging.sh`
   - Localizar/corrigir `scripts/backup_database.sh`

2. `.github/workflows/deploy-dev.yml`

   - `scripts/smoke_login.sh` → `automation/testing/smoke_login.sh`

3. `.github/workflows/config-validation.yml`

   - `python scripts/validate_config.py` → Localizar arquivo

4. `.github/workflows/config-migration.yml`

   - `python scripts/migrate_and_validate.py` → Localizar arquivo

5. `.github/workflows/security-scan.yml`
   - `python scripts/security_audit.py` → Localizar arquivo

### Fase 3: Atualização de Scripts Raiz

**Arquivos a atualizar**:

1. `sila.sh`

   - `./scripts/listar_codigo.sh` → `./automation/utils/listar_codigo.sh`
   - `scripts/listar_codigo.sh` → `automation/utils/listar_codigo.sh`

2. `sila_start.sh`

   - `scripts/build_frontend.sh` → `automation/maintenance/build_frontend.sh`
   - `find scripts/ -type f -name "*.sh"` → `find automation/ -type f -name "*.sh"`

3. `cleanup_project.sh`

   - Remover/atualizar referências obsoletas a `scripts/`

4. `cleanup_obsolete.sh`
   - Atualizar lista de scripts em `scripts/` para `automation/`

### Fase 4: Atualização de Python/TypeScript

**Arquivos a atualizar**:

1. `automation/maintenance/unify_passwords.py`

   - Lista com `"scripts/preencher_env_critico.py"` →
     `"automation/utils/preencher_env_critico.py"`

2. `ci/run_tests.py`

   - Import de `scripts/run_tests.py` → Localizar em `automation/testing/`

3. Arquivos ADR internos
   - Strings em docstrings/comentários com referências

### Fase 5: Verificação de Docker/Compose

1. `infrastructure/docker/docker-compose.yml`
   - Validar paths relativos após migração

---

## 📊 Estatísticas

| Categoria                   | Total | Status        |
| --------------------------- | ----- | ------------- |
| **Shell scripts (.sh)**     | 50+   | ⏳ Aguardando |
| **Python files (.py)**      | 20+   | ⏳ Aguardando |
| **CI/CD YAML**              | 14+   | ⏳ Aguardando |
| **Docker/Compose**          | 5+    | ⏳ Aguardando |
| **Referências críticas**    | 40+   | 🔴 ALTO       |
| **Referências baixo risco** | 30+   | 🟡 MÉDIO      |

---

## 🎯 Prioridades

### 🔴 CRÍTICO (Fazer primeiro)

1. CI/CD Workflows (.github/workflows/\*.yml)
2. Scripts de inicialização (sila.sh, sila_start.sh)
3. Verificar arquivos faltantes

### 🟡 IMPORTANTE

1. Python scripts em automação
2. Shell scripts em raiz
3. Docker-compose references

### 🟢 MENOR PRIORIDADE

1. Strings em comentários/docstrings
2. Referências em backup/cache

---

## ⚠️ Considerações

1. **Arquivos não localizados**: Alguns scripts referenciados não foram encontrados.
   Possibilidades:

   - Foram removidos em limpezas anteriores
   - Estão em outro diretório sob novo nome
   - Precisam ser criados

2. **Compatibilidade regressiva**:

   - `backend/` e `frontend/` no raiz podem ser mantidos como symlinks
   - Alternativa: manter diretórios vazios por compatibilidade

3. **Git history**:

   - Todos os commits precisam de referências atualizadas
   - Considerar usar find+replace com git history

4. **Documentação**:
   - Atualizar README com novos caminhos
   - Atualizar guias de contribuição
   - Atualizar wikis/documentação interna

---

## 📝 Próximas Etapas

1. ✅ Análise concluída (este documento)
2. ⏳ **Implementação de correções** (próximo passo)
3. ⏳ Validação de imports
4. ⏳ Testes de CI/CD
5. ⏳ Commit final com histórico atualizado

---

**Status**: Fase 1 análise concluída. Pronto para fase de implementação de correções.

---

**Documento gerado**: Novembro 13, 2025 **Verificado por**: Audit automático **Status**:
⏳ AGUARDANDO EXECUÇÃO DE CORREÇÕES
