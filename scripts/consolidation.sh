#!/bin/bash
# 🎯 MASTER CONSOLIDATION SCRIPT - SILA SYSTEM
# The Silk Road Operation: Clean up the 90% frontend duplication
# Data: 2026-03-18

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SCRIPTS_DIR="$REPO_ROOT/scripts/consolidation"

cat << "EOF"
████████████████████████████████████████████████████████████████
██                                                              ██
██     🛣️  OPERAÇÃO ROTA DA SEDA - CONSOLIDAÇÃO CRÍTICA       ██
██     The Silent Killer: Technical Debt Resolution 2026      ██
██                                                              ██
████████████████████████████████████████████████████████████████

Objetivos:
  1️⃣  Frontend Consolidation (interfaces/ → apps/) - RISCO: LOW
  2️⃣  Alembic Cleanup (remover raiz) - RISCO: MEDIUM  
  3️⃣  Base Repository Audit (preparar para normalização) - RISCO: HIGH

════════════════════════════════════════════════════════════════

EOF

echo "Qual consolidação deseja executar?"
echo ""
echo "  [1] Frontend Merge (absorver interfaces/frontend → apps/frontend)"
echo "      Risco: LOW | Benefício: Elimina 90% duplication"
echo ""
echo "  [2] Alembic Cleanup (remover /alembic da raiz)"
echo "      Risco: MEDIUM | Benefício: Simplifica PYTHONPATH"
echo ""
echo "  [3] Base Repository Scan (mapear para consolidação)"
echo "      Risco: HIGH | Benefício: Prepara normalização"
echo ""
echo "  [4] Ver Auditoria Completa"
echo ""
echo "  [0] Sair"
echo ""
echo "════════════════════════════════════════════════════════════"
read -p "Escolha (0-4): " choice

case "$choice" in
    1)
        echo ""
        echo "▶️  Executando Frontend Merge..."
        echo ""
        "$SCRIPTS_DIR/01_frontend_merge.sh"
        ;;
    2)
        echo ""
        echo "▶️  Executando Alembic Cleanup..."
        echo ""
        "$SCRIPTS_DIR/02_alembic_cleanup.sh"
        ;;
    3)
        echo ""
        echo "▶️  Executando Base Repository Scan..."
        echo ""
        "$SCRIPTS_DIR/03_base_repository_scan.sh"
        ;;
    4)
        echo ""
        cat "$REPO_ROOT/docs/CONSOLIDATION_AUDIT.md"
        ;;
    0)
        echo "Saindo... Até logo!"
        exit 0
        ;;
    *)
        echo "❌ Opção inválida"
        exit 1
        ;;
esac

echo ""
echo "════════════════════════════════════════════════════════════"
echo "✅ Operação concluída!"
echo ""
echo "🔗 Documentação:"
echo "   • Auditoria: docs/CONSOLIDATION_AUDIT.md"
echo "   • Backups: reports/backups/"
echo ""
