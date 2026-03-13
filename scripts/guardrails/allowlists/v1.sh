#!/usr/bin/env bash

# Guardrails pytest allowlist (version v1)
# Phases:
# - core: suite padrão estável para execução contínua
# - integration: foco em integração/e2e não legada
# - legacy: suites fora do baseline oficial (auditoria de dívida técnica)

GUARDRAILS_ALLOWLIST_PHASES=(core integration legacy)

declare -a GUARDRAILS_PYTEST_TARGETS_CORE=(
  "apps/backend/tests"
)

declare -a GUARDRAILS_PYTEST_IGNORES_CORE=(
  "apps/backend/tests/integration/modules"
  "apps/backend/tests/integration/test_pydantic_v2.py"
  "apps/backend/tests/unit/test_sanitation_service.py"
  "apps/backend/tests/test_models.py"
  "apps/backend/tests/test_basic_endpoints.py"
  "apps/backend/tests/test_citizen_document_service.py"
  "apps/backend/tests/test_location_import.py"
  "apps/backend/tests/test_modules_ping.py"
  "apps/backend/tests/test_smoke_production.py"
)

declare -a GUARDRAILS_PYTEST_TARGETS_INTEGRATION=(
  "apps/backend/tests/integration"
  "apps/backend/tests/e2e"
)

declare -a GUARDRAILS_PYTEST_IGNORES_INTEGRATION=(
  "apps/backend/tests/integration/modules"
  "apps/backend/tests/integration/test_pydantic_v2.py"
)

declare -a GUARDRAILS_PYTEST_TARGETS_LEGACY=(
  "apps/backend/tests/integration/modules"
  "apps/backend/tests/integration/test_pydantic_v2.py"
  "apps/backend/tests/unit/test_sanitation_service.py"
  "apps/backend/tests/test_models.py"
  "apps/backend/tests/test_basic_endpoints.py"
  "apps/backend/tests/test_citizen_document_service.py"
  "apps/backend/tests/test_location_import.py"
  "apps/backend/tests/test_modules_ping.py"
  "apps/backend/tests/test_smoke_production.py"
)

declare -a GUARDRAILS_PYTEST_IGNORES_LEGACY=()
