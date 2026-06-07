#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
COMPOSE_FILE="$PROJECT_ROOT/.devcontainer/docker-compose.yml"
BACKEND_DIR="$PROJECT_ROOT/apps/backend"
FRONTEND_DIR="$PROJECT_ROOT/apps/frontend"
ROOT_VENV="$PROJECT_ROOT/.venv/bin/activate"
ROOT_VENV_BIN="$(dirname "$ROOT_VENV")"
ENV_MODE_INPUT="${ENV_MODE:-auto}"
BACKEND_PID=""
FRONTEND_PID=""
MAX_RETRIES="${MAX_STARTUP_RETRIES:-60}"
RETRY_DELAY_SECONDS="${STARTUP_RETRY_DELAY_SECONDS:-1}"

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Comando obrigatório não encontrado: $1" >&2
    exit 1
  fi
}

docker_available() {
  command -v docker >/dev/null 2>&1
}

tcp_port_open() {
  local host="$1"
  local port="$2"

  timeout 1 bash -lc "exec 3<>/dev/tcp/$host/$port" >/dev/null 2>&1
}

run_compose_service_check() {
  local service_name="$1"
  shift
  docker_available || return 1
  docker compose -f "$COMPOSE_FILE" exec -T "$service_name" "$@"
}

wait_for_postgres() {
  local attempts="${1:-$MAX_RETRIES}"

  for ((i=1; i<=attempts; i++)); do
    if command -v pg_isready >/dev/null 2>&1; then
      if pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" >/dev/null 2>&1; then
        echo "  ✓ PostgreSQL pronto via pg_isready"
        return 0
      fi
    fi

    if tcp_port_open "$DB_HOST" "$DB_PORT"; then
      echo "  ✓ PostgreSQL acessível via TCP em $DB_HOST:$DB_PORT"
      return 0
    elif [[ "$ENV_MODE" == "docker" ]] \
      && run_compose_service_check db pg_isready -h localhost -p 5432 -U "$POSTGRES_USER" -d "$POSTGRES_DB" >/dev/null 2>&1; then
      echo "  ✓ PostgreSQL pronto via pg_isready no container"
      return 0
    fi

    echo "  ⏳ Aguardando PostgreSQL ($i/$attempts)..."
    sleep "$RETRY_DELAY_SECONDS"
  done

  echo "  ✗ Timeout aguardando PostgreSQL" >&2
  if [[ "$ENV_MODE" == "host" ]]; then
    echo "    Dica: inicie o PostgreSQL local em $DB_HOST:$DB_PORT antes de rodar o stack." >&2
  fi
  return 1
}

wait_for_redis() {
  local attempts="${1:-$MAX_RETRIES}"

  for ((i=1; i<=attempts; i++)); do
    if command -v redis-cli >/dev/null 2>&1; then
      if redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" ping 2>/dev/null | grep -q PONG; then
        echo "  ✓ Redis pronto via redis-cli"
        return 0
      fi
    fi

    if tcp_port_open "$REDIS_HOST" "$REDIS_PORT"; then
      echo "  ✓ Redis acessível via TCP em $REDIS_HOST:$REDIS_PORT"
      return 0
    elif [[ "$ENV_MODE" == "docker" ]] \
      && run_compose_service_check redis redis-cli ping 2>/dev/null | grep -q PONG; then
      echo "  ✓ Redis pronto via redis-cli no container"
      return 0
    fi

    echo "  ⏳ Aguardando Redis ($i/$attempts)..."
    sleep "$RETRY_DELAY_SECONDS"
  done

  echo "  ✗ Timeout aguardando Redis" >&2
  if [[ "$ENV_MODE" == "host" ]]; then
    echo "    Dica: inicie o Redis local em $REDIS_HOST:$REDIS_PORT antes de rodar o stack." >&2
  fi
  return 1
}

terminate_process_group() {
  local pid="$1"

  if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
    kill -TERM -- "-$pid" 2>/dev/null || kill -TERM "$pid" 2>/dev/null || true
    wait "$pid" 2>/dev/null || true
  fi
}

cleanup() {
  local exit_code=$1
  trap - EXIT INT TERM

  terminate_process_group "$BACKEND_PID"
  terminate_process_group "$FRONTEND_PID"

  exit "$exit_code"
}

handle_signal() {
  cleanup 130
}

require_command npm
require_command bash
require_command setsid

if [[ ! -f "$ROOT_VENV" ]]; then
  echo "Virtualenv não encontrado em $ROOT_VENV" >&2
  exit 1
fi

eval "$("$PROJECT_ROOT/scripts/dev/load_runtime_env.sh" "$ENV_MODE_INPUT")"

if [[ "$ENV_MODE" == "docker" ]]; then
  require_command docker
  echo "==> Subindo PostgreSQL e Redis via Docker Compose ($ENV_MODE)"
  docker compose -f "$COMPOSE_FILE" up -d db redis
else
  echo "==> Usando PostgreSQL e Redis locais em $DB_HOST:$DB_PORT e $REDIS_HOST:$REDIS_PORT ($ENV_MODE)"
fi

if [[ "${ENV_DEBUG:-0}" == "1" ]]; then
  echo "==> Runtime env debug"
  env | grep -E '^(ENV_MODE|GMX_|POSTGRES_|DB_|DATABASE_URL|ASYNC_DATABASE_URL|REDIS_|CELERY_|API_PORT|FRONTEND_PORT|VITE_API_PORT|VITE_API_URL|WATCHFILES_FORCE_POLLING|MAX_STARTUP_RETRIES|STARTUP_RETRY_DELAY_SECONDS)=' | sort
fi

wait_for_postgres
wait_for_redis

echo "==> Executando migrações"
# shellcheck disable=SC1090
source "$ROOT_VENV"
(
  cd "$BACKEND_DIR"
  alembic upgrade head
)

if [[ ! -d "$FRONTEND_DIR/node_modules" ]]; then
  echo "==> Instalando dependências do frontend"
  (
    cd "$FRONTEND_DIR"
    npm install
  )
fi

trap 'handle_signal' INT TERM

echo "==> Iniciando backend em http://127.0.0.1:$API_PORT"
# Start from repo root so top-level package `apps` is importable
setsid bash -lc "cd '$PROJECT_ROOT' && export PYTHONPATH='$PROJECT_ROOT:$BACKEND_DIR' && exec '$ROOT_VENV_BIN/uvicorn' apps.backend.app.main:app --host 0.0.0.0 --port '$API_PORT' --reload --reload-dir '$BACKEND_DIR'" &
BACKEND_PID=$!

echo "==> Iniciando frontend em http://127.0.0.1:$FRONTEND_PORT"
setsid bash -lc "cd '$FRONTEND_DIR' && exec npm run dev" &
FRONTEND_PID=$!

echo ""
echo "Frontend: http://localhost:$FRONTEND_PORT"
echo "Backend:  http://localhost:$API_PORT/docs"
echo "Modo:     $ENV_MODE"
echo ""

set +e
wait -n "$BACKEND_PID" "$FRONTEND_PID"
EXIT_CODE=$?
set -e

cleanup "$EXIT_CODE"
