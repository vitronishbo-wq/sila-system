#!/usr/bin/env bash

# ==============================================================================
# SILA System - Safe Root Reorganizer
# ------------------------------------------------------------------------------
# Objetivo:
#   Organizar ARQUIVOS SOLTOS NA RAIZ do repositório (logs e reports gerados)
#   movendo-os para pastas dedicadas, de forma segura e auditável.
#
# Características:
#   - Opera SOMENTE na raiz (não entra em subdiretórios)
#   - Modo padrão: DRY-RUN (não move nada, apenas gera plano)
#   - Modo apply: --apply (executa os movimentos com confirmação)
#   - Usa git mv quando possível para preservar histórico
#   - Agrupa em:
#       logs/                     → logs simples
#       reports/logs/             → logs de relatórios
#       reports/integration/      → resultados de testes de integração
#       reports/audit/            → auditorias
#       reports/onboarding/       → relatórios de onboarding
#       reports/import_updates/   → relatórios de importação
#       reports/migration/        → relatórios de migração
#       reports/phase3/           → relatórios da fase 3
#
# Uso rápido:
#   # Apenas ver o plano (NÃO move nada)
#   ./safe_root_reorganizer.sh
#
#   # Aplicar plano padrão (logs + reports)
#   ./safe_root_reorganizer.sh --apply
#
#   # Ver ajuda
#   ./safe_root_reorganizer.sh --help
# ============================================================================

set -euo pipefail

# ----------------------------------------------------------------------------
# Cores
# ----------------------------------------------------------------------------
if [ -t 1 ]; then
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  YELLOW='\033[1;33m'
  BLUE='\033[0;34m'
  CYAN='\033[0;36m'
  BOLD='\033[1m'
  RESET='\033[0m'
else
  RED=''
  GREEN=''
  YELLOW=''
  BLUE=''
  CYAN=''
  BOLD=''
  RESET=''
fi

log_info()   { echo -e "${BLUE}[INFO]${RESET}  $*"; }
log_warn()   { echo -e "${YELLOW}[WARN]${RESET}  $*"; }
log_error()  { echo -e "${RED}[ERROR]${RESET} $*"; }
log_success(){ echo -e "${GREEN}[OK]${RESET}    $*"; }

# ----------------------------------------------------------------------------
# Ajuda e verificação de raiz
# ----------------------------------------------------------------------------
usage() {
  cat <<EOF
${BOLD}SILA System - Safe Root Reorganizer${RESET}

Uso:
  $0 [opções]

Opções:
  --apply        Aplica o plano (executa mv/git mv)
  --include-docs Inclui reorganização de documentação da raiz (ETAPA_*, FASE_3_*, MIGRATION_*, etc.)
  --include-scripts Inclui reorganização de scripts da raiz (sila_start.sh, dev-up.ps1, etc.)
  --no-color     Desabilita cores no output
  --help, -h     Mostra esta ajuda

Comportamento padrão:
  - Examina apenas arquivos diretamente na raiz do repositório
  - Gera um plano de reorganização para logs e reports
  - Opcionalmente inclui documentação da raiz quando --include-docs é usado
  - NÃO move nada a menos que --apply seja informado

Exemplos:
  # Somente plano (recomendado primeiro)
  $0

  # Aplicar plano padrão (logs + reports)
  $0 --apply
EOF
}

check_project_root() {
  if [ ! -f "README.md" ] || [ ! -d ".git" ]; then
    log_error "Este script deve ser executado na raiz do repositório (onde há README.md e .git)."
    exit 1
  fi
}

# ----------------------------------------------------------------------------
# Flags de execução
# ----------------------------------------------------------------------------
APPLY=false
INCLUDE_DOCS=false
INCLUDE_SCRIPTS=false

# Parsing simples de argumentos
while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply)
      APPLY=true
      shift
      ;;
    --include-docs)
      INCLUDE_DOCS=true
      shift
      ;;
    --include-scripts)
      INCLUDE_SCRIPTS=true
      shift
      ;;
    --no-color)
      RED=''; GREEN=''; YELLOW=''; BLUE=''; CYAN=''; BOLD=''; RESET=''
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      log_warn "Opção desconhecida: $1 (ignorando)"
      shift
      ;;
  esac
done

check_project_root

if [ "$INCLUDE_DOCS" = true ]; then
  log_info "Iniciando varredura segura da raiz para organizar logs, reports e documentação..."
else
  log_info "Iniciando varredura segura da raiz para organizar logs e reports..."
fi

# Arquivo de plano (sempre gerado)
PLAN_FILE="root_reorg_plan_$(date +%Y%m%d_%H%M%S).txt"
log_info "Plano será registrado em: ${PLAN_FILE}"

echo "# SILA System - Root Reorganization Plan" > "$PLAN_FILE"
echo "# Generated: $(date)" >> "$PLAN_FILE"
echo "# Mode: $( [ "$APPLY" = true ] && echo "APPLY" || echo "DRY-RUN" )" >> "$PLAN_FILE"
echo "# Include docs: $INCLUDE_DOCS" >> "$PLAN_FILE"
echo "# Include scripts: $INCLUDE_SCRIPTS" >> "$PLAN_FILE"
echo "" >> "$PLAN_FILE"

# ----------------------------------------------------------------------------
# Helpers de movimentação
# ----------------------------------------------------------------------------
ensure_dir() {
  local dir="$1"
  if [ ! -d "$dir" ]; then
    mkdir -p "$dir"
  fi
}

is_git_tracked() {
  local path="$1"
  if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    if git ls-files --error-unmatch "$path" >/dev/null 2>&1; then
      return 0
    fi
  fi
  return 1
}

register_move() {
  local category="$1"    # ex: logs, report:onboarding
  local src="$2"         # ex: service_logs.txt
  local dest="$3"        # ex: logs/service_logs.txt

  if [ ! -e "$src" ]; then
    return 0
  fi

  ensure_dir "$(dirname "$dest")"

  echo "[${category}] $src -> $dest" | tee -a "$PLAN_FILE"

  if [ "$APPLY" = true ]; then
    if is_git_tracked "$src"; then
      log_info "git mv $src $dest"
      git mv "$src" "$dest"
    else
      log_info "mv $src $dest"
      mv "$src" "$dest"
    fi
  fi
}

# ----------------------------------------------------------------------------
# Confirmação em modo APPLY
# ----------------------------------------------------------------------------
if [ "$APPLY" = true ]; then
  echo
  if [ "$INCLUDE_DOCS" = true ]; then
    log_warn "MODO APLICAR ATIVO: arquivos serão movidos (logs + reports + docs da raiz)."
  else
    log_warn "MODO APLICAR ATIVO: arquivos serão movidos (logs + reports)."
  fi
  read -r -p "Confirmar execução? (y/N): " CONFIRM
  case "$CONFIRM" in
    y|Y)
      log_info "Prosseguindo com a reorganização."
      ;;
    *)
      log_warn "Operação cancelada pelo usuário."
      exit 0
      ;;
  esac
fi

# ----------------------------------------------------------------------------
# Varredura de arquivos da raiz
# ----------------------------------------------------------------------------
log_info "Coletando arquivos diretamente na raiz..."

mapfile -d '' ROOT_FILES < <(find . -maxdepth 1 -type f -print0)

PLANNED_MOVES=0

plan_move() {
  local category="$1"
  local src="$2"
  local dest="$3"

  # Remover prefixo ./ se existir
  src="${src#./}"
  dest="${dest#./}"

  register_move "$category" "$src" "$dest"
  PLANNED_MOVES=$((PLANNED_MOVES + 1))
}

for path in "${ROOT_FILES[@]}"; do
  file="${path#./}"

  case "$file" in
    # ----------------------------------------------------------
    # LOGS SIMPLES NA RAIZ
    # ----------------------------------------------------------
    service_logs.txt)
      plan_move "logs" "$path" "logs/$file"
      ;;
    services_status.txt)
      plan_move "logs" "$path" "logs/$file"
      ;;
    test_results.txt)
      plan_move "logs" "$path" "logs/$file"
      ;;

    # ----------------------------------------------------------
    # LOGS/REPORTS ESPECÍFICOS JÁ PADRONIZADOS EM OUTRO SCRIPT
    # (mantém consistência com restructure_project.sh)
    # ----------------------------------------------------------
    healing_output.txt)
      plan_move "report:logs" "$path" "reports/logs/$file"
      ;;
    integration_test_results.txt)
      plan_move "report:integration" "$path" "reports/integration/$file"
      ;;
    erros.txt)
      plan_move "report:logs" "$path" "reports/logs/$file"
      ;;
    deleted_files_snapshot.txt)
      plan_move "report:audit" "$path" "reports/audit/$file"
      ;;

    # ----------------------------------------------------------
    # RELATÓRIOS DE ONBOARDING
    # ----------------------------------------------------------
    onboarding_report_*.txt)
      plan_move "report:onboarding" "$path" "reports/onboarding/$file"
      ;;

    # ----------------------------------------------------------
    # RELATÓRIOS DE IMPORTAÇÃO / UPDATE
    # ----------------------------------------------------------
    import_update_report_*.json)
      plan_move "report:import_updates" "$path" "reports/import_updates/$file"
      ;;

    # ----------------------------------------------------------
    # RELATÓRIOS DE MIGRAÇÃO E FASE 3
    # ----------------------------------------------------------
    migration_analysis_report.json)
      plan_move "report:migration" "$path" "reports/migration/$file"
      ;;
    phase_3_validation_report.json)
      plan_move "report:phase3" "$path" "reports/phase3/$file"
      ;;
    phase_3_validation_report_formatted.txt)
      plan_move "report:phase3" "$path" "reports/phase3/$file"
      ;;

    # ----------------------------------------------------------
    # RELATÓRIOS DE POLÍTICA / DELTAS
    # ----------------------------------------------------------
    policy_report.json)
      plan_move "report:policy" "$path" "reports/policy/$file"
      ;;
    report_delta.json|report_delta.json.gz)
      plan_move "report:deltas" "$path" "reports/deltas/$file"
      ;;

    *)
      # Outros arquivos da raiz são ignorados por este script,
      # exceto documentação quando --include-docs estiver ativo
      if [ "$INCLUDE_DOCS" = true ]; then
        case "$file" in
          # ------------------------------------------------------
          # DOCUMENTAÇÃO: ETAPAS 5 e 6
          # ------------------------------------------------------
          ETAPA_5*)
            plan_move "docs:etapa_5" "$path" "docs/etapas/etapa_5/$file"
            ;;
          ETAPA_6*|INDICE_ETAPA_6.*|.ETAPA_6*|README_ETAPA_6.*)
            plan_move "docs:etapa_6" "$path" "docs/etapas/etapa_6/$file"
            ;;

          # ------------------------------------------------------
          # DOCUMENTAÇÃO: FASE 3 / ENTREGAS
          # ------------------------------------------------------
          FASE_3*|ENTREGA_FASE_3*|MANIFESTO_ENTREGA_FASE_3.*|ENTREGA_COMPLETA_INTEGRATION_PHASE3.*|README_FASE_3.*)
            plan_move "docs:fase_3" "$path" "docs/fase_3/$file"
            ;;

          # ------------------------------------------------------
          # DOCUMENTAÇÃO: MIGRAÇÃO
          # ------------------------------------------------------
          MIGRATION_*.md|README_MIGRATION.*)
            plan_move "docs:migration" "$path" "docs/migration/$file"
            ;;

          # ------------------------------------------------------
          # DOCUMENTAÇÃO: GUIAS INICIAIS / ONBOARDING
          # ------------------------------------------------------
          00_LEIA_PRIMEIRO.*|LEIA_PRIMEIRO.*|COMECE_AQUI.*|START_HERE.*|QUICK_START.*|QUICKSTART_CARD.*|START_DOCUMENTATION.*|SETUP_NOVO_DEV.*|GUIA_PARA_LEIGOS.*|ENV_SETUP.*|CARTAO_DE_REFERENCIA.*|PROXIMO_PASSO.*)
            plan_move "docs:getting_started" "$path" "docs/getting_started/$file"
            ;;

          # ------------------------------------------------------
          # DOCUMENTAÇÃO: COMANDOS / ÍNDICES / PROJECTAGENT
          # ------------------------------------------------------
          MASTER_COMMAND_INDEX.*|MASTER_INDEX_USAGE.*|COMMAND_REFERENCE_CARD.*|COMMAND_VALIDATION_REPORT.*|PROJECT_COMMANDS_ORGANIZED.*|README_MASTER_INDEX.*|README_PROJECTAGENT.*|PROJECTAGENT_SUMMARY.*)
            plan_move "docs:commands" "$path" "docs/commands/$file"
            ;;

          # ------------------------------------------------------
          # DOCUMENTAÇÃO: STATUS / RESUMOS / ENTREGA
          # ------------------------------------------------------
          STATUS_CONSOLIDADO.*|FINAL_SUMMARY.*|DELIVERY_MANIFEST.*|DELIVERY_SUMMARY_TXT.*|INDICE_COMPLETO_ENTREGA.*|ENTREGA_FINAL.*|PATHS_CORRECTIONS_SUMMARY.*|PATH_CORRECTIONS_REPORT.*|VARIABLE_NORMALIZATION_PLAN.*)
            plan_move "docs:status" "$path" "docs/status/$file"
            ;;

          # ------------------------------------------------------
          # DOCUMENTAÇÃO: FERRAMENTAS / PRE-COMMIT / GIT
          # ------------------------------------------------------
          README_PRECOMMIT.*|GIT_CLEANUP_LOG.*)
            plan_move "docs:tooling" "$path" "docs/tooling/$file"
            ;;

          # ------------------------------------------------------
          # DOCUMENTAÇÃO: INTEGRATION VALIDATOR
          # ------------------------------------------------------
          INTEGRATION_VALIDATOR_*|README_INTEGRATION_VALIDATOR.*|QUICK_START_INTEGRATION_VALIDATOR.*)
            plan_move "docs:integration_validator" "$path" "docs/integration_validator/$file"
            ;;

          # ------------------------------------------------------
          # DOCUMENTAÇÃO: NGINX / DOCKER NGINX
          # ------------------------------------------------------
          NGINX_*|DOCKER_COMPOSE_NGINX.*)
            plan_move "docs:nginx" "$path" "docs/nginx/$file"
            ;;

          # ------------------------------------------------------
          # DOCUMENTAÇÃO: NAVEGAÇÃO / ESTRUTURA
          # ------------------------------------------------------
          NAVIGATION_INDEX.*)
            plan_move "docs:navigation" "$path" "docs/navigation/$file"
            ;;
          .tree-*.md)
            plan_move "docs:structure" "$path" "docs/structure/$file"
            ;;

          *)
            :
            ;;
        esac
      fi
      ;;
  esac

done

echo "" >> "$PLAN_FILE"
echo "Total planned moves: $PLANNED_MOVES" >> "$PLAN_FILE"

echo
if [ "$PLANNED_MOVES" -eq 0 ]; then
  log_warn "Nenhum arquivo elegível encontrado na raiz para reorganização (logs/reports)."
else
  log_success "Plano gerado com $PLANNED_MOVES movimentações planejadas."
  log_info "Veja o plano detalhado em: $PLAN_FILE"
fi

if [ "$APPLY" = true ]; then
  log_success "Reorganização aplicada. Recomenda-se revisar com: git status"
else
  log_info "Modo DRY-RUN: nenhum arquivo foi movido."
  log_info "Se o plano estiver OK, execute novamente com: $0 --apply"
fi

exit 0
