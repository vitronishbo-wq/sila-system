#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
DB_SERVICE_NAME="${DB_SERVICE_NAME:-db}"

compose_service_is_running() {
    local compose_file="$1"

    [[ -f "$compose_file" ]] || return 1
    docker compose -f "$compose_file" ps -q "$DB_SERVICE_NAME" 2>/dev/null | grep -q .
}

select_compose_context() {
    local devcontainer_compose="$ROOT_DIR/.devcontainer/docker-compose.yml"
    local infra_compose="$ROOT_DIR/infra/docker-compose.yml"
    local infra_override="$ROOT_DIR/infra/docker-compose.override.yml"

    COMPOSE_FILES=()

    if [[ -n "${SILA_DB_COMPOSE_CONTEXT:-}" ]]; then
        case "$SILA_DB_COMPOSE_CONTEXT" in
            devcontainer)
                COMPOSE_FILES=("$devcontainer_compose")
                ;;
            infra)
                COMPOSE_FILES=("$infra_compose")
                [[ -f "$infra_override" ]] && COMPOSE_FILES+=("$infra_override")
                ;;
            *)
                echo "❌ SILA_DB_COMPOSE_CONTEXT deve ser 'devcontainer' ou 'infra'." >&2
                return 1
                ;;
        esac
    elif [[ -n "${SILA_DB_COMPOSE_FILE:-}" ]]; then
        COMPOSE_FILES=("$SILA_DB_COMPOSE_FILE")
    elif compose_service_is_running "$devcontainer_compose"; then
        COMPOSE_FILES=("$devcontainer_compose")
    elif compose_service_is_running "$infra_compose"; then
        COMPOSE_FILES=("$infra_compose")
        [[ -f "$infra_override" ]] && COMPOSE_FILES+=("$infra_override")
    elif [[ -f "$devcontainer_compose" ]]; then
        COMPOSE_FILES=("$devcontainer_compose")
    elif [[ -f "$infra_compose" ]]; then
        COMPOSE_FILES=("$infra_compose")
        [[ -f "$infra_override" ]] && COMPOSE_FILES+=("$infra_override")
    else
        echo "❌ Nenhum docker compose com serviço '$DB_SERVICE_NAME' foi encontrado." >&2
        return 1
    fi

    for compose_file in "${COMPOSE_FILES[@]}"; do
        if [[ ! -f "$compose_file" ]]; then
            echo "❌ Arquivo docker compose não encontrado: $compose_file" >&2
            return 1
        fi
    done

    COMPOSE_CMD=(docker compose)
    for compose_file in "${COMPOSE_FILES[@]}"; do
        COMPOSE_CMD+=(-f "$compose_file")
    done
}

db_container_id() {
    "${COMPOSE_CMD[@]}" ps -a -q "$DB_SERVICE_NAME" 2>/dev/null | head -n 1
}

db_data_volume_name() {
    local container_id="${1:-$(db_container_id)}"

    [[ -n "$container_id" ]] || return 0

    docker inspect \
        --format '{{range .Mounts}}{{if eq .Destination "/var/lib/postgresql/data"}}{{.Name}}{{end}}{{end}}' \
        "$container_id"
}

wait_for_db_ready() {
    local retries="${1:-30}"
    local sleep_seconds="${2:-2}"
    local db_user="${POSTGRES_USER:-sila_user}"
    local db_name="${POSTGRES_DB:-sila_db}"
    local attempt=1

    while (( attempt <= retries )); do
        if "${COMPOSE_CMD[@]}" exec -T "$DB_SERVICE_NAME" pg_isready -U "$db_user" -d "$db_name" >/dev/null 2>&1; then
            return 0
        fi

        sleep "$sleep_seconds"
        attempt=$((attempt + 1))
    done

    echo "❌ PostgreSQL não ficou pronto a tempo." >&2
    return 1
}

select_compose_context

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    printf '%s\n' "${COMPOSE_FILES[@]}"
fi
