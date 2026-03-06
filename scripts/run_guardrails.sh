#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

MODULE_ROOTS=("apps/backend/app/modules")
RUN_ARCHITECTURE_SCAN="${GUARDRAILS_RUN_ARCHITECTURE_SCAN:-1}"
ARCHITECTURE_SCAN_CMD="${GUARDRAILS_ARCHITECTURE_SCAN_CMD:-python3 apps/backend/tools/architecture/run_analysis.py}"
SCAN_BEFORE_REPORT="${GUARDRAILS_SCAN_BEFORE_REPORT:-reports/architecture_scan_before.json}"
SCAN_AFTER_REPORT="${GUARDRAILS_SCAN_AFTER_REPORT:-reports/architecture_scan_after.json}"
REFACTOR_REPORT="${GUARDRAILS_REFACTOR_REPORT:-reports/architecture_refactor_report.json}"
REFACTOR_DRY_RUN="${REFACTOR_DRY_RUN:-0}"
ALLOWLIST_PHASE="${GUARDRAILS_PHASE:-core}"
ALLOWLIST_VERSION="${GUARDRAILS_ALLOWLIST_VERSION:-v1}"
ALLOWLIST_FILE="scripts/guardrails/allowlists/${ALLOWLIST_VERSION}.sh"
PYTEST_BIN="${GUARDRAILS_PYTEST_BIN:-pytest}"
TEST_CMD="${GUARDRAILS_TEST_CMD:-}"

declare -a PHASE_TARGETS=()
declare -a PHASE_IGNORES=()

load_allowlist_phase() {
  local phase="$1"
  local phase_upper
  phase_upper="$(printf "%s" "$phase" | tr '[:lower:]' '[:upper:]')"

  if [[ ! -f "$ALLOWLIST_FILE" ]]; then
    echo "Allowlist file not found: $ALLOWLIST_FILE"
    exit 1
  fi

  # shellcheck source=/dev/null
  source "$ALLOWLIST_FILE"

  if [[ ! " ${GUARDRAILS_ALLOWLIST_PHASES[*]} " =~ " ${phase} " ]]; then
    echo "Unknown GUARDRAILS_PHASE='${phase}'. Allowed: ${GUARDRAILS_ALLOWLIST_PHASES[*]}"
    exit 1
  fi

  local targets_var="GUARDRAILS_PYTEST_TARGETS_${phase_upper}"
  local ignores_var="GUARDRAILS_PYTEST_IGNORES_${phase_upper}"

  if ! declare -p "$targets_var" >/dev/null 2>&1; then
    echo "Allowlist targets not defined for phase '${phase}' in ${ALLOWLIST_FILE}"
    exit 1
  fi

  if ! declare -p "$ignores_var" >/dev/null 2>&1; then
    eval "$ignores_var=()"
  fi

  declare -n targets_ref="$targets_var"
  declare -n ignores_ref="$ignores_var"
  PHASE_TARGETS=("${targets_ref[@]}")
  PHASE_IGNORES=("${ignores_ref[@]}")
}

if [[ "$RUN_ARCHITECTURE_SCAN" == "1" ]]; then
  echo "[1/9] Running enterprise architecture scan..."
  bash -lc "$ARCHITECTURE_SCAN_CMD"
else
  echo "[1/9] Skipping enterprise architecture scan (GUARDRAILS_RUN_ARCHITECTURE_SCAN=0)."
fi

echo "[2/9] Enforcing core namespace guardrail..."
python3 scripts/guardrails/check_core_namespace.py --root apps/backend

echo "[3/9] Enforcing module registry synchronization guardrail..."
python3 scripts/guardrails/check_module_registry_sync.py --modules-root apps/backend/app/modules

if [[ "${GUARDRAILS_ENFORCE_GUIDE_SYNC:-1}" == "1" ]]; then
  echo "[4/9] Enforcing AI architecture guide sync guardrail..."
  python3 scripts/guardrails/check_architecture_guide_sync.py
else
  echo "[4/9] Skipping AI architecture guide sync guardrail (GUARDRAILS_ENFORCE_GUIDE_SYNC=0)."
fi

echo "[5/9] Scanning architecture (before refactor)..."
python3 scripts/architecture_scan.py \
  --roots "${MODULE_ROOTS[@]}" \
  --json-out "$SCAN_BEFORE_REPORT"

echo "[6/9] Applying safe refactors..."
REFACTOR_ARGS=(
  --roots "${MODULE_ROOTS[@]}"
  --report-out "$REFACTOR_REPORT"
)
if [[ "$REFACTOR_DRY_RUN" == "1" ]]; then
  REFACTOR_ARGS+=(--dry-run)
fi
python3 scripts/refactor_modules.py "${REFACTOR_ARGS[@]}"

echo "[7/9] Scanning architecture (after refactor)..."
python3 scripts/architecture_scan.py \
  --roots "${MODULE_ROOTS[@]}" \
  --json-out "$SCAN_AFTER_REPORT" \
  --fail-on-violations

echo "[8/9] Running backend architecture guardrails..."
if [[ -f "apps/backend/scripts/architecture_guardrails.sh" ]]; then
  bash apps/backend/scripts/architecture_guardrails.sh
else
  echo "Guardrails script not found at apps/backend/scripts/architecture_guardrails.sh; skipping."
fi

echo "[9/9] Running tests..."
if [[ "${SKIP_TESTS:-0}" == "1" ]]; then
  echo "Skipping tests because SKIP_TESTS=1."
else
  if [[ -n "$TEST_CMD" ]]; then
    echo "Using explicit GUARDRAILS_TEST_CMD override."
    bash -lc "$TEST_CMD"
  else
    load_allowlist_phase "$ALLOWLIST_PHASE"

    echo "Using test allowlist version=${ALLOWLIST_VERSION} phase=${ALLOWLIST_PHASE}"
    echo "Targets (${#PHASE_TARGETS[@]}): ${PHASE_TARGETS[*]}"
    if [[ "${#PHASE_IGNORES[@]}" -eq 0 ]]; then
      echo "Ignores (0): none"
    else
      echo "Ignores (${#PHASE_IGNORES[@]}): ${PHASE_IGNORES[*]}"
    fi

    PYTEST_ARGS=(--maxfail=1 --disable-warnings -q)
    PYTEST_ARGS+=("${PHASE_TARGETS[@]}")
    for ignore_path in "${PHASE_IGNORES[@]}"; do
      PYTEST_ARGS+=(--ignore="$ignore_path")
    done

    if [[ -n "${GUARDRAILS_PYTEST_EXTRA_ARGS:-}" ]]; then
      read -r -a extra_args <<< "${GUARDRAILS_PYTEST_EXTRA_ARGS}"
      PYTEST_ARGS+=("${extra_args[@]}")
    fi

    "$PYTEST_BIN" "${PYTEST_ARGS[@]}"
  fi
fi

echo "Guardrails pipeline completed."
