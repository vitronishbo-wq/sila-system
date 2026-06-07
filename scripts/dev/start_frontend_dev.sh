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
exec npm run dev:raw -- --host 0.0.0.0 --port "${GMX_FRONTEND_PORT:-$FRONTEND_PORT}" "$@"
