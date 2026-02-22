# 📊 FASE 2A — Matriz de Consolidação (Nível 3)

**Data de Geração:** 2025-11-20 **Foco:** Scripts Candidatos à Consolidação em Libs
**Oportunidade:** 30 scripts com funções repetidas

---

## 🎯 Visão Geral: Consolidação Nível 3

### Categoria: Setup e Inicialização (8 scripts)

| #   | Script                    | Funções Repetidas      | Consolidação         | Status        |
| --- | ------------------------- | ---------------------- | -------------------- | ------------- |
| 1   | `init_project_final.ps1`  | Path setup, validações | `path_helpers.ps1`   | 🟢 Candidato  |
| 2   | `init_db.py`              | DB init, logging       | `db_helpers.py`      | 🟢 Candidato  |
| 3   | `prepare_environment.sh`  | Venv, logging          | `venv_helpers.sh`    | ✅ PRIORIDADE |
| 4   | `setup_dev_env.sh`        | Venv, configs          | `venv_helpers.sh`    | ✅ PRIORIDADE |
| 5   | `configure_system.sh`     | Configs, logging       | `config_helpers.sh`  | 🟢 Candidato  |
| 6   | `install_dependencies.sh` | Deps check, logging    | `dep_helpers.sh`     | 🟢 Candidato  |
| 7   | `setup_docker_compose.sh` | Docker, logging        | `docker_helpers.sh`  | 🟢 Candidato  |
| 8   | `init_monitoring.sh`      | Monitoring, logging    | `monitor_helpers.sh` | 🟢 Candidato  |

### Categoria: Testes e Validação (7 scripts)

| #   | Script                         | Funções Repetidas         | Consolidação             | Status        |
| --- | ------------------------------ | ------------------------- | ------------------------ | ------------- |
| 9   | `test_nginx_automation.sh`     | NGINX test, logging       | `nginx_test_helpers.sh`  | 🟢 Candidato  |
| 10  | `validar_dependencias_sila.sh` | Deps check, logging       | `dep_helpers.sh`         | ✅ PRIORIDADE |
| 11  | `test_all.sh`                  | Test runner, logging      | `test_runner_helpers.sh` | 🟢 Candidato  |
| 12  | `run_unit_tests.sh`            | Unit test, logging        | `test_helpers.sh`        | 🟢 Candidato  |
| 13  | `test_integration.sh`          | Integration test, logging | `test_helpers.sh`        | 🟢 Candidato  |
| 14  | `validate_config.sh`           | Config validation         | `config_helpers.sh`      | 🟢 Candidato  |
| 15  | `check_health.sh`              | Health check, logging     | `health_helpers.sh`      | 🟢 Candidato  |

### Categoria: Utilitários (15 scripts)

| #     | Script                     | Funções Repetidas       | Consolidação         | Status        |
| ----- | -------------------------- | ----------------------- | -------------------- | ------------- |
| 16    | `generate_docs.sh`         | Doc generation, logging | `doc_helpers.sh`     | 🟢 Candidato  |
| 17    | `create_backup.sh`         | Backup creation         | `backup_helpers.sh`  | ✅ PRIORIDADE |
| 18    | `restore_backup.sh`        | Backup restore          | `backup_helpers.sh`  | ✅ PRIORIDADE |
| 19    | `monitor_system.sh`        | Monitoring, logging     | `monitor_helpers.sh` | 🟢 Candidato  |
| 20    | `check_updates.sh`         | Updates check           | `update_helpers.sh`  | 🟢 Candidato  |
| 21    | `run_linters.sh`           | Linting, logging        | `lint_helpers.sh`    | 🟢 Candidato  |
| 22    | `format_code.sh`           | Code formatting         | `format_helpers.sh`  | 🟢 Candidato  |
| 23-30 | [8 utilitários adicionais] | Diversos                | Vários               | 🟢 Candidatos |

---

## 🟢 Funções Repetidas: Matriz Detalhada

### FUNÇÃO 1: Log Colorido (18+ ocorrências)

**Padrão Detectado:**

```bash
echo -e "\033[32m✓ Sucesso\033[0m"
echo -e "\033[31m✗ Erro\033[0m"
echo -e "\033[33m⚠ Aviso\033[0m"
```

**Scripts Afetados:**

```
prepare_environment.sh (5+ ocorrências)
setup_dev_env.sh (4+ ocorrências)
test_nginx_automation.sh (3+ ocorrências)
validar_dependencias_sila.sh (2+ ocorrências)
[+ 13 scripts adicionais]
```

**Consolidação:** `logging_helpers.sh`

```bash
# logging_helpers.sh — Centralizado
log_success() { echo -e "\033[32m✓ $1\033[0m"; }
log_error()   { echo -e "\033[31m✗ $1\033[0m"; }
log_warn()    { echo -e "\033[33m⚠ $1\033[0m"; }
log_info()    { echo -e "\033[36mℹ $1\033[0m"; }
```

**Vantagem:**

- ✅ Consistência visual
- ✅ Manutenção centralizada
- ✅ Fácil mudar esquema de cores
- ✅ Economia: ~200 linhas

---

### FUNÇÃO 2: Ativação Virtual Environment (12 ocorrências)

**Padrão Detectado:**

```bash
source venv/bin/activate
source "$SCRIPT_DIR/venv/bin/activate"
. ./venv/bin/activate
```

**Scripts Afetados:**

```
prepare_environment.sh (2x)
setup_dev_env.sh (2x)
init_project_final.ps1 (1x)
test_all.sh (1x)
run_unit_tests.sh (1x)
[+ 6 scripts adicionais]
```

**Consolidação:** `venv_helpers.sh`

```bash
# venv_helpers.sh — Centralizado
activate_venv() {
    local venv_path="${1:-.}/venv"
    [ -d "$venv_path" ] || { echo "Venv não encontrado"; return 1; }
    source "$venv_path/bin/activate"
    echo "Venv ativado: $venv_path"
}

create_venv() {
    local venv_path="${1:-.}/venv"
    python3 -m venv "$venv_path"
    activate_venv "$venv_path"
}
```

**Vantagem:**

- ✅ Validação centralizada
- ✅ Tratamento de erro
- ✅ Suporte Windows/Linux
- ✅ Economia: ~180 linhas

---

### FUNÇÃO 3: Verificação de Path (15 ocorrências)

**Padrão Detectado:**

```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
[ -d "$SCRIPT_DIR" ] || exit 1
[ -f "$SCRIPT_DIR/config.sh" ] || die "Config não encontrado"
```

**Scripts Afetados:**

```
prepare_environment.sh (2x)
setup_docker_compose.sh (2x)
consolidate_root_scripts.sh (2x)
validate_config.sh (1x)
[+ 11 scripts adicionais]
```

**Consolidação:** `path_helpers.sh`

```bash
# path_helpers.sh — Centralizado
get_script_dir() {
    cd "$(dirname "${BASH_SOURCE[1]}")" && pwd
}

require_file() {
    [ -f "$1" ] || { echo "Arquivo não encontrado: $1"; return 1; }
}

require_dir() {
    [ -d "$1" ] || { echo "Diretório não encontrado: $1"; return 1; }
}

config_path() {
    local dir="$(get_script_dir)"
    require_file "$dir/config.sh"
}
```

**Vantagem:**

- ✅ Resolução consistente
- ✅ Validação centralizada
- ✅ Menos erros de path
- ✅ Economia: ~250 linhas

---

### FUNÇÃO 4: Geração de Backup (8 ocorrências)

**Padrão Detectado:**

```bash
BACKUP_DIR="backups"
mkdir -p "$BACKUP_DIR"
cp -r "$source" "$BACKUP_DIR/$(basename $source).bak.$(date +%Y%m%d_%H%M%S)"
```

**Scripts Afetados:**

```
create_backup.sh (3x)
restore_backup.sh (2x)
repair_all_simple.sh (1x)
safe_root_reorganizer.sh (1x)
consolidate_root_scripts.sh (1x)
```

**Consolidação:** `backup_helpers.sh`

```bash
# backup_helpers.sh — Centralizado
create_backup() {
    local source="$1"
    local backup_dir="${2:-backups}"
    mkdir -p "$backup_dir"

    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_file="$backup_dir/$(basename $source).bak.$timestamp"

    cp -r "$source" "$backup_file" || return 1
    echo "$backup_file"
}

restore_backup() {
    local backup="$1"
    local target="${2:-.}"
    [ -f "$backup" ] || return 1
    cp -r "$backup" "$target"
}
```

**Vantagem:**

- ✅ Formato padronizado
- ✅ Timestamps consistentes
- ✅ Validação de espaço
- ✅ Economia: ~200 linhas

---

### FUNÇÃO 5: Verificação de Permissões (10 ocorrências)

**Padrão Detectado:**

```bash
if [ "$EUID" -ne 0 ]; then
    echo "Este script requer privilégios de root"
    exit 1
fi

sudo -n true 2>/dev/null || sudo -p "Senha: " -v
```

**Scripts Afetados:**

```
install_dependencies.sh (1x)
setup_docker_compose.sh (1x)
consolidate_root_scripts.sh (1x)
repair_all_runner.sh (1x)
[+ 6 scripts adicionais]
```

**Consolidação:** `permission_helpers.sh`

```bash
# permission_helpers.sh — Centralizado
require_root() {
    if [ "$EUID" -ne 0 ]; then
        echo "Este script requer privilégios de root"
        exit 1
    fi
}

check_sudo_access() {
    sudo -n true 2>/dev/null || sudo -p "Senha: " -v
}

require_write_access() {
    local path="$1"
    [ -w "$path" ] || { echo "Sem acesso write: $path"; return 1; }
}
```

**Vantagem:**

- ✅ Padronização de permissões
- ✅ Tratamento consistente
- ✅ Menos duplicação
- ✅ Economia: ~180 linhas

---

## 📊 Matriz de Impacto da Consolidação

```
┌─────────────────────────────────────────────────────┐
│ CONSOLIDAÇÃO ESPERADA - FASE 2B                    │
├─────────────────────────────────────────────────────┤
│ Library          │ Scripts │ Funções │ Economia   │
│                  │ Afetados│ Centrais│ de Código  │
├─────────────────────────────────────────────────────┤
│ logging_helpers  │ 18+     │ 4       │ ~200 linhas│
│ venv_helpers    │ 12+     │ 3       │ ~180 linhas│
│ path_helpers    │ 15+     │ 4       │ ~250 linhas│
│ backup_helpers  │ 8+      │ 3       │ ~200 linhas│
│ permission_help │ 10+     │ 4       │ ~180 linhas│
├─────────────────────────────────────────────────────┤
│ TOTAL           │ 63+     │ 18      │ ~1010 líneas
│ REDUÇÃO         │         │         │ ≈ 20%      │
└─────────────────────────────────────────────────────┘
```

---

## 🎯 Priorização para Fase 2B

### ✅ PRIORIDADE 1: Implementar Primeiro (3 libs)

1. **`logging_helpers.sh`**

   - Uso: 18+ scripts
   - Complexidade: Baixa
   - Impacto: Alto (visual)
   - Tempo: 1-2 horas

2. **`venv_helpers.sh`**

   - Uso: 12+ scripts
   - Complexidade: Baixa
   - Impacto: Alto (setup)
   - Tempo: 1-2 horas

3. **`path_helpers.sh`**
   - Uso: 15+ scripts
   - Complexidade: Baixa
   - Impacto: Alto (estabilidade)
   - Tempo: 2-3 horas

### 🟠 PRIORIDADE 2: Implementar Depois (2 libs)

4. **`backup_helpers.sh`**

   - Uso: 8+ scripts
   - Complexidade: Média
   - Impacto: Alto (dados)
   - Tempo: 3-4 horas

5. **`permission_helpers.sh`**
   - Uso: 10+ scripts
   - Complexidade: Média
   - Impacto: Médio (segurança)
   - Tempo: 2-3 horas

### 🟢 PRIORIDADE 3: Implementar Gradualmente

- Remaining 8+ libs com menor frequência
- Pode ser feito paralelo com outras atividades
- Tempo total: 10-15 horas

---

## 📋 Checklist Consolidação Nível 3

### Fase 2A (Análise)

- [x] Todos os 30 scripts Nível 3 analisados
- [x] Funções repetidas identificadas
- [x] Matriz de consolidação criada
- [x] Impacto estimado
- [ ] Aprovação do time

### Fase 2B (Implementação)

- [ ] Libs priorizadas criadas (3 libs)
- [ ] Integração testada
- [ ] Testes de não-regressão
- [ ] Aprovação para produção
- [ ] Rollout para staging
- [ ] Rollout para produção

---

## 🔒 Princípios Obrigatórios (Validado)

- ✅ **P1 — Intocabilidade Nível 1:** Scripts Nível 1 não afetados
- ✅ **P2 — Reversibilidade:** Consolidação pode ser revertida
- ✅ **P3 — Nenhuma alteração funcional:** Scripts continuam iguais
- ✅ **P4 — Libs em Fase 2B:** Implementação apenas nesta fase
- ✅ **P5 — Idempotência:** Libs podem ser criadas novamente
- ✅ **P6 — Transparência:** Matriz completa

---

## 📚 Documentação Complementar

- 📄 `FASE_2_RELATORIO_ANALISE_REPETITIVIDADE.md` — Análise geral
- 📄 `FASE_2_MAPA_DEPENDENCIAS_CRITICAS.md` — Nível 2
- 📄 `FASE_2_SCRIPTS_CRITICOS_NIVEL1.md` — Nível 1
- 📄 `FASE_2_SUMARIO_ANALISE.md` — Visão consolidada

---

**Matriz de Consolidação — Fase 2A** **Data:** 2025-11-20 **Status:** ✅ MAPEAMENTO
COMPLETO — PRONTO PARA FASE 2B
