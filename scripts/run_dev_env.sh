#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UTILS_DIR="$SCRIPT_DIR/utils"

log_info()  { echo -e "[INFO] $*"; }
log_warn()  { echo -e "[WARN] $*"; }
log_error() { echo -e "[ERROR] $*" >&2; }

if [[ ! -d "$UTILS_DIR" ]]; then
  log_error "Diretório de utils não encontrado: $UTILS_DIR"
  exit 1
fi

DEV_SETUP_SH="$UTILS_DIR/dev_setup.sh"
TEST_RUNNER_SH="$UTILS_DIR/test_runner.sh"

if [[ ! -f "$DEV_SETUP_SH" ]]; then
  log_error "Script de setup não encontrado: $DEV_SETUP_SH"
  exit 1
fi

if [[ ! -f "$TEST_RUNNER_SH" ]]; then
  log_warn "Script de testes não encontrado: $TEST_RUNNER_SH"
fi

case "$OSTYPE" in
  linux-gnu*|darwin*)
    log_info "Sistema suportado ($OSTYPE). Iniciando setup..."
    ;;
  *)
    log_error "Sistema não suportado neste shell script ($OSTYPE). Use PowerShell no Windows."
    exit 1
    ;;
esac

bash "$DEV_SETUP_SH"

if [[ -f "$TEST_RUNNER_SH" ]]; then
  bash "$TEST_RUNNER_SH"
else
  log_warn "Pulo execução de testes (test_runner.sh não disponível)."
fi

log_info "Fluxo run_dev_env.sh concluído com sucesso."
