#!/bin/bash
# 🧹 Script de Limpeza - Arquivos Obsoletos e Backups
# Executa: bash scripts/cleanup_obsolete_files.sh

set -e

echo "🧹 SILA - Limpeza de Arquivos Obsoletos"
echo "========================================"
echo ""

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

DELETED_COUNT=0
TOTAL_SIZE=0

# Função para deletar arquivo
delete_file() {
    local file="$1"
    if [ -f "$file" ]; then
        local size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo "0")
        TOTAL_SIZE=$((TOTAL_SIZE + size))
        rm -f "$file"
        echo -e "${GREEN}✅ Deletado:${NC} $file"
        DELETED_COUNT=$((DELETED_COUNT + 1))
    fi
}

echo -e "${BLUE}📍 Fase 1: Backups com data antiga (20251103_135027)${NC}"
echo ""

# Backups docker-compose antigos
delete_file "docker-compose.yml.bak.20251103_135027"
delete_file "docker-compose.dev.yml.bak.20251103_135027"
delete_file "docker-compose.migration.yml.bak.20251103_135027"
delete_file "docker-compose.test.yml.bak.20251103_135027"
delete_file "devops/docker-compose.yml.bak.20251103_135027"

# Backups de scripts antigos
delete_file "scripts/preencher_env_critico.py.bak.20251103_135027"
delete_file "scripts/preencher_env_critico_multi.py.bak.20251103_135027"
delete_file "scripts/preencher_env_critico_multi_csv.py.bak.20251103_135027"
delete_file "scripts/auto_create_admin.sh.bak.20251103_135027"

echo ""
echo -e "${BLUE}📍 Fase 2: Backups .v1.bak (Pydantic v1)${NC}"
echo ""

# Backups Pydantic v1 em scripts
delete_file "scripts/utils/update_translations.py.v1.bak"
delete_file "scripts/migrate_pydantic_v1_to_v2.py.v1.bak"
delete_file "scripts/archive/upgrade_pydantic_v2_smart.py.v1.bak"

# Backups Pydantic v1 em venv (não devem ser modificados)
echo -e "${YELLOW}⚠️  Pulando backups em venv/ (não devem ser deletados):${NC}"
echo "   • venv/lib/python3.12/site-packages/pydantic/*.bak"
echo "   • backend/venv/lib/python3.12/site-packages/pydantic/*.bak"

echo ""
echo -e "${BLUE}📍 Fase 3: Backups recentes (manter apenas o mais novo)${NC}"
echo ""

# Manter devops/docker-compose.yml.bak (mais recente)
echo -e "${GREEN}✅ Mantido:${NC} devops/docker-compose.yml.bak (backup atual)"

# Deletar backend/modules/payment/models.py.bak (já migrado)
delete_file "backend/modules/payment/models.py.bak"

echo ""
echo "========================================"
echo -e "${GREEN}✨ Limpeza Concluída!${NC}"
echo "========================================"
echo ""
echo "📊 Estatísticas:"
echo "   • Arquivos deletados: $DELETED_COUNT"
echo "   • Espaço liberado: $(numfmt --to=iec $TOTAL_SIZE 2>/dev/null || echo "$TOTAL_SIZE bytes")"
echo ""
echo "📁 Arquivos mantidos:"
echo "   • devops/docker-compose.yml.bak (backup atual)"
echo "   • venv/**/*.bak (bibliotecas do Python)"
echo ""
