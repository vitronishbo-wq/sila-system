#!/usr/bin/env bash
set -euo pipefail

# 🧹 SILA Root Scripts Consolidation
#
# Consolida os scripts de orquestração e manutenção que ainda estão na raiz
# do repositório, movendo-os para pastas semânticas sob scripts/ via git mv.
#
# - Por padrão roda em modo DRY-RUN (só imprime o que faria).
# - Use --apply para efetivamente executar os git mv.
#
# Uso:
#   bash scripts/maintenance/consolidate_root_scripts.sh          # dry-run
#   bash scripts/maintenance/consolidate_root_scripts.sh --apply  # aplica git mv

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${ROOT_DIR}"

DRY_RUN=1
if [[ "${1:-}" == "--apply" ]]; then
  DRY_RUN=0
fi

# Garante que as pastas de destino existem
mkdir -p scripts/orchestration scripts/bootstrap scripts/maintenance

# Mapeamento explícito de scripts da raiz → destino interno
# Cada linha: "origem destino"
read -r -d '' SCRIPT_MAP << 'EOF'
abrir-windsurf.sh scripts/orchestration/abrir-windsurf.sh
advanced_project_analyzer.sh scripts/maintenance/advanced_project_analyzer.sh
changelog_auto.sh scripts/maintenance/changelog_auto.sh
clean_pendrive_safe.sh scripts/maintenance/clean_pendrive_safe.sh
cleanup_all_backups.sh scripts/maintenance/cleanup_all_backups.sh
cleanup_obsolete.sh scripts/maintenance/cleanup_obsolete.sh
cleanup_project.sh scripts/maintenance/cleanup_project.sh
cleanup_temp_files.sh scripts/maintenance/cleanup_temp_files.sh
complete_env.sh scripts/bootstrap/complete_env.sh
execute_auth_migration.sh scripts/orchestration/execute_auth_migration.sh
get-docker.sh scripts/bootstrap/get-docker.sh
init_database.sh scripts/bootstrap/init_database.sh
init_live_session.sh scripts/orchestration/init_live_session.sh
install_vsc_extensions.sh scripts/bootstrap/install_vsc_extensions.sh
make_executable.sh scripts/maintenance/make_executable.sh
monitor_sila.sh scripts/orchestration/monitor_sila.sh
nginx_automation.sh scripts/orchestration/nginx_automation.sh
nginx_diagnostic.sh scripts/maintenance/nginx_diagnostic.sh
nginx_monitor.sh scripts/orchestration/nginx_monitor.sh
prepare_environment.sh scripts/bootstrap/prepare_environment.sh
prepare_migration.sh scripts/orchestration/prepare_migration.sh
project_analyzer.sh scripts/maintenance/project_analyzer.sh
quick_deploy.sh scripts/orchestration/quick_deploy.sh
repair_all_runner.sh scripts/maintenance/repair_all_runner.sh
repair_all_simple.sh scripts/maintenance/repair_all_simple.sh
restructure_project.sh scripts/maintenance/restructure_project.sh
run_with_pythonpath.sh scripts/bootstrap/run_with_pythonpath.sh
sila.sh scripts/orchestration/sila.sh
sila_config.sh scripts/bootstrap/sila_config.sh
sila_start.sh scripts/orchestration/sila_start.sh
sila_stop.sh scripts/orchestration/sila_stop.sh
simple_test.sh scripts/testing/simple_test.sh
smoke-test.sh scripts/testing/smoke-test.sh
start_sila.sh scripts/orchestration/start_sila.sh
status_sila.sh scripts/orchestration/status_sila.sh
test_start_backend.sh scripts/testing/test_start_backend.sh
update_comandos.sh scripts/maintenance/update_comandos.sh
validar_dependencias_sila.sh scripts/maintenance/validar_dependencias_sila.sh
EOF

# Garante subpasta de testing também
mkdir -p scripts/testing

echo "🧹 Consolidando scripts da raiz (DRY_RUN=${DRY_RUN})"

while read -r SRC DST; do
  [[ -z "${SRC}" ]] && continue
  # Linha pode ter comentários ou espaços extras
  if [[ "${SRC}" == \#* ]]; then
    continue
  fi

  if [[ ! -f "${SRC}" ]]; then
    echo "⚠️  Ignorando, arquivo não existe na raiz: ${SRC}"
    continue
  fi

  if [[ ${DRY_RUN} -eq 1 ]]; then
    echo "[DRY-RUN] git mv '${SRC}' '${DST}'"
  else
    echo "git mv '${SRC}' '${DST}'"
    git mv "${SRC}" "${DST}"
  fi

done <<< "${SCRIPT_MAP}"

if [[ ${DRY_RUN} -eq 1 ]]; then
  echo "\nℹ️  Nenhuma alteração aplicada (modo dry-run)."
  echo "   Revise o plano e depois rode novamente com --apply."
else
  echo "\n✅ Movimentação aplicada."
  echo "   Use 'git status' e 'git diff --stat' para revisar antes de commitar."
fi
