#!/bin/bash

################################################################################
# SCRIPT DE MIGRAÇÃO AUTOMÁTICA - Fase 2
# Migra scripts para usar bibliotecas comuns
################################################################################

set -euo pipefail

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MIGRATED=0
FAILED=0

echo -e "${BOLD}${CYAN}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         MIGRAÇÃO AUTOMÁTICA - Fase 2 (Scripts Críticos)       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}\n"

# Lista de scripts a migrar
SCRIPTS_TO_MIGRATE=(
    "infra/nginx_automation.sh"
    "infra/nginx_monitor.sh"
    "core/sila_start.sh"
    "setup/init_live_session.sh"
    "migration/execute_auth_migration.sh"
    "migration/prepare_migration.sh"
    "infra/install_vsc_extensions.sh"
    "maintenance/cleanup_temp_files.sh"
    "infra/nginx_diagnostic.sh"
)

# Função para verificar se script já foi migrado
is_migrated() {
    local script="$1"
    if grep -q "source.*lib/logging.sh" "$script" 2>/dev/null; then
        return 0  # Já migrado
    else
        return 1  # Não migrado
    fi
}

# Função para migrar um script
migrate_script() {
    local script="$1"
    local full_path="$SCRIPTS_DIR/$script"

    if [ ! -f "$full_path" ]; then
        echo -e "${RED}❌ Ficheiro não encontrado: $script${NC}"
        ((FAILED++))
        return 1
    fi

    if is_migrated "$full_path"; then
        echo -e "${YELLOW}⏭️  Já migrado: $script${NC}"
        return 0
    fi

    echo -e "${BLUE}🔄 Migrando: $script${NC}"

    # Criar backup
    cp "$full_path" "$full_path.bak"

    # Adicionar imports no início (após shebang)
    {
        head -1 "$full_path"
        echo ""
        echo "# ============================================================================"
        echo "# IMPORTAR BIBLIOTECAS COMUNS"
        echo "# ============================================================================"
        echo ""
        echo 'SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"'
        echo 'source "$SCRIPT_DIR/../lib/colors.sh"'
        echo 'source "$SCRIPT_DIR/../lib/logging.sh"'
        echo ""
        tail -n +2 "$full_path" | grep -v "^RED=" | grep -v "^GREEN=" | grep -v "^BLUE=" | grep -v "^YELLOW=" | grep -v "^CYAN=" | grep -v "^MAGENTA=" | grep -v "^BOLD=" | grep -v "^NC=" | grep -v "^# Cores" | grep -v "^# Definições de cores" | grep -v "^log()" | grep -v "^success()" | grep -v "^error()" | grep -v "^warn()" | grep -v "^info()" | grep -v "^section()"
    } > "$full_path.tmp"

    mv "$full_path.tmp" "$full_path"

    echo -e "${GREEN}✅ Migrado com sucesso: $script${NC}"
    ((MIGRATED++))
    return 0
}

# Executar migração
echo -e "${BOLD}Iniciando migração...${NC}\n"

for script in "${SCRIPTS_TO_MIGRATE[@]}"; do
    migrate_script "$script"
done

# Resumo
echo -e "\n${BOLD}${CYAN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}Resumo da Migração:${NC}"
echo -e "  ${GREEN}✅ Migrados: $MIGRATED${NC}"
echo -e "  ${RED}❌ Falhados: $FAILED${NC}"
echo -e "${BOLD}${CYAN}════════════════════════════════════════════════════════════════${NC}\n"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 Migração concluída com sucesso!${NC}\n"
    echo -e "${BOLD}Próximos passos:${NC}"
    echo "  1. Testar scripts migrados"
    echo "  2. Remover ficheiros .bak se tudo funcionar"
    echo "  3. Iniciar Fase 3 (consolidação de scripts)"
    exit 0
else
    echo -e "${RED}⚠️  Alguns scripts falharam. Verifique os backups (.bak)${NC}\n"
    exit 1
fi
