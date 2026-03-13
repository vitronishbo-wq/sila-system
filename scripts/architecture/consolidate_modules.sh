#!/usr/bin/env bash
set -euo pipefail

MODULES_DIR="apps/backend/app/modules"
SHARED_DIR="apps/backend/app/platform/shared"

echo "=== SILA CONSOLIDATION: START ==="

ensure_manifest() {
    local target_dir="$1"
    local module_name="$2"
    local module_type="$3"
    local manifest="${target_dir}/module.yaml"

    mkdir -p "${target_dir}"
    if [ ! -f "${manifest}" ]; then
        cat <<EOF > "${manifest}"
name: ${module_name}
type: ${module_type}
version: 1.0.0

exposes:
  api_routers: []
  public_models: []
  events_published: []

requires:
  domains: []
  core_services: []

subdomains: []
EOF
    fi
}

move_contents_if_exists() {
    local src="$1"
    local dst="$2"

    if [ ! -d "${src}" ]; then
        return 0
    fi

    mkdir -p "${dst}"
    shopt -s dotglob nullglob
    local entries=("${src}"/*)
    if [ ${#entries[@]} -gt 0 ]; then
        mv "${entries[@]}" "${dst}/"
    fi
    shopt -u dotglob nullglob

    rm -rf "${src}"
}

echo "[1/4] Shared Kernel"
mkdir -p "${SHARED_DIR}"/{domain,application,infrastructure}
touch "${SHARED_DIR}/domain/address.py"
touch "${SHARED_DIR}/domain/currency.py"
touch "${SHARED_DIR}/domain/cidadao_id.py"
touch "${SHARED_DIR}/domain/status_workflow.py"

echo "[2/4] Fusoes criticas"

# Economy: Financas
ensure_manifest "${MODULES_DIR}/economy/financas" "financas" "sub_domain"
mkdir -p "${MODULES_DIR}/economy/financas/taxation" "${MODULES_DIR}/economy/financas/public_budget"
move_contents_if_exists "${MODULES_DIR}/economy/financas_impostos" "${MODULES_DIR}/economy/financas/taxation"
move_contents_if_exists "${MODULES_DIR}/economy/financas_publicas" "${MODULES_DIR}/economy/financas/public_budget"

# Resources: Pescas
ensure_manifest "${MODULES_DIR}/resources/pescas" "pescas" "sub_domain"
mkdir -p "${MODULES_DIR}/resources/pescas/industrial"
move_contents_if_exists "${MODULES_DIR}/resources/pescas_industriais" "${MODULES_DIR}/resources/pescas/industrial"

# Economy: Comercio -> Trade
ensure_manifest "${MODULES_DIR}/economy/trade" "trade" "sub_domain"
mkdir -p "${MODULES_DIR}/economy/trade/external" "${MODULES_DIR}/economy/trade/services"
move_contents_if_exists "${MODULES_DIR}/economy/comercio_externo" "${MODULES_DIR}/economy/trade/external"
move_contents_if_exists "${MODULES_DIR}/economy/comercio_servicos" "${MODULES_DIR}/economy/trade/services"

# Infrastructure: Logistica
ensure_manifest "${MODULES_DIR}/infrastructure_sector/logistica" "logistica" "sub_domain"
mkdir -p "${MODULES_DIR}/infrastructure_sector/logistica/ports" "${MODULES_DIR}/infrastructure_sector/logistica/transport"
move_contents_if_exists "${MODULES_DIR}/infrastructure_sector/portos_logistica" "${MODULES_DIR}/infrastructure_sector/logistica/ports"
move_contents_if_exists "${MODULES_DIR}/infrastructure_sector/transportes_logistica" "${MODULES_DIR}/infrastructure_sector/logistica/transport"

echo "[3/4] Manifestos com autoridade"
python3 - <<'PY'
from pathlib import Path
import yaml

targets = [
    Path("apps/backend/app/modules/economy/financas/module.yaml"),
    Path("apps/backend/app/modules/resources/pescas/module.yaml"),
    Path("apps/backend/app/modules/economy/trade/module.yaml"),
    Path("apps/backend/app/modules/infrastructure_sector/logistica/module.yaml"),
]

for path in targets:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not isinstance(data, dict):
            data = {}
    else:
        data = {}

    data.setdefault("name", path.parent.name)
    data.setdefault("type", "sub_domain")
    data.setdefault("version", "1.0.0")
    data.setdefault("exposes", {})
    data.setdefault("requires", {})
    data.setdefault("subdomains", [])

    exposes = data.get("exposes") if isinstance(data.get("exposes"), dict) else {}
    exposes.setdefault("api_routers", [])
    exposes.setdefault("public_models", [])
    exposes.setdefault("events_published", [])
    data["exposes"] = exposes

    requires = data.get("requires") if isinstance(data.get("requires"), dict) else {}
    requires.setdefault("domains", [])
    requires.setdefault("core_services", [])
    data["requires"] = requires

    authority = data.get("authority") if isinstance(data.get("authority"), dict) else {}
    authority["entities"] = ["Cidadao", "CertidaoNascimento"]
    data["authority"] = authority

    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
PY

echo "[4/4] Scanner de imports quebrados"
for pattern in \
    "comercio_externo" \
    "financas_impostos" \
    "pescas_industriais" \
    "portos_logistica" \
    "transportes_logistica"
do
    echo "--- ${pattern} ---"
    grep -R --line-number --fixed-strings --binary-files=without-match \
        --exclude-dir="__pycache__" "${pattern}" apps/backend/app/modules || true
done

echo "=== SILA CONSOLIDATION: DONE ==="
