#!/usr/bin/env bash
set -euo pipefail

MODULES_DIR="apps/backend/app/modules"

find "$MODULES_DIR" -mindepth 2 -maxdepth 2 -type d | while read -r mod; do

MACRO=$(basename "$(dirname "$mod")")
SUB=$(basename "$mod")

mkdir -p "$mod"/{api,application,domain,infrastructure}

touch "$mod"/__init__.py
touch "$mod"/api/__init__.py

cat <<'PYEOF' > "$mod/api/health.py"
from fastapi import APIRouter

router = APIRouter()

def module_name():
    parts = __name__.split(".")
    try:
        return f"{parts[3]}.{parts[4]}"
    except Exception:
        return __name__

@router.get("/health")
def health():
    return {
        "status": "ok",
        "module": module_name()
    }
PYEOF

ROUTER="$mod/api/router.py"

if [ ! -f "$ROUTER" ]; then
cat <<'PYEOF' > "$ROUTER"
from fastapi import APIRouter
from .health import router as health_router

router = APIRouter()

router.include_router(health_router)
PYEOF
fi

done
