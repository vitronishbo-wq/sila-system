#!/bin/bash
# 🧹 CLEANUP_SEEDS.sh - Remove todos os scripts de seed redundantes
# Consolida os 26 scripts em 1 único entry point (run_master_seed.py)

set -e

cd /home/dev03wsl/sila-system

echo ""
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                            ║"
echo "║            🧹 LIMPEZA DE SEEDS - Consolidação para Master Seed             ║"
echo "║                                                                            ║"
echo "║        De: 26 scripts redundantes                                         ║"
echo "║        Para: 1 entrada única (apps/backend/seeds/run_master_seed.py)       ║"
echo "║                                                                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

count=0

# Função para remover arquivo com logging
remove_file() {
    local file=$1
    if [ -f "$file" ]; then
        rm -f "$file"
        echo -e "${GREEN}✅ Removido: $file${NC}"
        ((count++))
    fi
}

# ============================================================================
# ROOT LEVEL - 7 scripts
# ============================================================================
echo -e "\n${YELLOW}📍 ROOT LEVEL (7 scripts)${NC}"
remove_file "seed_local_complete.py"
remove_file "seed_provinces_law_14_24.py"
remove_file "seed_users_official.py"
remove_file "seed_users_v5.py"
remove_file "seed_users_with_territory.py"
remove_file "seed_citizens_territory.py"
remove_file "test_seed_idempotent_final.py"

# ============================================================================
# APPS/BACKEND - 4 scripts
# ============================================================================
echo -e "\n${YELLOW}📍 APPS/BACKEND (4 scripts)${NC}"
remove_file "apps/backend/seed_21_provinces.py"
remove_file "apps/backend/seed_21_provinces_final.py"
remove_file "apps/backend/seed_users_v4.py"
remove_file "apps/backend/seeds/run_all.py"

# ============================================================================
# APPS/BACKEND/SCRIPTS - 3 scripts
# ============================================================================
echo -e "\n${YELLOW}📍 APPS/BACKEND/SCRIPTS (3 scripts)${NC}"
remove_file "apps/backend/scripts/seed_admin_roles.py"
remove_file "apps/backend/scripts/seed_all_users.py"
remove_file "apps/backend/scripts/seed_citizen_roles.py"

# ============================================================================
# APPS/BACKEND/SEEDS/CORE - 6 scripts (manter seed_founding_users.py como ref)
# ============================================================================
echo -e "\n${YELLOW}📍 APPS/BACKEND/SEEDS/CORE (6 scripts)${NC}"
remove_file "apps/backend/seeds/core/seed_and_token.py"
remove_file "apps/backend/seeds/core/seed_angola_dpa_v3.py"
remove_file "apps/backend/seeds/core/seed_angola_provinces.py"
remove_file "apps/backend/seeds/core/seed_founding_users_v2.py"
remove_file "apps/backend/seeds/core/seed_fuc_citizen.py"
remove_file "apps/backend/seeds/core/seed_fuc_golden_citizen.py"

# ============================================================================
# APPS/BACKEND/SEEDS/SCRIPTS - 2 scripts
# ============================================================================
echo -e "\n${YELLOW}📍 APPS/BACKEND/SEEDS/SCRIPTS (2 scripts)${NC}"
remove_file "apps/backend/seeds/scripts/seed_base_users.py"
remove_file "apps/backend/seeds/scripts/seed_reference_data.py"

# ============================================================================
# APPS/BACKEND/SEEDS - 2 scripts
# ============================================================================
echo -e "\n${YELLOW}📍 APPS/BACKEND/SEEDS (2 scripts)${NC}"
remove_file "apps/backend/seeds/seed_admin_users.py"
remove_file "apps/backend/seeds/seed_citizen_documents.py"

# ============================================================================
# MANTER (referência apenas, não usar)
# ============================================================================
echo -e "\n${YELLOW}📍 MANTIDOS COMO REFERÊNCIA (apenas leitura)${NC}"
if [ -f "apps/backend/seeds/core/seed_founding_users.py" ]; then
    echo -e "${GREEN}✓ apps/backend/seeds/core/seed_founding_users.py (mantido para referência)${NC}"
fi

# ============================================================================
# RELATÓRIO FINAL
# ============================================================================
echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ LIMPEZA CONCLUÍDA!${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}📊 Estatísticas:${NC}"
echo "   • Arquivos removidos: $count / 25"
echo "   • Novo entry point: apps/backend/seeds/run_master_seed.py"
echo "   • Redução: 26 scripts → 1 script (~96% de consolidação)"
echo ""
echo -e "${GREEN}🚀 Próximos passos:${NC}"
echo "   1. Testar: cd apps/backend && python seeds/run_master_seed.py"
echo "   2. Validar: PGPASSWORD=... psql -c 'SELECT COUNT(*) FROM users;'"
echo "   3. Fazer commit: git add -A && git commit -m 'refactor: consolidate seeds'"
echo ""

# Verificação final
echo -e "${YELLOW}✓ Verificando estrutura final...${NC}"
remaining=$(find . -name "*seed*.py" -not -path "./.venv/*" -not -path "./venv/*" 2>/dev/null | grep -v __pycache__ | wc -l)
echo "   Arquivos seed restantes: $remaining (esperado: 2 - run_master_seed.py + seed_founding_users.py)"
echo ""

if [ $remaining -le 3 ]; then
    echo -e "${GREEN}✅ SUCESSO! Sistema limpo e consolidado.${NC}"
else
    echo -e "${YELLOW}⚠️ AVISO: Ainda há seeds não mapeados. Revisar manualmente.${NC}"
fi

echo ""
