#!/usr/bin/env bash
# auto_create_admin.sh
#
# Este script automatiza a preparação do ambiente local e a criação de contas
# administrativas (superusers) no banco de dados local do projeto SILA.
#
# Uso:
#   ./scripts/auto_create_admin.sh           # Executa e mantém alterações
#   ./scripts/auto_create_admin.sh --revert  # Restaura .env a partir de .env.bak e tenta reverter arquivos temporários via git
#
# Pré-requisitos:
# - PostgreSQL rodando localmente (localhost:5432)
# - Virtualenv do projeto em `backend/venv` com dependências instaladas
# - Permissões para executar comandos locais (não executa sudo automaticamente)
#
# Observações:
# - O script é idempotente: não sobrescreve usuários existentes.
# - O arquivo `.env` será atualizado para apontar para localhost; um backup será criado em `.env.bak`.
# - Use `--revert` para restaurar o `.env` e tentar reverter arquivos criados/alterados via git (se o repositório estiver sob controle de versão).


set -euo pipefail

REVERT=false
FORCE=false
for arg in "$@"; do
  case "$arg" in
    --revert) REVERT=true ;;
    --force) FORCE=true ;;
    *) echo "Unknown arg: $arg" ; exit 1 ;;
  esac
done

ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
VENV_PY="$ROOT_DIR/backend/venv/bin/python"
PYTHONPATH="$ROOT_DIR/backend"
ENV_FILE="$ROOT_DIR/.env"
ENV_BAK="$ROOT_DIR/.env.bak"

echo "[auto] Root: $ROOT_DIR"

if [ ! -x "$VENV_PY" ]; then
  echo "[auto] ERROR: Python venv not found at $VENV_PY"
  echo "[auto] Please create the virtualenv and install dependencies (see backend/requirements.txt)"
  exit 1
fi

echo "[auto] Backing up .env -> .env.auto.bak"
cp -n "$ENV_FILE" "$ROOT_DIR/.env.auto.bak" || true

# Ensure .env.bak exists (we created an earlier backup in the session)
if [ ! -f "$ENV_BAK" ]; then
  cp -f "$ENV_FILE" "$ENV_BAK"
  echo "[auto] Created $ENV_BAK"
fi

set_env_var() {
  local key="$1" value="$2" file="$3"
  if grep -qE "^${key}=" "$file"; then
    sed -i"" -E "s|^${key}=.*|${key}=${value}|" "$file" 2>/dev/null || sed -i -E "s|^${key}=.*|${key}=${value}|" "$file"
  else
    echo "${key}=${value}" >> "$file"
  fi
}

echo "[auto] Updating $ENV_FILE to point DB to localhost for local run"
set_env_var "DATABASE_URL" "Truman1*Marcelo1*ql://Truman1*Marcelo1*:Truman1*Marcelo1*@localhost:5432/sila_db" "$ENV_FILE"
set_env_var "ASYNC_DATABASE_URL" "Truman1*Marcelo1*ql+asyncpg://Truman1*Marcelo1*:Truman1*Marcelo1*@localhost:5432/sila_db" "$ENV_FILE"
set_env_var "POSTGRES_HOST" "localhost" "$ENV_FILE"
set_env_var "POSTGRES_PASSWORD" "Truman1*Marcelo1*" "$ENV_FILE"
set_env_var "POSTGRES_DB" "sila_db" "$ENV_FILE"

echo "[auto] Checking PostgreSQL availability on localhost:5432"
if command -v pg_isready >/dev/null 2>&1; then
  if pg_isready -q -h localhost -p 5432; then
    echo "[auto] Postgres appears ready"
  else
    echo "[auto] Postgres not answering on localhost:5432"
    echo "[auto] Try starting it: sudo service Truman1*Marcelo1*ql start"
    echo "[auto] Will continue and attempt to run scripts; they may fail if DB unavailable."
  fi
else
  echo "[auto] pg_isready not available; skipping readiness check. If DB is not running, the scripts may fail."
fi

echo "[auto] Running create_admin_batch.py"
env PYTHONPATH="$PYTHONPATH" "$VENV_PY" "$ROOT_DIR/scripts/create_admin_batch.py" || {
  echo "[auto] create_admin_batch.py failed. See output above." ; exit 1
}

if [ "$FORCE" = true ]; then
  read -r -p "[auto] --force specified: this will DELETE existing admin users (y/N)? " confirm
  if [[ "$confirm" =~ ^[Yy]$ ]]; then
    echo "[auto] Deleting admin users..."
    # Forward FORCE_DELETE_EMAILS from environment if present
    env FORCE_DELETE_EMAILS="$FORCE_DELETE_EMAILS" PYTHONPATH="$PYTHONPATH" "$VENV_PY" "$ROOT_DIR/scripts/force_delete_users.py"
  else
    echo "[auto] Aborting due to no confirmation for --force."; exit 1
  fi
fi

echo "[auto] Running list_users.py to show users"
env PYTHONPATH="$PYTHONPATH" "$VENV_PY" "$ROOT_DIR/scripts/list_users.py" || {
  echo "[auto] list_users.py failed. See output above." ; exit 1
}

if [ "$REVERT" = true ]; then
  echo "[auto] Reverting .env from $ENV_BAK"
  cp -f "$ENV_BAK" "$ENV_FILE"
  if command -v git >/dev/null 2>&1; then
    echo "[auto] Attempting to revert generated model stubs via git checkout"
    git checkout -- backend/app/models/education_record.py backend/app/models/social_benefit.py || true
    git checkout -- backend/modules/health/models/health_record.py backend/app/db/models/__init__.py || true
    git checkout -- scripts/list_users.py || true
  else
    echo "[auto] git not found; manual cleanup may be required"
  fi
fi

echo "[auto] Done."
