#!/usr/bin/env bash
set -euo pipefail

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}=== SILA UNIVERSALIZER V2: MACRO & SUB-DOMINIOS ===${NC}"

MODULES_DIR="apps/backend/app/modules"
DOMAINS=("economy" "governance" "intelligence" "justice" "resources" "infrastructure_sector" "society" "educacao")

to_pascal_case() {
    local raw="$1"
    echo "${raw}" | sed -E 's/(^|[_\.-])([a-zA-Z])/\U\2/g'
}

apply_sila_dna() {
    local target_path="$1"
    local name="$2"
    local type="$3" # macro_domain | sub_domain

    mkdir -p "${target_path}"/{api,application,domain,infrastructure,tests}

    local manifest="${target_path}/module.yaml"
    if [ ! -f "${manifest}" ]; then
        cat <<EOF > "${manifest}"
name: ${name}
type: ${type}
version: 1.0.0
status: alpha
owner: sila-core
description: Universal module manifest for SILA System

exposes:
  api_routers: []
  public_models: []
  events_published: []

requires:
  domains: []
  core_services: []

subdomains: []
EOF
        echo -e "${GREEN}[GEN]${NC} ${type}: ${name}/module.yaml"
    fi

    local arch_doc="${target_path}/ARCHITECTURE.md"
    if [ ! -f "${arch_doc}" ]; then
        cat <<EOF > "${arch_doc}"
# Arquitetura do Modulo: ${name^^}

## Contexto
Este modulo pertence ao SILA System e segue o padrao universal de Bounded Context.

## Fronteira (Contracts)
- **API Entrypoint:** \`api/router.py\`
- **Domain Exceptions:** \`domain/exceptions.py\`
- **Persistence Layer:** \`infrastructure/repository.py\`
EOF
        echo -e "${GREEN}[GEN]${NC} ${name}/ARCHITECTURE.md"
    fi

    local exceptions="${target_path}/domain/exceptions.py"
    if [ ! -s "${exceptions}" ]; then
        local class_name
        class_name="$(to_pascal_case "${name}")"
        echo "class ${class_name}Error(Exception): pass" > "${exceptions}"
        echo -e "${GREEN}[GEN]${NC} ${name}/domain/exceptions.py"
    fi
}

for mod in "${DOMAINS[@]}"; do
    mod_path="${MODULES_DIR}/${mod}"

    if [ ! -d "${mod_path}" ]; then
        echo -e "${YELLOW}[SKIP]${NC} Modulo ${mod} nao encontrado em ${MODULES_DIR}"
        continue
    fi

    echo -e "${BLUE}--- Processando Macro: ${mod} ---${NC}"
    apply_sila_dna "${mod_path}" "${mod}" "macro_domain"

    while IFS= read -r -d '' sub; do
        sub_name="$(basename "${sub}")"
        echo -e "  ${YELLOW}└─ Sub-modulo:${NC} ${sub_name}"
        apply_sila_dna "${sub}" "${sub_name}" "sub_domain"
    done < <(
        find "${mod_path}" -mindepth 1 -maxdepth 1 -type d \
            ! -name "api" \
            ! -name "application" \
            ! -name "domain" \
            ! -name "infrastructure" \
            ! -name "tests" \
            ! -name "__pycache__" \
            -print0
    )
done

echo -e "\n${BLUE}=== UNIVERSALIZACAO NIVEL 2 CONCLUIDA ===${NC}"
echo -e "Proximo passo: Rodar 'python3 scripts/arch_compiler.py' para indexar."
