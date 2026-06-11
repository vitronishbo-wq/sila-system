#!/usr/bin/env bash
# DEMO HEALTH CHECK — SILA Nascimento BI NIF SS
# Exit code: 0 = all OK, 1 = any failure
set -euo pipefail
FAIL=0
PASS=0

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

check() {
    local label="$1"
    shift
    if "$@" >/dev/null 2>&1; then
        echo -e "  ${GREEN}OK${NC}  $label"
        PASS=$((PASS + 1))
    else
        echo -e "  ${RED}FAIL${NC} $label"
        FAIL=$((FAIL + 1))
    fi
}

check_detail() {
    local label="$1"
    shift
    if "$@" >/dev/null 2>&1; then
        echo -e "  ${GREEN}OK${NC}  $label"
        PASS=$((PASS + 1))
    else
        echo -e "  ${RED}FAIL${NC} $label — see output above"
        FAIL=$((FAIL + 1))
    fi
}

echo "============================================"
echo "  DEMO HEALTH CHECK — Nascimento BI NIF SS"
echo "============================================"
echo ""

# ─── Prerequisites ────────────────────────────────
echo "[1/5] Infra-estrutura"

check "PostgreSQL  (pg_isready)"  pg_isready -h localhost -p 5432
check "Redis       (PONG)"        redis-cli -h localhost ping

# ─── Python env ────────────────────────────────────
echo ""
echo "[2/5] Ambiente Python"

check "virtual env at .venv"       test -f .venv/bin/python
check "celery importável"          .venv/bin/python -c "from celery import Celery; print('OK')"
check "deps import (get_identity_context)" .venv/bin/python -c "
import sys
sys.path.insert(0, '.')
sys.path.insert(0, 'apps/backend')
from apps.backend.app.api.deps import get_identity_context
print('OK')
"

# ─── DB state ──────────────────────────────────────
echo ""
echo "[3/5] Banco de dados"

check "DATABASE_URL resolvida"     grep -q 'DATABASE_URL' .env 2>/dev/null
check "Alembic migrations"         .venv/bin/python -c "
import sys
sys.path.insert(0, '.')
sys.path.insert(0, 'apps/backend')
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.runtime.environment import EnvironmentContext
cfg = Config('apps/backend/alembic.ini')
script = ScriptDirectory.from_config(cfg)
head = script.get_current_head()
print(f'HEAD: {head}')
"

# ─── Workflow loader ───────────────────────────────
echo ""
echo "[4/5] Workflow loader"

# Run loader and capture output
LOADER_OUTPUT=$(.venv/bin/python scripts/load_process_workflows.py 2>&1)
LOADER_EXIT=$?
if [ $LOADER_EXIT -eq 0 ]; then
    echo -e "  ${GREEN}OK${NC}  Loader executado com sucesso"
    echo "$LOADER_OUTPUT" | head -3 | sed 's/^/       /'
    PASS=$((PASS + 1))
else
    echo -e "  ${RED}FAIL${NC} Loader falhou (exit=$LOADER_EXIT)"
    echo "$LOADER_OUTPUT" | sed 's/^/       /'
    FAIL=$((FAIL + 1))
fi

# ─── E2E tests ─────────────────────────────────────
echo ""
echo "[5/5] Testes E2E nascimento_bi_nif_ss"

TEST_OUTPUT=$(.venv/bin/python -m pytest \
    apps/backend/app/processes/nascimento_bi_nif_ss/tests/e2e/ \
    -v --tb=short 2>&1)
TEST_EXIT=$?
if [ $TEST_EXIT -eq 0 ]; then
    echo -e "  ${GREEN}OK${NC}  3/3 passed"
    PASS=$((PASS + 1))
else
    echo -e "  ${RED}FAIL${NC} testes E2E (exit=$TEST_EXIT)"
    echo "$TEST_OUTPUT" | tail -5 | sed 's/^/       /'
    FAIL=$((FAIL + 1))
fi

# ─── Summary ───────────────────────────────────────
echo ""
echo "============================================"
echo -e "  ${GREEN}${PASS} passed${NC}  ${RED}${FAIL} failed${NC}"
echo "============================================"

if [ $FAIL -gt 0 ]; then
    echo ""
    echo "RISCOS CONHECIDOS:"
    echo "  - core/dependencies/__init__.py:5 import residual (não afeta nascimento)"
    echo "  - 54 falhas pré-existentes no test suite completo (fora do escopo)"
    exit 1
fi
exit 0
