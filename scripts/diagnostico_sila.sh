#!/bin/bash
{
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     RELATÓRIO DE DIAGNÓSTICO - SILA SYSTEM                    ║"
echo "║     Data: $(date '+%Y-%m-%d %H:%M:%S')                              ║"
echo "╚════════════════════════════════════════════════════════════════╝"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SETOR A: SHARED KERNEL"
echo "═══════════════════════════════════════════════════════════════"

echo ""
echo "[A.1] Arquivos vazios em core:"
find apps/backend/app/core -name '*.py' -type f -empty ! -name '__init__*' | wc -l
echo ""
echo "[A.2] TODO/FIXME em core:"
grep -r 'todo:\|fixme:' apps/backend/app/core --include='*.py' 2>/dev/null | cut -d: -f1 | sort -u | wc -l

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SETOR B: JUSTIÇA/CIDADANIA"
echo "═══════════════════════════════════════════════════════════════"

echo ""
echo "[B.1] Arquivos vazios em justice:"
find apps/backend/app/modules/justice -name '*.py' -type f -empty ! -name '__init__*' | wc -l
echo ""
echo "[B.2] Deprecated endpoints:"
find apps/backend/app/modules/justice -name '*deprecat*' -type f | wc -l
echo ""
echo "[B.3] TODO/FIXME em justice:"
grep -r 'todo:\|fixme:' apps/backend/app/modules/justice --include='*.py' 2>/dev/null | cut -d: -f1 | sort -u | wc -l

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SETOR C: SETOR ECONÔMICO"
echo "═══════════════════════════════════════════════════════════════"

echo ""
echo "[C.1] Arquivos vazios em economy:"
find apps/backend/app/modules/economy -name '*.py' -type f -empty ! -name '__init__*' | wc -l
echo ""
echo "[C.2] TODO/FIXME em economy:"
grep -r 'todo:\|fixme:' apps/backend/app/modules/economy --include='*.py' 2>/dev/null | cut -d: -f1 | sort -u | wc -l

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SETOR D: INFRAESTRUTURA"
echo "═══════════════════════════════════════════════════════════════"

echo ""
echo "[D.1] Arquivos vazios em infrastructure_sector:"
find apps/backend/app/modules/infrastructure_sector -name '*.py' -type f -empty ! -name '__init__*' | wc -l
echo ""
echo "[D.2] TODO/FIXME em infrastructure_sector:"
grep -r 'todo:\|fixme:' apps/backend/app/modules/infrastructure_sector --include='*.py' 2>/dev/null | cut -d: -f1 | sort -u | wc -l

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "DIAGNÓSTICO GERAL"
echo "═══════════════════════════════════════════════════════════════"

echo ""
echo "[TOTAL] Arquivos Python vazios (potential garbage):"
find apps/backend/app -name '*.py' -type f -empty ! -name '__init__*' | wc -l

echo ""
echo "[TOTAL] Arquivos com legacy/deprecated markers:"
grep -ri 'legacy\|deprecated' apps/backend/app --include='*.py' 2>/dev/null | cut -d: -f1 | sort -u | wc -l

echo ""
} 2>&1
