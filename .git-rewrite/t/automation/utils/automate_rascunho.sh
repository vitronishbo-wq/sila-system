#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="/opt/sila-system"
BACKEND_DIR="$ROOT_DIR/backend"
SCRIPTS_DIR="$ROOT_DIR/scripts"
LOGFILE="$ROOT_DIR/automate_rascunho.log"

echo "Automação rascunho - iniciando" | tee "$LOGFILE"
date --iso-8601=seconds | tee -a "$LOGFILE"

# Helper
run_cmd(){
  echo
  echo "----> $*" | tee -a "$LOGFILE"
  if ! "$@" 2>&1 | tee -a "$LOGFILE"; then
    echo "Command failed: $*" | tee -a "$LOGFILE"
    return 1
  fi
}

# 1) Fix SQLAlchemy declarative_base imports (script created earlier)
if [ -x "${SCRIPTS_DIR}/fix_sqlalchemy_declarative_imports.py" ] || [ -f "${SCRIPTS_DIR}/fix_sqlalchemy_declarative_imports.py" ]; then
  run_cmd python3 "${SCRIPTS_DIR}/fix_sqlalchemy_declarative_imports.py" --apply --root "$BACKEND_DIR"
else
  echo "Aviso: script fix_sqlalchemy_declarative_imports.py não encontrado em ${SCRIPTS_DIR}. Pulando." | tee -a "$LOGFILE"
fi

# 2) Fix Pydantic v2 Config migration (script created at repo root)
if [ -x "$ROOT_DIR/fix_pydantic_v2_config.py" ] || [ -f "$ROOT_DIR/fix_pydantic_v2_config.py" ]; then
  run_cmd python3 "$ROOT_DIR/fix_pydantic_v2_config.py" --apply "$BACKEND_DIR"
else
  echo "Aviso: script fix_pydantic_v2_config.py não encontrado em ${ROOT_DIR}. Pulando." | tee -a "$LOGFILE"
fi

# 3) Ensure backend/tests/conftest.py contains PYTHONPATH injection (we modified earlier)
if [ -f "$BACKEND_DIR/tests/conftest.py" ]; then
  echo "Conftest found: $BACKEND_DIR/tests/conftest.py" | tee -a "$LOGFILE"
else
  echo "Aviso: conftest.py não encontrado em $BACKEND_DIR/tests — testes podem falhar" | tee -a "$LOGFILE"
fi

# 4) Quick import check for modules.location.models
echo
echo "----> Import check: modules.location.models" | tee -a "$LOGFILE"
python3 - <<PY | tee -a "$LOGFILE"
import sys, traceback
sys.path.insert(0, '$BACKEND_DIR')
try:
    import importlib
    m = importlib.import_module('modules.location.models')
    print('Imported modules.location.models OK')
    print('Has CommuneCreate?', hasattr(m, 'CommuneCreate'))
    print('Sample names:', [n for n in dir(m) if not n.startswith('_')][:40])
except Exception:
    traceback.print_exc()
    raise
PY

# 5) Run pytest if available
echo
if command -v pytest >/dev/null 2>&1; then
  echo "----> Running pytest -q" | tee -a "$LOGFILE"
  (cd "$BACKEND_DIR" && pytest -q) | tee -a "$LOGFILE"
else
  echo "Aviso: pytest não está instalado neste ambiente. Para rodar a suíte de testes, ative o venv e execute: \n  cd $BACKEND_DIR && pytest -q" | tee -a "$LOGFILE"
fi

echo
echo "Automação rascunho - concluída" | tee -a "$LOGFILE"
exit 0
