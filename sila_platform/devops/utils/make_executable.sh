#!/bin/bash

# =================================================================
# MAKE EXECUTABLE - Torna todos os scripts executáveis
# Execute este script primeiro após clonar o repositório
# =================================================================

# Cores
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}Tornando scripts executáveis...${NC}"
echo ""

# Lista de scripts
SCRIPTS=(
    "deploy_final.sh"
    "deploy_master.sh"
    "quick_deploy.sh"
    "setup_git_remote.sh"
    "setup_docker_hd.sh"
    "setup_docker_storage.sh"
    "fix_admin_build.sh"
    "cleanup_old_backups.sh"
    "cleanup_temp_files.sh"
    "init_live_session.sh"
    "make_executable.sh"
)

# Tornar executáveis
for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        chmod +x "$script"
        echo -e "${GREEN}✓${NC} $script"
    else
        echo -e "  $script (não encontrado)"
    fi
done

echo ""
echo -e "${GREEN}Concluído!${NC}"
echo ""
echo "Próximos passos:"
echo "  1. ./init_live_session.sh    # Inicializar ambiente"
echo "  2. ./setup_docker_hd.sh       # Configurar Docker"
echo "  3. ./setup_git_remote.sh      # Configurar Git"
echo "  4. ./deploy_final.sh          # Fazer deploy"
echo ""

exit 0
