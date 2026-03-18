#!/bin/bash
# 🎯 Script de Consolidação: Frontend Merging
# Objetivo: Absorver interfaces/frontend → apps/frontend
# Risco: LOW - interfaces/frontend é orphaned
# Data: 2026-03-18

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_DIR="$REPO_ROOT/reports/backups"
APPS_FRONTEND="$REPO_ROOT/apps/frontend"
INTERFACES_FRONTEND="$REPO_ROOT/interfaces/frontend"

echo "════════════════════════════════════════════════════════════"
echo "🎯 CONSOLIDAÇÃO FRONTEND: interfaces/ → apps/"
echo "════════════════════════════════════════════════════════════"

# 1️⃣ Safety Check
echo ""
echo "1️⃣ VERIFICANDO PRÉ-REQUISITOS..."

if [ ! -d "$APPS_FRONTEND" ]; then
    echo "❌ ERRO: $APPS_FRONTEND não encontrado"
    exit 1
fi

if [ ! -d "$INTERFACES_FRONTEND" ]; then
    echo "⚠️  AVISO: $INTERFACES_FRONTEND já não existe (talvez já consolidado?)"
    exit 0
fi

# 2️⃣ Backup
echo ""
echo "2️⃣ CRIANDO BACKUP DE SEGURANÇA..."
mkdir -p "$BACKUP_DIR"

BACKUP_PATH="$BACKUP_DIR/.frontend.backup-${TIMESTAMP}"
cp -r "$INTERFACES_FRONTEND" "$BACKUP_PATH"
echo "✅ Backup criado: $BACKUP_PATH"

# 3️⃣ Assets Merge (WebP optimization)
echo ""
echo "3️⃣ MIGRANDO ASSETS (WebP otimizado)..."

if [ -d "$INTERFACES_FRONTEND/src/assets/images" ]; then
    mkdir -p "$APPS_FRONTEND/src/assets/images"
    
    # Copy WebP files (mais otimizados)
    find "$INTERFACES_FRONTEND/src/assets/images" -name "*.webp" -exec \
        cp {} "$APPS_FRONTEND/src/assets/images/" \; 2>/dev/null || true
    
    echo "✅ Assets WebP migrados para apps/frontend"
fi

# 4️⃣ Remove interfaces/frontend
echo ""
echo "4️⃣ REMOVENDO interfaces/frontend (orphaned)..."
rm -rf "$INTERFACES_FRONTEND"
echo "✅ interfaces/frontend removido"

# 5️⃣ Summary
echo ""
echo "════════════════════════════════════════════════════════════"
echo "✅ CONSOLIDAÇÃO CONCLUÍDA COM SUCESSO!"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📊 Resumo:"
echo "   • apps/frontend: MANTIDO (ativo)"
echo "   • interfaces/frontend: REMOVIDO (orphaned)"
echo "   • Assets otimizados (WebP): MIGRADOS"
echo "   • Backup: $BACKUP_PATH"
echo ""
echo "🔍 Próximos passos:"
echo "   1. Testar: cd $REPO_ROOT/apps/frontend && npm run dev"
echo "   2. Commit: git add -A && git commit -m 'chore: consolidate frontend'"
echo ""
