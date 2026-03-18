#!/bin/bash
# 🔍 Script de Auditoria: Base Repository Deduplication
# Objetivo: Mapear todas as implementações de BaseRepository
# Risco: HIGH - Esta é uma operação complexa que afeta 900+ módulos
# Data: 2026-03-18

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
REPORT_DIR="$REPO_ROOT/reports/base-repository-audit"

echo "════════════════════════════════════════════════════════════"
echo "🔍 AUDITORIA: BaseRepository Deduplication"
echo "════════════════════════════════════════════════════════════"

mkdir -p "$REPORT_DIR"

# 1️⃣ Find all BaseRepository implementations
echo ""
echo "1️⃣ PROCURANDO TODAS AS IMPLEMENTAÇÕES DE BASE_REPOSITORY..."

find "$REPO_ROOT/apps/backend" -name "*base*repository*.py" \
    -not -path "*/__pycache__/*" \
    -not -path "*/.venv/*" | sort > "$REPORT_DIR/base-repositories.txt"

echo "✅ Encontrados:"
cat "$REPORT_DIR/base-repositories.txt"

# 2️⃣ Analyze each implementation
echo ""
echo "2️⃣ ANALISANDO CADA IMPLEMENTAÇÃO..."

while IFS= read -r file; do
    echo ""
    echo "├─ $file"
    echo "│  Linhas: $(wc -l < "$file")"
    echo "│  Classes:"
    grep -E "^class.*Repository" "$file" | sed 's/^/│    /' || echo "│    (nenhuma)"
    echo "│  Métodos base:"
    grep -E "def (create|read|update|delete|find)" "$file" | wc -l | xargs echo "│    Total:"
done < "$REPORT_DIR/base-repositories.txt"

# 3️⃣ Check for imports
echo ""
echo "3️⃣ MAPEANDO DEPENDÊNCIAS (quem importa o quê)..."

cat > "$REPORT_DIR/import-analysis.txt" << 'EOF'
# Import Analysis Results
EOF

for repo_file in $(cat "$REPORT_DIR/base-repositories.txt"); do
    repo_name=$(basename "$repo_file" .py)
    import_count=$(grep -r "from.*$repo_name import\|import.*$repo_name" \
        "$REPO_ROOT/apps/backend" \
        --include="*.py" \
        --exclude-dir=__pycache__ 2>/dev/null | wc -l)
    
    echo "   $repo_file: **$import_count** imports" >> "$REPORT_DIR/import-analysis.txt"
done

cat "$REPORT_DIR/import-analysis.txt"

# 4️⃣ Create consolidation plan
echo ""
echo "4️⃣ GERANDO PLANO DE CONSOLIDAÇÃO..."

cat > "$REPORT_DIR/consolidation-plan.md" << 'EOF'
# BaseRepository Consolidation Plan

## Problem Statement
Multiple implementations of BaseRepository exist across the codebase, causing:
- Inconsistent query patterns
- Difficulty updating repository contracts
- Duplication of pagination/filtering logic

## Recommended Single Source of Truth
**✅ apps/backend/app/core/database/repositories/base_repository.py**

This is the most active and well-maintained implementation.

## Consolidation Strategy

### Phase 1: Analysis (CURRENT)
- [x] Identify all BaseRepository implementations
- [x] Map import dependencies
- [ ] Run tests to ensure no hidden contracts

### Phase 2: Normalization (PLANNED)
- [ ] Define standard interface in core/database/repositories
- [ ] Create migration guide for modules
- [ ] Update imports in batches by module

### Phase 3: Deduplication (PLANNED)
- [ ] Redirect old implementations to core location
- [ ] Run full test suite
- [ ] Remove obsolete files

### Phase 4: Verification (PLANNED)
- [ ] Code review
- [ ] Performance testing
- [ ] Team validation

## Next Steps
1. Review import-analysis.txt for dependencies
2. Create batch normalization scripts per module group
3. Execute with git history preservation (interactive rebasing if needed)
EOF

cat "$REPORT_DIR/consolidation-plan.md"

# 5️⃣ Summary
echo ""
echo "════════════════════════════════════════════════════════════"
echo "✅ AUDITORIA CONCLUÍDA"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📊 Relatórios Gerados:"
echo "   • $REPORT_DIR/base-repositories.txt"
echo "   • $REPORT_DIR/import-analysis.txt"
echo "   • $REPORT_DIR/consolidation-plan.md"
echo ""
echo "⚠️  NOTA: BaseRepository consolidation é de ALTO RISCO"
echo "         Requer validação completa e testes"
echo ""
echo "🔍 Próximos passos:"
echo "   1. Revisar relatórios de importações"
echo "   2. Planejar consolidação por módulos (batch normalization)"
echo "   3. Executar com CI/CD validation"
echo ""
