#!/usr/bin/env bash
# smoke-test.sh — Modern, automated smoke test runner + HTML report
# Usage: ./smoke-test.sh [--verbose] [--ci] [--base-url URL] [--retries N] [--timeout SEC]
set -euo pipefail

# ---------- Config (override via env or CLI) ----------
BASE_URL="${SMOKE_BASE_URL:-http://127.0.0.1:8000}"
RETRIES="${SMOKE_RETRIES:-2}"        # retries per endpoint
TIMEOUT="${SMOKE_TIMEOUT:-8}"        # curl timeout in seconds
VERBOSE=false
CI_MODE=false
REPORT_HTML="${SMOKE_REPORT_HTML:-smoke-report.html}"
REPORT_LOG="${SMOKE_REPORT_LOG:-smoke-report.log}"
AUTH_TOKEN="${SMOKE_AUTH_TOKEN:-}"   # if set, will be sent as Bearer token
# ------------------------------------------------------

# ---------- CLI parsing ----------
while (( "$#" )); do
  case "$1" in
    --verbose) VERBOSE=true; shift ;;
    --ci) CI_MODE=true; shift ;;
    --base-url) BASE_URL="$2"; shift 2 ;;
    --retries) RETRIES="$2"; shift 2 ;;
    --timeout) TIMEOUT="$2"; shift 2 ;;
    -h|--help)
      cat << EOF
Usage: $0 [--verbose] [--ci] [--base-url URL] [--retries N] [--timeout SEC]

Environment overrides:
  SMOKE_BASE_URL, SMOKE_RETRIES, SMOKE_TIMEOUT, SMOKE_AUTH_TOKEN,
  SMOKE_REPORT_HTML, SMOKE_REPORT_LOG
EOF
      exit 0
      ;;
    *) echo "Unknown arg: $1"; exit 2 ;;
  esac
done
# ------------------------------------------------------

# ---------- Dependencies ----------
for cmd in curl jq mktemp date; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "ERROR: required command not found: $cmd" >&2
    exit 2
  fi
done
# ------------------------------------------------------

# ---------- Helpers ----------
timestamp() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }
now_ms(){ date +%s%3N; }  # milliseconds
safe_header() {
  if [[ -n "$AUTH_TOKEN" ]]; then
    echo "-H 'Authorization: Bearer ${AUTH_TOKEN}'"
  else
    echo ""
  fi
}

curl_with_retry() {
  # args: method url [data_json]
  local method="$1"; shift
  local url="$1"; shift
  local data="${1:-}"
  local attempt=0
  local out tmp_status tmp_body
  while (( attempt <= RETRIES )); do
    attempt=$((attempt+1))
    if [[ -n "$data" ]]; then
      out=$(curl -sS --max-time "$TIMEOUT" -X "$method" "$url" -H "Content-Type: application/json" $(safe_header) -d "$data" -w "\n%{http_code}" 2>&1) || out="$out"
    else
      out=$(curl -sS --max-time "$TIMEOUT" -X "$method" "$url" $(safe_header) -w "\n%{http_code}" 2>&1) || out="$out"
    fi
    tmp_status="$(echo "$out" | tail -n1 || echo "")"
    tmp_body="$(echo "$out" | sed '$d' || true)"
    if [[ "$tmp_status" =~ ^2|3[0-9]{1}$ ]]; then
      echo -e "$tmp_body\n$tmp_status"
      return 0
    fi
    # retry on non-2xx/3xx
    if (( attempt <= RETRIES )); then
      sleep 0.6
      continue
    else
      echo -e "$tmp_body\n$tmp_status"
      return 1
    fi
  done
}

safe_json() {
  # pretty or raw depending on jq parseability
  local raw="$1"
  if echo "$raw" | jq . >/dev/null 2>&1; then
    echo "$raw" | jq .
  else
    echo "$raw"
  fi
}
# ------------------------------------------------------

# ---------- Prepare report files ----------
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT
: > "$REPORT_LOG"
start_ms=$(now_ms)
start_ts="$(timestamp)"

cat > "$REPORT_HTML" <<'HTML_HEAD'
<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Smoke Test Report</title>
<style>
 body{font-family:Inter,Arial,Helvetica,sans-serif;margin:18px;}
 table{border-collapse:collapse;width:100%}
 th,td{padding:8px;border:1px solid #ddd;text-align:left;vertical-align:top}
 th{background:#f4f4f6}
 .ok{background:#e6f7e6}
 .fail{background:#ffe6e6}
 pre{white-space:pre-wrap;word-break:break-word;background:#fafafa;padding:8px;border-radius:6px}
 .meta{color:#666;font-size:0.9rem}
</style>
</head>
<body>
<h1>Smoke Test Report</h1>
<p class="meta">Start: __START_TS__ &nbsp;|&nbsp; Base URL: __BASE_URL__</p>
<table>
<tr><th>Teste</th><th>Status</th><th>HTTP</th><th>Detalhes</th></tr>
HTML_HEAD

# replace markers
sed -i "s|__START_TS__|${start_ts}|g" "$REPORT_HTML"
sed -i "s|__BASE_URL__|${BASE_URL}|g" "$REPORT_HTML"
# ------------------------------------------------------

# ---------- Runner ----------
total=0; passed=0; failed=0

log_and_report() {
  # args: desc status http_code body
  local desc="$1"; shift
  local status="$1"; shift
  local http="$1"; shift
  local body="$1"; shift

  ((total++))
  if [[ "$status" == "OK" ]]; then ((passed++)); else ((failed++)); fi

  echo "[$(timestamp)] $desc -> $status ($http)" >> "$REPORT_LOG"
  if $VERBOSE; then
    echo "$body" >> "$REPORT_LOG"
    echo "----" >> "$REPORT_LOG"
  fi

  body_html=""
  if $VERBOSE && [[ -n "$body" ]]; then
    # escape for HTML: we rely on <pre>
    body_html="<pre>$(echo "$body" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')</pre>"
  else
    body_html="(omitted)"
  fi

  class="ok"
  if [[ "$status" != "OK" ]]; then class="fail"; fi

  cat >> "$REPORT_HTML" <<HTML_ROW
<tr class="${class}"><td>${desc}</td><td>${status}</td><td>${http}</td><td>${body_html}</td></tr>
HTML_ROW
}

run_test() {
  # args: desc method path [data_json] [expected_http_regex]
  local desc="$1"; shift
  local method="$1"; shift
  local path="$1"; shift
  local data="${1:-}"; shift || true
  local expect="${1:-2..}"  # naive; we check leading '2' success
  local url="${BASE_URL}${path}"
  local out rc body http
  if out="$(curl_with_retry "$method" "$url" "$data")"; then
    body="$(echo "$out" | sed '$d')"
    http="$(echo "$out" | tail -n1)"
    log_and_report "$desc" "OK" "$http" "$body"
    return 0
  else
    body="$(echo "$out" | sed '$d')"
    http="$(echo "$out" | tail -n1 || echo "ERR")"
    log_and_report "$desc" "FAIL" "$http" "$body"
    return 1
  fi
}

# quick helper for GET without data
run_get(){ run_test "$1" "GET" "$2" "" ; }
run_post(){ run_test "$1" "POST" "$2" "$3" ; }
run_put(){ run_test "$1" "PUT" "$2" "$3" ; }
run_delete(){ run_test "$1" "DELETE" "$2" "" ; }

# ---------- Test list ----------
echo "Starting smoke tests at $start_ts; base: $BASE_URL"
echo "Log -> $REPORT_LOG ; HTML -> $REPORT_HTML"

# simple endpoints
run_get "Ping global" "/ping" || true
run_get "Health V1" "/api/v1/health" || true
run_get "Health V2" "/api/v2/health" || true

# auth/login (POST query or JSON depending on API)
# try JSON body login first
login_payload='{"email":"admin@sila.gov.ao","password":"Truman1*Marcelo1*"}'
if run_test "Auth login v2 (JSON)" "POST" "/api/v2/auth/login" "$login_payload"; then
  login_resp="$(tail -n1 < "$REPORT_LOG" >/dev/null 2>&1 || true)"
fi
# legacy path (best-effort)
run_post "Auth login v1 legacy" "/api/auth/login" "$login_payload" || true

# ping many service modules (list kept compact)
modules=(address appointments auth citizenship commercial common complaints documents education finance governance health identity integration internal journeys justice location monitoring notification payment registry reports sanitation service_hub social statistics training urbanism)
for m in "${modules[@]}"; do
  run_get "Ping ${m}" "/${m}/${m}/ping" || true
done

# dashboard
run_get "Dashboard resumo" "/api/v2/dashboard/resumo" || true
run_get "Dashboard municipios" "/api/v2/dashboard/municipios" || true

# ----- CRUD health flow (create -> get -> put -> delete -> confirm) -----
echo "Running CRUD flow for /health/ ..."

create_body='{"name":"smoke-test","age":99}'
create_out="$(curl_with_retry "POST" "${BASE_URL}/health/" "$create_body")" || create_out=""
create_status="$(echo "$create_out" | tail -n1 || echo "")"
create_body_raw="$(echo "$create_out" | sed '$d' || echo "")"

if [[ "$create_status" =~ ^2 ]]; then
  # try get id (support id or record_id)
  record_id="$(echo "$create_body_raw" | jq -r '.id // .record_id // .data.id // empty' 2>/dev/null || true)"
  if [[ -z "$record_id" || "$record_id" == "null" ]]; then
    log_and_report "Create Health" "FAIL" "$create_status" "$create_body_raw"
  else
    log_and_report "Create Health" "OK" "$create_status" "$create_body_raw"
    # get
    run_get "Get Health ${record_id}" "/health/${record_id}" || true
    # put
    run_put "Update Health ${record_id}" "/health/${record_id}" '{"age":42}' || true
    # delete
    run_delete "Delete Health ${record_id}" "/health/${record_id}" || true
    # confirm delete (expect non-200)
    if out="$(curl_with_retry "GET" "${BASE_URL}/health/${record_id}" "")"; then
      # If GET succeeds after delete, treat as failure
      body="$(echo "$out" | sed '$d')"
      http="$(echo "$out" | tail -n1)"
      log_and_report "Confirm delete Health ${record_id}" "FAIL" "$http" "$body"
    else
      out="$(echo "$out" || true)"
      body="$(echo "$out" | sed '$d' || true)"
      http="$(echo "$out" | tail -n1 || "ERR")"
      # Consider 4xx/422 as OK (deleted)
      if [[ "$http" =~ ^4 ]]; then
        log_and_report "Confirm delete Health ${record_id}" "OK" "$http" "$body"
      else
        log_and_report "Confirm delete Health ${record_id}" "FAIL" "$http" "$body"
      fi
    fi
  fi
else
  log_and_report "Create Health" "FAIL" "$create_status" "$create_body_raw"
fi

# ---------- Finalize report ----------
end_ms=$(now_ms)
duration_ms=$((end_ms - start_ms))
duration_s=$((duration_ms / 1000))
end_ts="$(timestamp)"

cat >> "$REPORT_HTML" <<HTML_FOOT
</table>
<p class="meta">Finish: ${end_ts} &nbsp;|&nbsp; Duration: ${duration_s}s (${duration_ms}ms)</p>
<p class="meta">Summary: total=${total}, passed=${passed}, failed=${failed}</p>
</body>
</html>
HTML_FOOT

echo "Finished: start=${start_ts} end=${end_ts} duration=${duration_s}s"
echo "Summary: total=${total} passed=${passed} failed=${failed}"
echo "Report files: ${REPORT_LOG}, ${REPORT_HTML}"

# if CI mode, don't try to open browser
if ! $CI_MODE; then
  # try to open the HTML report if xdg-open available (best-effort)
  if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$REPORT_HTML" >/dev/null 2>&1 || true
  fi
fi

# final exit code
if (( failed > 0 )); then
  exit 1
else
  exit 0
fi

PORTAL_URL="http://127.0.0.1:3000"
ADMIN_URL="http://127.0.0.1:4000"

log "🌐 Testando Portal do Cidadão..."
check_page "Portal Home" "$PORTAL_URL" "<title>Portal do Cidadão</title>"
check_page "Portal Login" "$PORTAL_URL/login" "<h1>Entrar</h1>"
check_page "Portal Serviços" "$PORTAL_URL/servicos" "Lista de Serviços"

log "🛠️ Testando Interface Administrativa..."
check_page "Admin Login" "$ADMIN_URL/login" "<h1>Administração</h1>"
check_page "Admin Dashboard" "$ADMIN_URL/dashboard" "Dashboard"
check_page "Admin Usuários" "$ADMIN_URL/users" "Gestão de Utilizadores"
