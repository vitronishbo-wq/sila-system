#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_MODE_INPUT="${ENV_MODE:-auto}"

if [[ "${1:-}" == "host" || "${1:-}" == "docker" || "${1:-}" == "auto" ]]; then
  ENV_MODE_INPUT="$1"
fi

detect_runtime_label() {
  if [[ -f "/.dockerenv" ]]; then
    echo "container"
    return
  fi
  if grep -qi microsoft /proc/version 2>/dev/null; then
    echo "wsl"
    return
  fi
  echo "linux"
}

trim_container_rows() {
  if [[ -z "${1:-}" ]]; then
    return 0
  fi

  awk 'BEGIN { FS="\t" } /^docker-/ { print; found=1 } END { exit found ? 0 : 1 }' <<<"$1"
}

classify_container() {
  local name="$1"

  case "$name" in
    *celery*)
      printf 'worker'
      ;;
    *db*|*redis*|*proxy*)
      printf 'infra'
      ;;
    *edge*)
      printf 'edge'
      ;;
    *api*)
      printf 'api'
      ;;
    *)
      printf 'other'
      ;;
  esac
}

probe_api_health() {
  local api_base_url="$1"
  local health_url=""
  local raw=""
  local candidate=""
  local candidates=(
    "$api_base_url/api/health"
    "$api_base_url/api/health/live"
    "$api_base_url/system/health"
    "$api_base_url/health"
  )

  if ! command -v curl >/dev/null 2>&1; then
    printf 'unknown|curl indisponivel|%s\n' "${candidates[0]}"
    return 0
  fi

  for candidate in "${candidates[@]}"; do
    raw="$(curl -fsS --max-time "${GMX_URL_TIMEOUT_SECONDS:-2}" "$candidate" 2>/dev/null || true)"
    if [[ -n "$raw" ]]; then
      health_url="$candidate"
      break
    fi
  done

  if [[ -z "$raw" ]]; then
    printf 'down||%s\n' "${candidates[0]}"
    return 0
  fi

  if grep -Eq '"status"[[:space:]]*:[[:space:]]*"(ok|ready|healthy)"' <<<"$raw" \
    || grep -Eq '"alive"[[:space:]]*:[[:space:]]*true' <<<"$raw"; then
    printf 'ok|%s|%s\n' "$raw" "$health_url"
    return 0
  fi

  printf 'degraded|%s|%s\n' "$raw" "$health_url"
}

eval "$("$PROJECT_ROOT/scripts/dev/load_runtime_env.sh" "$ENV_MODE_INPUT")"

RUNTIME_LABEL="$(detect_runtime_label)"
ACTIVE_API_DOCS_URL="$("$PROJECT_ROOT/scripts/dev/print_runtime_urls.sh" "$ENV_MODE" --active-api 2>/dev/null || true)"
ACTIVE_API_BASE_URL="$("$PROJECT_ROOT/scripts/dev/print_runtime_urls.sh" "$ENV_MODE" --active-api-base 2>/dev/null || true)"
ACTIVE_API_LABEL="$("$PROJECT_ROOT/scripts/dev/print_runtime_urls.sh" "$ENV_MODE" --active-api-label 2>/dev/null || true)"
ACTIVE_API_TIME="$("$PROJECT_ROOT/scripts/dev/print_runtime_urls.sh" "$ENV_MODE" --active-api-time 2>/dev/null || true)"
ACTIVE_FRONTEND_URL="$("$PROJECT_ROOT/scripts/dev/print_runtime_urls.sh" "$ENV_MODE" --active-frontend 2>/dev/null || true)"

IFS='|' read -r API_HEALTH_STATUS API_HEALTH_BODY API_HEALTH_URL < <(
  probe_api_health "${ACTIVE_API_BASE_URL:-$LOCAL_API_BASE_URL}"
)

ALL_CONTAINERS="$(docker ps --format '{{.Names}}\t{{.Status}}\t{{.Ports}}' 2>/dev/null || true)"
STACK_CONTAINERS="$(trim_container_rows "$ALL_CONTAINERS" 2>/dev/null || printf '%s\n' "$ALL_CONTAINERS")"

API_COUNT=0
WORKER_COUNT=0
INFRA_COUNT=0
EDGE_COUNT=0
OTHER_COUNT=0
TOTAL_COUNT=0
CONTAINER_LINES=""

if [[ -n "$STACK_CONTAINERS" ]]; then
  while IFS=$'\t' read -r name status ports; do
    [[ -z "$name" ]] && continue
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    role="$(classify_container "$name")"
    case "$role" in
      api) API_COUNT=$((API_COUNT + 1)) ;;
      worker) WORKER_COUNT=$((WORKER_COUNT + 1)) ;;
      infra) INFRA_COUNT=$((INFRA_COUNT + 1)) ;;
      edge) EDGE_COUNT=$((EDGE_COUNT + 1)) ;;
      *) OTHER_COUNT=$((OTHER_COUNT + 1)) ;;
    esac
    CONTAINER_LINES="${CONTAINER_LINES}  [$role] $name | ${status:-n/a} | ${ports:-sem portas publicadas}"$'\n'
  done <<<"$STACK_CONTAINERS"
fi

cat <<EOF
Runtime: $RUNTIME_LABEL
Mode: $ENV_MODE
Loader: $GMX_ENV_SOURCE

Stack:
  dev: api=$( [[ -n "$ACTIVE_API_DOCS_URL" ]] && printf 'up' || printf 'down' ) frontend=$( [[ -n "$ACTIVE_FRONTEND_URL" ]] && printf 'up' || printf 'down' )
  infra: containers=$TOTAL_COUNT api=$API_COUNT workers=$WORKER_COUNT infra=$INFRA_COUNT edge=$EDGE_COUNT other=$OTHER_COUNT

API:
  docs: ${ACTIVE_API_DOCS_URL:-unreachable}
  health: $API_HEALTH_STATUS -> ${API_HEALTH_URL:-n/a}
  source: ${ACTIVE_API_LABEL:-none}${ACTIVE_API_TIME:+, ${ACTIVE_API_TIME}s}
EOF

if [[ -n "$API_HEALTH_BODY" ]]; then
  printf '  body: %s\n' "$API_HEALTH_BODY"
fi

echo ""
echo "Containers:"
if [[ -n "$CONTAINER_LINES" ]]; then
  printf '%s' "$CONTAINER_LINES"
else
  echo "  Nenhum container ativo encontrado."
fi
