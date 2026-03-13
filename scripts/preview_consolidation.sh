#!/bin/bash

# ============================================================================
# DRY-RUN: Mostrar o que será consolidado SEM FAZER MUDANÇAS
# ============================================================================

WORKSPACE="/home/dev03wsl/sila-system"
MODULES_A="$WORKSPACE/modules"
MODULES_B="$WORKSPACE/app/modules"
MODULES_C="$WORKSPACE/apps/backend/app/modules"

echo "════════════════════════════════════════════════════════════════════"
echo "DRY-RUN: CONSOLIDAÇÃO DE MÓDULOS - PREVIEW"
echo "════════════════════════════════════════════════════════════════════"
echo ""
echo "⚠️  NENHUMA MUDANÇA SERÁ FEITA - ISTO É APENAS UM PREVIEW"
echo ""

# ============================================================================
# PARTE 1: ANÁLISE DE DUPLICAÇÃO
# ============================================================================

echo "════════════════════════════════════════════════════════════════════"
echo "1️⃣  MÓDULOS DUPLICADOS (QUE SERÃO CONSOLIDADOS)"
echo "════════════════════════════════════════════════════════════════════"

echo ""
echo "📌 IDENTITY (3 locais):"
echo "   • $MODULES_A/identity/ (tamanho: $(du -sh $MODULES_A/identity 2>/dev/null | cut -f1))"
echo "     └─ Contém: $(ls -1 $MODULES_A/identity 2>/dev/null | grep -v "\.py\|__" | tr '\n' ',' | sed 's/,$//')"
echo ""
echo "   • $MODULES_B/identity/ (tamanho: $(du -sh $MODULES_B/identity 2>/dev/null | cut -f1))"
echo "     └─ Contém: $(ls -1 $MODULES_B/identity 2>/dev/null | grep -v "\.py\|__" | tr '\n' ',' | sed 's/,$//')"
echo ""
echo "   • $MODULES_C/identity/ (tamanho: $(du -sh $MODULES_C/identity 2>/dev/null | cut -f1)) ✅ SERÁ MANTIDO"
echo "     └─ Contém: $(ls -1 $MODULES_C/identity 2>/dev/null | grep -v "\.py\|__" | tr '\n' ',' | sed 's/,$//')"
echo "     └─ Ação: Mesclar ficheiros únicos de A e B"

echo ""
echo "📌 DOCUMENTS (2 locais):"
echo "   • $MODULES_A/documents/ (tamanho: $(du -sh $MODULES_A/documents 2>/dev/null | cut -f1))"
echo "     └─ Contém: $(ls -1 $MODULES_A/documents 2>/dev/null | grep -v "\.py\|__" | tr '\n' ',' | sed 's/,$//')"
echo ""
echo "   • $MODULES_C/documents/ (tamanho: $(du -sh $MODULES_C/documents 2>/dev/null | cut -f1)) ✅ SERÁ MANTIDO"
echo "     └─ Contém: $(ls -1 $MODULES_C/documents 2>/dev/null | grep -v "\.py\|__" | tr '\n' ',' | sed 's/,$//')"
echo "     └─ Ação: Copiar schemas/ e services/ de A"

echo ""
echo "📌 PAYMENT (2 locais):"
echo "   • $MODULES_A/payment/ (tamanho: $(du -sh $MODULES_A/payment 2>/dev/null | cut -f1))"
echo "     └─ Contém: $(ls -1 $MODULES_A/payment 2>/dev/null | grep -v "\.py\|__" | tr '\n' ',' | sed 's/,$//')"
echo ""
echo "   • $MODULES_C/payment/ (tamanho: $(du -sh $MODULES_C/payment 2>/dev/null | cut -f1)) ✅ SERÁ MANTIDO"
echo "     └─ Contém: $(ls -1 $MODULES_C/payment 2>/dev/null | grep -v "\.py\|__" | tr '\n' ',' | sed 's/,$//')"
echo "     └─ Ação: Copiar models/ e services/ de A"

echo ""
echo "📌 EDUCACAO (2 locais):"
echo "   • $MODULES_B/educacao/ (tamanho: $(du -sh $MODULES_B/educacao 2>/dev/null | cut -f1))"
echo "     └─ Contém: $(ls -1 $MODULES_B/educacao 2>/dev/null | grep -v "\.py\|__" | tr '\n' ',' | sed 's/,$//')"
echo ""
echo "   • $MODULES_C/educacao/ (tamanho: $(du -sh $MODULES_C/educacao 2>/dev/null | cut -f1)) ✅ SERÁ MANTIDO"
echo "     └─ Contém: $(ls -1 $MODULES_C/educacao 2>/dev/null | grep -v "\.py\|__" | tr '\n' ',' | sed 's/,$//')"
echo "     └─ Ação: Mesclar conteúdo de core/ de B"

echo ""
echo "📌 JUSTICE (2 locais):"
echo "   • $MODULES_B/justice/ (tamanho: $(du -sh $MODULES_B/justice 2>/dev/null | cut -f1))"
echo "     └─ Contém: $(ls -1 $MODULES_B/justice 2>/dev/null | grep -v "\.py\|__" | tr '\n' ',' | sed 's/,$//')"
echo ""
echo "   • $MODULES_C/justice/ (tamanho: $(du -sh $MODULES_C/justice 2>/dev/null | cut -f1)) ✅ SERÁ MANTIDO"
echo "     └─ Contém: $(ls -1 $MODULES_C/justice 2>/dev/null | grep -v "\.py\|__" | tr '\n' ',' | sed 's/,$//')"
echo "     └─ Ação: Mesclar conteúdo de core/ de B"

echo ""
echo "📌 XROAD (2 locais):"
echo "   • $MODULES_B/xroad/ (tamanho: $(du -sh $MODULES_B/xroad 2>/dev/null | cut -f1))"
echo "     └─ Contém: $(ls -1 $MODULES_B/xroad 2>/dev/null | grep -v "\.py\|__" | tr '\n' ',' | sed 's/,$//')"
echo ""
echo "   • $MODULES_C/xroad/ (tamanho: $(du -sh $MODULES_C/xroad 2>/dev/null | cut -f1)) ✅ SERÁ MANTIDO"
echo "     └─ Contém: $(ls -1 $MODULES_C/xroad 2>/dev/null | grep -v "\.py\|__" | tr '\n' ',' | sed 's/,$//')"
echo "     └─ Ação: Verificar qual versão é superior"

# ============================================================================
# PARTE 2: MÓDULOS QUE SERÃO REMOVIDOS
# ============================================================================

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "2️⃣  DIRETÓRIOS QUE SERÃO REMOVIDOS"
echo "════════════════════════════════════════════════════════════════════"

echo ""
echo "🗑️  SERÁ REMOVIDO: $MODULES_A"
echo "   Tamanho: $(du -sh $MODULES_A 2>/dev/null | cut -f1)"
if [[ -d "$MODULES_A" ]]; then
    echo "   Ficheiros:"
    find "$MODULES_A" -type f | wc -l | xargs echo "   └─ Total de ficheiros:"
    du -sh "$MODULES_A"/* 2>/dev/null | sed 's/^/     /'
fi

echo ""
echo "🗑️  SERÁ REMOVIDO: $MODULES_B"
echo "   Tamanho: $(du -sh $MODULES_B 2>/dev/null | cut -f1)"
if [[ -d "$MODULES_B" ]]; then
    echo "   Ficheiros:"
    find "$MODULES_B" -type f | wc -l | xargs echo "   └─ Total de ficheiros:"
    du -sh "$MODULES_B"/* 2>/dev/null | sed 's/^/     /'
fi

# ============================================================================
# PARTE 3: IMPORTS QUE SERÃO ATUALIZADOS
# ============================================================================

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "3️⃣  IMPORTS QUE SERÃO ATUALIZADOS"
echo "════════════════════════════════════════════════════════════════════"

echo ""
echo "Procurando ficheiros com imports antigos..."
import_files=$(grep -r "from modules\.|from app\.modules\." "$WORKSPACE" \
    --include="*.py" 2>/dev/null | \
    grep -v ".venv" | grep -v "__pycache__" | \
    cut -d: -f1 | sort -u)

import_count=$(echo "$import_files" | wc -l)
echo "Encontrados: $import_count ficheiros"

echo ""
echo "📋 Ficheiros a atualizar:"
echo "$import_files" | head -20 | sed 's/^/   • /'

if [[ $(echo "$import_files" | wc -l) -gt 20 ]]; then
    echo "   ... e mais $((import_count - 20)) ficheiros"
fi

# Amostra de mudanças
echo ""
echo "📝 Exemplos de mudanças de import:"
echo ""
echo "   ❌ ANTES:"
echo "      from modules.identity import ..."
echo "      from app.modules.educacao import ..."
echo ""
echo "   ✅ DEPOIS:"
echo "      from apps.backend.app.modules.identity import ..."
echo "      from apps.backend.app.modules.educacao import ..."

# ============================================================================
# PARTE 4: RESUMO DE NÚMEROS
# ============================================================================

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "4️⃣  RESUMO ESTATÍSTICO"
echo "════════════════════════════════════════════════════════════════════"

echo ""
total_modules=$(ls -1 "$MODULES_C" | grep -v "\.py\|__" | wc -l)
duplicated=6  # identity, documents, payment, educacao, justice, xroad
unique_in_c=$((total_modules - duplicated))

echo "📊 MÓDULOS:"
echo "   • Módulos únicos em /apps/backend/app/modules/: $unique_in_c"
echo "   • Módulos duplicados a consolidar: $duplicated"
echo "   • Total final: $total_modules"

echo ""
total_size_a=$(du -sh "$MODULES_A" 2>/dev/null | cut -f1)
total_size_b=$(du -sh "$MODULES_B" 2>/dev/null | cut -f1)
total_size_c=$(du -sh "$MODULES_C" 2>/dev/null | cut -f1)

echo "💾 TAMANHO:"
echo "   • /modules/: $total_size_a (será removido)"
echo "   • /app/modules/: $total_size_b (será removido)"
echo "   • /apps/backend/app/modules/: $total_size_c (será expandido)"

echo ""
echo "📝 IMPORTS:"
echo "   • Ficheiros a atualizar: $import_count"

# ============================================================================
# PARTE 5: ESTRUTURA FINAL
# ============================================================================

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "5️⃣  ESTRUTURA FINAL (APÓS CONSOLIDAÇÃO)"
echo "════════════════════════════════════════════════════════════════════"

echo ""
echo "📦 LOCAL ÚNICO: /apps/backend/app/modules/"
echo ""
echo "   Módulos consolidados:"
ls -1 "$MODULES_C" | grep -v "\.py\|__" | sed 's/^/   • /'

# ============================================================================
# PARTE 6: BACKUP
# ============================================================================

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "6️⃣  BACKUP"
echo "════════════════════════════════════════════════════════════════════"

echo ""
echo "✅ O script de consolidação criará backup em:"
echo "   /tmp/sila_modules_backup/modules_<timestamp>.tar.gz"
echo ""
echo "Para restaurar manualmente:"
echo "   tar -xzf /tmp/sila_modules_backup/modules_<timestamp>.tar.gz -C /home/dev03wsl/sila-system"

# ============================================================================
# PARTE 7: PRÓXIMAS AÇÕES
# ============================================================================

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "7️⃣  PRÓXIMAS AÇÕES"
echo "════════════════════════════════════════════════════════════════════"

echo ""
echo "✅ Para executar a consolidação:"
echo ""
echo "   OPÇÃO A (Automático - RECOMENDADO):"
echo "   bash /home/dev03wsl/sila-system/scripts/consolidate_modules.sh"
echo ""
echo "   OPÇÃO B (Manual, passo-a-passo):"
echo "   Consultar: /home/dev03wsl/sila-system/CONSOLIDATION_EXECUTION_GUIDE.md"
echo ""
echo "✅ Para validar depois:"
echo "   bash /home/dev03wsl/sila-system/scripts/validate_consolidation.sh"

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "✅ FIM DO PREVIEW (DRY-RUN)"
echo "════════════════════════════════════════════════════════════════════"
echo ""
