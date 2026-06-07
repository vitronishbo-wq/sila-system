#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_MODE_INPUT="${ENV_MODE:-auto}"
OUTPUT_KIND="pretty"

if [[ "${1:-}" == "host" || "${1:-}" == "docker" || "${1:-}" == "auto" ]]; then
  ENV_MODE_INPUT="$1"
  shift || true
fi

if [[ $# -gt 0 ]]; then
  OUTPUT_KIND="$1"
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

bridge_host_resolves() {
  getent hosts "$BRIDGE_BASE_HOST" >/dev/null 2>&1
}

check_url() {
  local url="$1"
  local err_file=""
  local time_total=""
  local curl_exit=0

  if command -v curl >/dev/null 2>&1; then
    err_file="$(mktemp)"
    set +e
    time_total="$(curl -o /dev/null -sS --max-time "$GMX_URL_TIMEOUT_SECONDS" -w "%{time_total}" "$url" 2>"$err_file")"
    curl_exit=$?
    set -e

    if [[ $curl_exit -eq 0 ]]; then
      rm -f "$err_file"
      printf 'ok|%s|\n' "$time_total"
      return 0
    fi

    printf 'error||%s\n' "$(tr '\n' ' ' < "$err_file" | sed 's/[[:space:]]\+/ /g; s/^ //; s/ $//')"
    rm -f "$err_file"
    return 0
  fi

  printf 'error||curl indisponivel\n'
  return 0
}

resolve_active_url() {
  local local_url="$1"
  local bridge_url="$2"
  local active_url="unreachable"
  local active_label="none"
  local active_time=""
  local candidate=""
  local candidate_label=""
  local candidate_url=""
  local probe_status=""
  local probe_time=""
  local probe_error=""

  IFS=',' read -r -a candidate_order <<< "${GMX_URL_PRIORITY:-local,bridge}"

  for candidate in "${candidate_order[@]}"; do
    candidate="${candidate//[[:space:]]/}"
    case "$candidate" in
      local)
        candidate_label="localhost"
        candidate_url="$local_url"
        ;;
      bridge)
        candidate_label="bridge"
        candidate_url="$bridge_url"
        ;;
      *)
        continue
        ;;
    esac

    IFS='|' read -r probe_status probe_time probe_error < <(check_url "$candidate_url")
    if [[ "$probe_status" == "ok" ]]; then
      active_url="$candidate_url"
      active_label="$candidate_label"
      active_time="$probe_time"
      break
    fi
  done

  printf '%s|%s|%s\n' "$active_url" "$active_label" "$active_time"
}

print_probe_debug() {
  local title="$1"
  shift
  local candidate=""
  local candidate_label=""
  local candidate_url=""
  local probe_status=""
  local probe_time=""
  local probe_error=""
  local local_url="$1"
  local bridge_url="$2"

  echo "$title"
  IFS=',' read -r -a candidate_order <<< "${GMX_URL_PRIORITY:-local,bridge}"
  for candidate in "${candidate_order[@]}"; do
    candidate="${candidate//[[:space:]]/}"
    case "$candidate" in
      local)
        candidate_label="localhost"
        candidate_url="$local_url"
        ;;
      bridge)
        candidate_label="bridge"
        candidate_url="$bridge_url"
        ;;
      *)
        continue
        ;;
    esac

    IFS='|' read -r probe_status probe_time probe_error < <(check_url "$candidate_url")
    if [[ "$probe_status" == "ok" ]]; then
      echo "  - $candidate_label: ok (${probe_time}s) -> $candidate_url"
    else
      echo "  - $candidate_label: error -> $candidate_url"
      echo "    $probe_error"
    fi
  done
}

format_active_line() {
  local active_url="$1"
  local active_label="$2"
  local active_time="$3"

  if [[ "$active_url" == "unreachable" ]]; then
    printf 'unreachable (%s)\n' "$active_label"
    return
  fi

  printf '%s (%s, %ss)\n' "$active_url" "$active_label" "$active_time"
}

api_base_from_docs_url() {
  local docs_url="$1"

  if [[ "$docs_url" == "unreachable" ]]; then
    printf 'unreachable\n'
    return
  fi

  printf '%s\n' "${docs_url%/docs}"
}

LOADER_EXPORTS="$("$PROJECT_ROOT/scripts/dev/load_runtime_env.sh" "$ENV_MODE_INPUT")"
eval "$LOADER_EXPORTS"

RUNTIME_LABEL="$(detect_runtime_label)"
BRIDGE_STATUS="unresolved"
if bridge_host_resolves; then
  BRIDGE_STATUS="resolved"
fi

IFS='|' read -r ACTIVE_API_URL ACTIVE_API_LABEL ACTIVE_API_TIME < <(
  resolve_active_url "$LOCAL_API_DOCS_URL" "$BRIDGE_API_DOCS_URL"
)
IFS='|' read -r ACTIVE_FRONTEND_URL ACTIVE_FRONTEND_LABEL ACTIVE_FRONTEND_TIME < <(
  resolve_active_url "$LOCAL_FRONTEND_URL" "$BRIDGE_FRONTEND_URL"
)

case "$OUTPUT_KIND" in
  pretty)
    cat <<EOF
Runtime: $RUNTIME_LABEL
Mode: $ENV_MODE

ACTIVE:
  API: $(format_active_line "$ACTIVE_API_URL" "$ACTIVE_API_LABEL" "$ACTIVE_API_TIME")
  Frontend: $(format_active_line "$ACTIVE_FRONTEND_URL" "$ACTIVE_FRONTEND_LABEL" "$ACTIVE_FRONTEND_TIME")

Options:
  localhost:
    API: $LOCAL_API_DOCS_URL
    Frontend: $LOCAL_FRONTEND_URL
  bridge:
    API: $BRIDGE_API_DOCS_URL
    Frontend: $BRIDGE_FRONTEND_URL
    Status: $BRIDGE_STATUS

Loader:
  Source: $GMX_ENV_SOURCE
EOF
    if [[ "$GMX_URL_DEBUG" == "1" && "$ACTIVE_API_URL" == "unreachable" ]]; then
      echo ""
      print_probe_debug "Debug API Probes:" "$LOCAL_API_DOCS_URL" "$BRIDGE_API_DOCS_URL"
    fi
    if [[ "$GMX_URL_DEBUG" == "1" && "$ACTIVE_FRONTEND_URL" == "unreachable" ]]; then
      echo ""
      print_probe_debug "Debug Frontend Probes:" "$LOCAL_FRONTEND_URL" "$BRIDGE_FRONTEND_URL"
    fi
    ;;
  --active-api)
    if [[ "$ACTIVE_API_URL" == "unreachable" ]]; then
      exit 1
    fi
    printf '%s\n' "$ACTIVE_API_URL"
    ;;
  --active-api-base)
    if [[ "$ACTIVE_API_URL" == "unreachable" ]]; then
      exit 1
    fi
    api_base_from_docs_url "$ACTIVE_API_URL"
    ;;
  --active-frontend)
    if [[ "$ACTIVE_FRONTEND_URL" == "unreachable" ]]; then
      exit 1
    fi
    printf '%s\n' "$ACTIVE_FRONTEND_URL"
    ;;
  --active-api-label)
    printf '%s\n' "$ACTIVE_API_LABEL"
    ;;
  --active-frontend-label)
    printf '%s\n' "$ACTIVE_FRONTEND_LABEL"
    ;;
  --active-api-time)
    printf '%s\n' "$ACTIVE_API_TIME"
    ;;
  --active-frontend-time)
    printf '%s\n' "$ACTIVE_FRONTEND_TIME"
    ;;
  *)
    echo "Formato inválido: $OUTPUT_KIND" >&2
    exit 1
    ;;
esac
