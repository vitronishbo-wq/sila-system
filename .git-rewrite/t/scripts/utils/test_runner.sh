#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

LOG_ROOT="$ROOT_DIR/logs/tests"
TIMESTAMP="$(date +'%Y%m%d_%H%M%S')"
LOG_DIR="$LOG_ROOT/$TIMESTAMP"

mkdir -p "$LOG_DIR"

log() {
  local level="$1"; shift
  echo "[$level] $*"
}

run_test() {
  local cmd="$1"
  local name="$2"
  local log_file="$LOG_DIR/$name.log"

  log "INFO" "Executando $name..."
  if bash -c "$cmd" &> "$log_file"; then
    log "INFO" "✅ $name OK (log: $log_file)"
  else
    log "ERROR" "❌ $name falhou (veja: $log_file)"
  fi
}

run_test "cd \"$ROOT_DIR\" && bash scripts/dev/project_analyzer.sh"                 "project-analyzer"
run_test "cd \"$ROOT_DIR\" && bash scripts/dev/master-index.sh quick --dry --json" "master-index-quick"

log "INFO" "Testes concluídos. Logs em: $LOG_DIR"
