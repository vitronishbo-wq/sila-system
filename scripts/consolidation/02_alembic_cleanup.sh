#!/bin/bash
# 🎯 Script de Consolidação: Alembic Cleanup
# Objetivo: Remover alembic/ da raiz (manter apenas apps/backend/alembic/)
# Risco: MEDIUM - Verificar referências em venv, pytest.ini, etc
# Data: 2026-03-18

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_DIR="$REPO_ROOT/reports/alembic-backups"
ROOT_ALEMBIC="$REPO_ROOT/alembic"
BACKEND_ALEMBIC="$REPO_ROOT/apps/backend/alembic"

echo "════════════════════════════════════════════════════════════"
echo "🎯 LIMPEZA ALEMBIC: /alembic → apps/backend/alembic/"
echo "════════════════════════════════════════════════════════════"

# 1️⃣ Safety Check
echo ""
echo "1️⃣ VERIFICANDO PRÉ-REQUISITOS..."

if [ ! -d "$ROOT_ALEMBIC" ]; then
    echo "⚠️  AVISO: $ROOT_ALEMBIC já não existe (talvez já removido?)"
    exit 0
fi

if [ ! -d "$BACKEND_ALEMBIC" ]; then
    echo "❌ ERRO: $BACKEND_ALEMBIC não encontrado (é o verdadeiro)"
    exit 1
fi

# 2️⃣ Verify references
echo ""
echo "2️⃣ VERIFICANDO REFERÊNCIAS EM FICHEIROS DE CONFIGURAÇÃO..."

REFS=$(grep -r "^alembic" "$REPO_ROOT" \
    --include="*.py" --include="*.ini" --include="*.toml" --include="*.yaml" \
    --exclude-dir=.venv --exclude-dir=__pycache__ 2>/dev/null | \
    grep -v "apps/backend/alembic" | \
    grep -v "reports/alembic-backups" | wc -l)

if [ "$REFS" -gt 0 ]; then
    echo "⚠️  AVISO: Encontradas $REFS referências a alembic fora de apps/backend/"
    echo "          Verifica manualmente antes de proceder"
    echo ""
    grep -r "^alembic" "$REPO_ROOT" \
        --include="*.py" --include="*.ini" --include="*.toml" --include="*.yaml" \
        --exclude-dir=.venv --exclude-dir=__pycache__ 2>/dev/null | \
        grep -v "apps/backend/alembic" | \
        grep -v "reports/alembic-backups" || true
    echo ""
fi

# 3️⃣ Backup root alembic
echo ""
echo "3️⃣ CRIANDO BACKUP DE SEGURANÇA..."
mkdir -p "$BACKUP_DIR"

BACKUP_PATH="$BACKUP_DIR/alembic-raiz-${TIMESTAMP}"
cp -r "$ROOT_ALEMBIC" "$BACKUP_PATH"
echo "✅ Backup criado: $BACKUP_PATH"

# 4️⃣ Compare versioning info
echo ""
echo "4️⃣ COMPARANDO MIGRAÇÕES..."
ROOT_COUNT=$(ls "$ROOT_ALEMBIC/versions" 2>/dev/null | wc -l)
BACKEND_COUNT=$(ls "$BACKEND_ALEMBIC/versions" 2>/dev/null | wc -l)

echo "   Root alembic: $ROOT_COUNT migrações"
echo "   Backend alembic: $BACKEND_COUNT migrações"

if [ "$ROOT_COUNT" -gt 0 ] && [ "$BACKEND_COUNT" -eq 0 ]; then
    echo "❌ ERRO: Backend alembic está vazio! Não podemos prosseguir"
    exit 1
fi

# 5️⃣ Archive pytest.ini if references alembic
if grep -q "alembic" "$REPO_ROOT/pytest.ini" 2>/dev/null; then
    echo ""
    echo "⚠️  pytest.ini menciona alembic, atualizando..."
    sed -i.bak 's|alembic|apps/backend/alembic|g' "$REPO_ROOT/pytest.ini"
    echo "✅ pytest.ini atualizado"
fi

# 6️⃣ Remove root alembic
echo ""
echo "5️⃣ REMOVENDO /alembic DA RAIZ..."
rm -rf "$ROOT_ALEMBIC"
echo "✅ /alembic removido"

# 7️⃣ Summary
echo ""
echo "════════════════════════════════════════════════════════════"
echo "✅ LIMPEZA ALEMBIC CONCLUÍDA COM SUCESSO!"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📊 Resumo:"
echo "   • Root /alembic: REMOVIDO (obsoleto)"
echo "   • Backend /apps/backend/alembic: MANTIDO (ativo - $BACKEND_COUNT migrações)"
echo "   • Backup: $BACKUP_PATH"
echo ""
echo "🔍 Próximos passos:"
echo "   1. Testar migrações: alembic -c apps/backend/alembic/alembic.ini current"
echo "   2. Commit: git add -A && git commit -m 'chore: remove root alembic'"
echo ""
