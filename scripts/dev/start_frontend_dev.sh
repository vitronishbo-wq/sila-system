#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
FRONTEND_DIR="$PROJECT_ROOT/apps/frontend"
ENV_MODE_INPUT="${ENV_MODE:-auto}"
INPUT_VITE_API_URL="${VITE_API_URL-}"
INPUT_VITE_API_PORT="${VITE_API_PORT-}"

pick_preferred_api_base() {
  local candidate=""

  IFS=',' read -r -a candidates <<< "${GMX_URL_PRIORITY:-local,bridge}"
  for candidate in "${candidates[@]}"; do
    candidate="${candidate//[[:space:]]/}"
    case "$candidate" in
      local)
        printf '%s\n' "$LOCAL_API_BASE_URL"
        return 0
        ;;
      bridge)
        printf '%s\n' "$BRIDGE_API_BASE_URL"
        return 0
        ;;
    esac
  done

  printf '%s\n' "$LOCAL_API_BASE_URL"
}

eval "$("$PROJECT_ROOT/scripts/dev/load_runtime_env.sh" "$ENV_MODE_INPUT")"

ACTIVE_API_BASE_URL=""
if ACTIVE_API_BASE_URL="$("$PROJECT_ROOT/scripts/dev/print_runtime_urls.sh" "$ENV_MODE" --active-api-base 2>/dev/null)"; then
  :
else
  ACTIVE_API_BASE_URL="$(pick_preferred_api_base)"
fi

export VITE_API_PORT="${VITE_API_PORT:-$GMX_API_PORT}"
if [[ -n "$INPUT_VITE_API_PORT" ]]; then
  export VITE_API_PORT="$INPUT_VITE_API_PORT"
fi

if [[ -n "$INPUT_VITE_API_URL" ]]; then
  export VITE_API_URL="$INPUT_VITE_API_URL"
else
  export VITE_API_URL="$ACTIVE_API_BASE_URL/api/v1"
fi

if [[ "${ENV_DEBUG:-0}" == "1" ]]; then
  echo "==> Frontend runtime API: $VITE_API_URL"
fi

cd "$FRONTEND_DIR"
# Check local Node version compatibility with Vite (>=20.19 or >=22.x)
node_version_ok() {
  if ! command -v node >/dev/null 2>&1; then
    return 1
  fi
  node_v_raw="$(node -v 2>/dev/null || echo '')"
  node_v="${node_v_raw#v}"
  major=$(echo "$node_v" | cut -d. -f1 || echo 0)
  minor=$(echo "$node_v" | cut -d. -f2 || echo 0)
  if [[ -z "$major" ]]; then
    return 1
  fi
  if (( major >= 22 )); then
    return 0
  fi
  if (( major == 20 )) && (( minor >= 19 )); then
    return 0
  fi
  return 1
}

if node_version_ok; then
  exec npm run dev:raw -- --host 0.0.0.0 --port "${GMX_FRONTEND_PORT:-$FRONTEND_PORT}" "$@"
else
  echo "[info] Detected Node version $(node -v 2>/dev/null || 'none') incompatible with Vite; attempting Docker fallback (node:20)"
  if ! command -v docker >/dev/null 2>&1; then
    echo "[error] Docker not available and Node incompatible. Please install Docker or upgrade Node to >=20.19." >&2
    exit 1
  fi

  HOST_NODE_MODULES_DIR="${HOST_NODE_MODULES_DIR:-$PROJECT_ROOT/.docker_node_modules/frontend}"
  mkdir -p "$HOST_NODE_MODULES_DIR"
  CONTAINER_NAME="sila_frontend_dev_$(basename "$PROJECT_ROOT")"

  docker run --rm --name "$CONTAINER_NAME" -p "${GMX_FRONTEND_PORT:-$FRONTEND_PORT}:3000" -v "$FRONTEND_DIR":/app -v "$HOST_NODE_MODULES_DIR":/app/node_modules -w /app node:20-bullseye \
    bash -lc "npm ci --legacy-peer-deps && npm run dev:raw -- --host 0.0.0.0 --port 3000"
fi
