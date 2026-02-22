#!/bin/bash
set -euo pipefail
SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MIGRATED=0
FAILED=0
SCRIPTS_TO_MIGRATE=(
    "infra/nginx_automation.sh"
    "infra/nginx_monitor.sh"
    "core/sila_start.sh"
    "setup/init_live_session.sh"
    "migration/execute_auth_migration.sh"
    "migration/prepare_migration.sh"
    "infra/install_vsc_extensions.sh"
    "maintenance/cleanup_temp_files.sh"
    "infra/nginx_diagnostic.sh"
)
is_migrated() {
    local script="$1"
    if grep -q "source.*lib/logging.sh" "$script" 2>/dev/null; then
        return 0
    else
        return 1
    fi
}
migrate_script() {
    local script="$1"
    local full_path="$SCRIPTS_DIR/$script"
    if [ ! -f "$full_path" ]; then
        ((FAILED++))
        return 1
    fi
    if is_migrated "$full_path"; then
        return 0
    fi
    cp "$full_path" "$full_path.bak"
    {
        head -1 "$full_path"
        echo ""
        echo 'SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"'
        echo 'source "$SCRIPT_DIR/../lib/colors.sh"'
        echo 'source "$SCRIPT_DIR/../lib/logging.sh"'
        echo 'export POSTGRES_PASSWORD=Trumanmarcelo_1983'
        echo 'export DATABASE_URL="postgresql+asyncpg://sila_user:Trumanmarcelo_1983@db:5432/sila_db"'
        echo ""
        tail -n +2 "$full_path" | grep -v "^RED=" | grep -v "^GREEN=" | grep -v "^BLUE=" | grep -v "^YELLOW=" | grep -v "^CYAN=" | grep -v "^MAGENTA=" | grep -v "^BOLD=" | grep -v "^NC=" | grep -v "^# Cores" | grep -v "^# Definições de cores" | grep -v "^log()" | grep -v "^success()" | grep -v "^error()" | grep -v "^warn()" | grep -v "^info()" | grep -v "^section()"
    } > "$full_path.tmp"
    mv "$full_path.tmp" "$full_path"
    ((MIGRATED++))
    return 0
}
for script in "${SCRIPTS_TO_MIGRATE[@]}"; do
    migrate_script "$script"
done
if [ $FAILED -eq 0 ]; then
    exit 0
else
    exit 1
fi