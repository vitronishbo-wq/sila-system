#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

MODE="${1:-${ENV_MODE:-auto}}"
OUTPUT_MODE="${2:-exports}"

detect_mode() {
  if [[ "$MODE" != "auto" ]]; then
    return
  fi

  if [[ -f "/.dockerenv" ]] || grep -qaE '(docker|containerd)' /proc/1/cgroup 2>/dev/null; then
    MODE="docker"
  else
    MODE="host"
  fi
}

resolve_env_file() {
  local candidate
  for candidate in \
    "$PROJECT_ROOT/.env.$MODE" \
    "$PROJECT_ROOT/.env.$MODE.example"
  do
    if [[ -f "$candidate" ]]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done

  echo "Nenhum arquivo .env para o modo '$MODE' foi encontrado." >&2
  return 1
}

capture_env_overrides() {
  OVERRIDE_KEYS=(
    POSTGRES_USER
    POSTGRES_PASSWORD
    POSTGRES_DB
    POSTGRES_HOST
    POSTGRES_PORT
    DB_USER
    DB_PASSWORD
    DB_NAME
    DB_HOST
    DB_PORT
    DATABASE_URL
    ASYNC_DATABASE_URL
    REDIS_HOST
    REDIS_PORT
    REDIS_DB
    REDIS_URL
    CELERY_BROKER_URL
    CELERY_RESULT_BACKEND
    API_HOST
    API_PORT
    FRONTEND_HOST
    FRONTEND_PORT
    GMX_API_PORT
    GMX_FRONTEND_PORT
    VITE_API_PORT
    VITE_API_URL
    LOCAL_BASE_HOST
    BRIDGE_BASE_HOST
    LOCAL_API_BASE_URL
    LOCAL_API_DOCS_URL
    LOCAL_API_HEALTH_URL
    LOCAL_FRONTEND_URL
    BRIDGE_API_BASE_URL
    BRIDGE_API_DOCS_URL
    BRIDGE_API_HEALTH_URL
    BRIDGE_FRONTEND_URL
    GMX_URL_PRIORITY
    GMX_URL_DEBUG
    GMX_URL_TIMEOUT_SECONDS
    WATCHFILES_FORCE_POLLING
    MAX_STARTUP_RETRIES
    STARTUP_RETRY_DELAY_SECONDS
  )

  OVERRIDE_SET_KEYS=()
  for key in "${OVERRIDE_KEYS[@]}"; do
    if [[ -v $key ]]; then
      OVERRIDE_SET_KEYS+=("$key")
      printf -v "OVERRIDE_VALUE_$key" '%s' "${!key}"
    fi
  done
}

restore_env_overrides() {
  local key=""
  local saved_var=""
  for key in "${OVERRIDE_SET_KEYS[@]}"; do
    saved_var="OVERRIDE_VALUE_$key"
    export "$key=${!saved_var}"
  done
}

normalize_env() {
  export GMX_ENV_LOADED=1
  export GMX_ENV_SOURCE="load_runtime_env.sh:$MODE"
  export ENV_MODE="$MODE"
  export POSTGRES_USER="${POSTGRES_USER:-sila_user}"
  export POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-Trumanmarcelo_1983}"
  export POSTGRES_DB="${POSTGRES_DB:-sila_db}"
  export POSTGRES_PORT="${POSTGRES_PORT:-5432}"
  export POSTGRES_HOST="${POSTGRES_HOST:-$([[ "$MODE" == "docker" ]] && echo db || echo 127.0.0.1)}"

  export DB_USER="${DB_USER:-$POSTGRES_USER}"
  export DB_PASSWORD="${DB_PASSWORD:-$POSTGRES_PASSWORD}"
  export DB_NAME="${DB_NAME:-$POSTGRES_DB}"
  export DB_PORT="${DB_PORT:-$POSTGRES_PORT}"
  export DB_HOST="${DB_HOST:-$POSTGRES_HOST}"

  export REDIS_PORT="${REDIS_PORT:-6379}"
  export REDIS_DB="${REDIS_DB:-0}"
  export REDIS_HOST="${REDIS_HOST:-$([[ "$MODE" == "docker" ]] && echo redis || echo 127.0.0.1)}"
  export REDIS_URL="${REDIS_URL:-redis://$REDIS_HOST:$REDIS_PORT/$REDIS_DB}"
  export CELERY_BROKER_URL="${CELERY_BROKER_URL:-$REDIS_URL}"
  export CELERY_RESULT_BACKEND="${CELERY_RESULT_BACKEND:-$REDIS_URL}"

  local async_database_url="postgresql+asyncpg://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB"
  export DATABASE_URL="${DATABASE_URL:-$async_database_url}"
  export ASYNC_DATABASE_URL="${ASYNC_DATABASE_URL:-$DATABASE_URL}"

  export API_HOST="${API_HOST:-127.0.0.1}"
  export API_PORT="${API_PORT:-8000}"
  export FRONTEND_HOST="${FRONTEND_HOST:-127.0.0.1}"
  export FRONTEND_PORT="${FRONTEND_PORT:-3000}"
  export GMX_API_PORT="${GMX_API_PORT:-$API_PORT}"
  export GMX_FRONTEND_PORT="${GMX_FRONTEND_PORT:-$FRONTEND_PORT}"
  export VITE_API_PORT="${VITE_API_PORT:-$GMX_API_PORT}"
  export VITE_API_URL="${VITE_API_URL:-http://127.0.0.1:$GMX_API_PORT/api/v1}"
  export LOCAL_BASE_HOST="${LOCAL_BASE_HOST:-localhost}"
  export BRIDGE_BASE_HOST="${BRIDGE_BASE_HOST:-host.docker.internal}"
  export LOCAL_API_BASE_URL="${LOCAL_API_BASE_URL:-http://$LOCAL_BASE_HOST:$GMX_API_PORT}"
  export LOCAL_API_DOCS_URL="${LOCAL_API_DOCS_URL:-$LOCAL_API_BASE_URL/docs}"
  export LOCAL_API_HEALTH_URL="${LOCAL_API_HEALTH_URL:-$LOCAL_API_BASE_URL/api/health}"
  export LOCAL_FRONTEND_URL="${LOCAL_FRONTEND_URL:-http://$LOCAL_BASE_HOST:$GMX_FRONTEND_PORT}"
  export BRIDGE_API_BASE_URL="${BRIDGE_API_BASE_URL:-http://$BRIDGE_BASE_HOST:$GMX_API_PORT}"
  export BRIDGE_API_DOCS_URL="${BRIDGE_API_DOCS_URL:-$BRIDGE_API_BASE_URL/docs}"
  export BRIDGE_API_HEALTH_URL="${BRIDGE_API_HEALTH_URL:-$BRIDGE_API_BASE_URL/api/health}"
  export BRIDGE_FRONTEND_URL="${BRIDGE_FRONTEND_URL:-http://$BRIDGE_BASE_HOST:$GMX_FRONTEND_PORT}"
  export GMX_URL_PRIORITY="${GMX_URL_PRIORITY:-local,bridge}"
  export GMX_URL_DEBUG="${GMX_URL_DEBUG:-0}"
  export GMX_URL_TIMEOUT_SECONDS="${GMX_URL_TIMEOUT_SECONDS:-2}"
  export WATCHFILES_FORCE_POLLING="${WATCHFILES_FORCE_POLLING:-$([[ "$MODE" == "host" ]] && echo true || echo false)}"
  export MAX_STARTUP_RETRIES="${MAX_STARTUP_RETRIES:-60}"
  export STARTUP_RETRY_DELAY_SECONDS="${STARTUP_RETRY_DELAY_SECONDS:-1}"
}

print_debug_env() {
  env | grep -E '^(ENV_MODE|GMX_|POSTGRES_|DB_|DATABASE_URL|ASYNC_DATABASE_URL|REDIS_|CELERY_|API_HOST|API_PORT|FRONTEND_HOST|FRONTEND_PORT|VITE_API_PORT|VITE_API_URL|LOCAL_|BRIDGE_|WATCHFILES_FORCE_POLLING|MAX_STARTUP_RETRIES|STARTUP_RETRY_DELAY_SECONDS)=' | sort >&2
}

print_exports() {
  printf 'export GMX_ENV_LOADED=%q\n' "$GMX_ENV_LOADED"
  printf 'export GMX_ENV_SOURCE=%q\n' "$GMX_ENV_SOURCE"
  printf 'export ENV_MODE=%q\n' "$ENV_MODE"
  printf 'export POSTGRES_USER=%q\n' "$POSTGRES_USER"
  printf 'export POSTGRES_PASSWORD=%q\n' "$POSTGRES_PASSWORD"
  printf 'export POSTGRES_DB=%q\n' "$POSTGRES_DB"
  printf 'export POSTGRES_HOST=%q\n' "$POSTGRES_HOST"
  printf 'export POSTGRES_PORT=%q\n' "$POSTGRES_PORT"
  printf 'export DB_USER=%q\n' "$DB_USER"
  printf 'export DB_PASSWORD=%q\n' "$DB_PASSWORD"
  printf 'export DB_NAME=%q\n' "$DB_NAME"
  printf 'export DB_HOST=%q\n' "$DB_HOST"
  printf 'export DB_PORT=%q\n' "$DB_PORT"
  printf 'export DATABASE_URL=%q\n' "$DATABASE_URL"
  printf 'export ASYNC_DATABASE_URL=%q\n' "$ASYNC_DATABASE_URL"
  printf 'export REDIS_HOST=%q\n' "$REDIS_HOST"
  printf 'export REDIS_PORT=%q\n' "$REDIS_PORT"
  printf 'export REDIS_DB=%q\n' "$REDIS_DB"
  printf 'export REDIS_URL=%q\n' "$REDIS_URL"
  printf 'export CELERY_BROKER_URL=%q\n' "$CELERY_BROKER_URL"
  printf 'export CELERY_RESULT_BACKEND=%q\n' "$CELERY_RESULT_BACKEND"
  printf 'export API_HOST=%q\n' "$API_HOST"
  printf 'export API_PORT=%q\n' "$API_PORT"
  printf 'export FRONTEND_HOST=%q\n' "$FRONTEND_HOST"
  printf 'export FRONTEND_PORT=%q\n' "$FRONTEND_PORT"
  printf 'export GMX_API_PORT=%q\n' "$GMX_API_PORT"
  printf 'export GMX_FRONTEND_PORT=%q\n' "$GMX_FRONTEND_PORT"
  printf 'export VITE_API_PORT=%q\n' "$VITE_API_PORT"
  printf 'export VITE_API_URL=%q\n' "$VITE_API_URL"
  printf 'export LOCAL_BASE_HOST=%q\n' "$LOCAL_BASE_HOST"
  printf 'export BRIDGE_BASE_HOST=%q\n' "$BRIDGE_BASE_HOST"
  printf 'export LOCAL_API_BASE_URL=%q\n' "$LOCAL_API_BASE_URL"
  printf 'export LOCAL_API_DOCS_URL=%q\n' "$LOCAL_API_DOCS_URL"
  printf 'export LOCAL_API_HEALTH_URL=%q\n' "$LOCAL_API_HEALTH_URL"
  printf 'export LOCAL_FRONTEND_URL=%q\n' "$LOCAL_FRONTEND_URL"
  printf 'export BRIDGE_API_BASE_URL=%q\n' "$BRIDGE_API_BASE_URL"
  printf 'export BRIDGE_API_DOCS_URL=%q\n' "$BRIDGE_API_DOCS_URL"
  printf 'export BRIDGE_API_HEALTH_URL=%q\n' "$BRIDGE_API_HEALTH_URL"
  printf 'export BRIDGE_FRONTEND_URL=%q\n' "$BRIDGE_FRONTEND_URL"
  printf 'export GMX_URL_PRIORITY=%q\n' "$GMX_URL_PRIORITY"
  printf 'export GMX_URL_DEBUG=%q\n' "$GMX_URL_DEBUG"
  printf 'export GMX_URL_TIMEOUT_SECONDS=%q\n' "$GMX_URL_TIMEOUT_SECONDS"
  printf 'export WATCHFILES_FORCE_POLLING=%q\n' "$WATCHFILES_FORCE_POLLING"
  printf 'export MAX_STARTUP_RETRIES=%q\n' "$MAX_STARTUP_RETRIES"
  printf 'export STARTUP_RETRY_DELAY_SECONDS=%q\n' "$STARTUP_RETRY_DELAY_SECONDS"
}

print_summary() {
  cat <<EOF
ENV_MODE=$ENV_MODE
ENV_FILE=$ENV_FILE
GMX_ENV_LOADED=$GMX_ENV_LOADED
GMX_ENV_SOURCE=$GMX_ENV_SOURCE
POSTGRES_HOST=$POSTGRES_HOST
POSTGRES_PORT=$POSTGRES_PORT
DATABASE_URL=$DATABASE_URL
REDIS_HOST=$REDIS_HOST
REDIS_PORT=$REDIS_PORT
REDIS_URL=$REDIS_URL
API_PORT=$API_PORT
FRONTEND_PORT=$FRONTEND_PORT
GMX_API_PORT=$GMX_API_PORT
GMX_FRONTEND_PORT=$GMX_FRONTEND_PORT
VITE_API_PORT=$VITE_API_PORT
VITE_API_URL=$VITE_API_URL
LOCAL_BASE_HOST=$LOCAL_BASE_HOST
BRIDGE_BASE_HOST=$BRIDGE_BASE_HOST
LOCAL_API_DOCS_URL=$LOCAL_API_DOCS_URL
LOCAL_API_HEALTH_URL=$LOCAL_API_HEALTH_URL
LOCAL_FRONTEND_URL=$LOCAL_FRONTEND_URL
BRIDGE_API_DOCS_URL=$BRIDGE_API_DOCS_URL
BRIDGE_API_HEALTH_URL=$BRIDGE_API_HEALTH_URL
BRIDGE_FRONTEND_URL=$BRIDGE_FRONTEND_URL
GMX_URL_PRIORITY=$GMX_URL_PRIORITY
GMX_URL_DEBUG=$GMX_URL_DEBUG
GMX_URL_TIMEOUT_SECONDS=$GMX_URL_TIMEOUT_SECONDS
WATCHFILES_FORCE_POLLING=$WATCHFILES_FORCE_POLLING
MAX_STARTUP_RETRIES=$MAX_STARTUP_RETRIES
STARTUP_RETRY_DELAY_SECONDS=$STARTUP_RETRY_DELAY_SECONDS
EOF
}

detect_mode

case "$MODE" in
  host|docker) ;;
  *)
    echo "Modo inválido: '$MODE'. Use host, docker ou auto." >&2
    exit 1
    ;;
esac

ENV_FILE="$(resolve_env_file)"
capture_env_overrides
set -a
source "$ENV_FILE"
set +a
restore_env_overrides
normalize_env

if [[ "${ENV_DEBUG:-0}" == "1" ]]; then
  print_debug_env
fi

case "$OUTPUT_MODE" in
  exports)
    print_exports
    ;;
  --print|print|summary)
    print_summary
    ;;
  *)
    echo "Formato de saída inválido: '$OUTPUT_MODE'." >&2
    exit 1
    ;;
esac
