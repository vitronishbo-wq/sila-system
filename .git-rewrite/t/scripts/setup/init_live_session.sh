#!/bin/bash

# =================================================================
# INIT LIVE SESSION - Inicialização rápida para sessão live
# Monta HD, verifica dependências e prepara ambiente
# =================================================================

# ============================================================================
# IMPORTAR BIBLIOTECAS COMUNS
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/colors.sh"
source "$SCRIPT_DIR/../lib/logging.sh"

echo -e "${CYAN}╔═══════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║    INIT LIVE SESSION - SILA SYSTEM                ║${NC}"
echo -e "${CYAN}║    Preparando ambiente para desenvolvimento       ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════╝${NC}"
echo ""

# Diretórios
HD_MOUNT="/mnt/sda2"
PROJECT_DIR="$HD_MOUNT/home/mint/Downloads/sila-system"
LOG_DIR="$HD_MOUNT/home/mint/Downloads/logs"

# 1. Verificar se HD está montado
log "Verificando montagem do HD interno..."
if mountpoint -q "$HD_MOUNT"; then
    success "HD interno já está montado em $HD_MOUNT"
else
    log "Montando HD interno..."
    if sudo mount /dev/sda2 "$HD_MOUNT" 2>/dev/null; then
        success "HD interno montado com sucesso"
    else
        error "Falha ao montar HD interno. Verifique se /dev/sda2 existe."
    fi
fi

# 2. Verificar se o projeto existe
log "Verificando projeto..."
if [ -d "$PROJECT_DIR" ]; then
    success "Projeto encontrado em $PROJECT_DIR"
else
    error "Projeto não encontrado em $PROJECT_DIR"
fi

# 3. Criar diretórios necessários
log "Criando diretórios necessários..."
mkdir -p "$LOG_DIR"
mkdir -p "$HD_MOUNT/home/mint/Downloads/backups"
success "Diretórios criados"

# 4. Verificar Git
log "Verificando Git..."
if command -v git >/dev/null 2>&1; then
    GIT_VERSION=$(git --version | cut -d' ' -f3)
    success "Git instalado (versão $GIT_VERSION)"
else
    warn "Git não está instalado"
    log "Instalando Git..."
    if sudo apt update -qq && sudo apt install -y git --no-install-recommends; then
        success "Git instalado com sucesso"
    else
        error "Falha ao instalar Git"
    fi
fi

# 5. Verificar chaves SSH
log "Verificando chaves SSH..."
if [ -f ~/.ssh/id_ed25519 ] || [ -f ~/.ssh/id_rsa ]; then
    success "Chave SSH encontrada"

    # Testar conexão GitHub
    log "Testando conexão GitHub..."
    if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
        success "Conexão GitHub: OK"
    else
        warn "Conexão GitHub: Falhou (configure sua chave SSH)"
    fi

    # Testar conexão GitLab
    log "Testando conexão GitLab..."
    if ssh -T git@gitlab.com 2>&1 | grep -q "Welcome"; then
        success "Conexão GitLab: OK"
    else
        warn "Conexão GitLab: Falhou (configure sua chave SSH)"
    fi
else
    warn "Chave SSH não encontrada"
    echo ""
    echo "Para gerar uma chave SSH, execute:"
    echo "  ssh-keygen -t ed25519 -C \"silahbo@gmail.com\""
    echo ""
    echo "Depois adicione a chave pública aos repositórios:"
    echo "  cat ~/.ssh/id_ed25519.pub"
    echo "  GitHub: https://github.com/settings/keys"
    echo "  GitLab: https://gitlab.com/-/profile/keys"
fi

# 6. Verificar e configurar Docker
log "Verificando Docker..."
if command -v docker >/dev/null 2>&1; then
    DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | tr -d ',')
    success "Docker instalado (versão $DOCKER_VERSION)"

    # Verificar se o usuário está no grupo docker
    if groups | grep -q docker; then
        success "Usuário no grupo docker"
    else
        warn "Usuário não está no grupo docker"
        log "Adicionando usuário ao grupo docker..."
        sudo usermod -aG docker $USER
        warn "Você precisará fazer logout e login novamente"
    fi

    # Executar setup completo do Docker
    log "Configurando Docker e Docker Compose..."
    if [ -f "$PROJECT_DIR/setup_docker_storage.sh" ]; then
        chmod +x "$PROJECT_DIR/setup_docker_storage.sh"
        "$PROJECT_DIR/setup_docker_storage.sh"
    else
        warn "Script setup_docker_storage.sh não encontrado"
        warn "Execute manualmente: ./setup_docker_storage.sh"
    fi
else
    warn "Docker não está instalado"
    echo ""
    echo "Para instalar Docker, execute:"
    echo "  curl -fsSL https://get.docker.com -o get-docker.sh"
    echo "  sudo sh get-docker.sh"
    echo "  sudo usermod -aG docker \$USER"
    echo ""
    echo "Depois execute: ./setup_docker_storage.sh"
fi

# 7. Verificar Docker Compose
log "Verificando Docker Compose..."
if command -v docker-compose >/dev/null 2>&1; then
    COMPOSE_VERSION=$(docker-compose --version | cut -d' ' -f3 | tr -d ',')
    success "Docker Compose instalado (versão $COMPOSE_VERSION)"
elif docker compose version >/dev/null 2>&1; then
    COMPOSE_VERSION=$(docker compose version --short)
    success "Docker Compose (plugin) instalado (versão $COMPOSE_VERSION)"
else
    warn "Docker Compose não está instalado"
fi

# 8. Mostrar resumo
echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║              RESUMO DA INICIALIZAÇÃO              ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}✓${NC} HD interno montado: $HD_MOUNT"
echo -e "${GREEN}✓${NC} Projeto localizado: $PROJECT_DIR"
echo -e "${GREEN}✓${NC} Logs em: $LOG_DIR"
echo ""

# 9. Navegar para o projeto
log "Navegando para o diretório do projeto..."
cd "$PROJECT_DIR" || error "Falha ao acessar diretório do projeto"
success "Pronto para trabalhar!"

echo ""
echo -e "${YELLOW}Próximos passos:${NC}"
echo "  1. Para fazer deploy: ./deploy_final.sh"
echo "  2. Para deploy rápido: ./quick_deploy.sh"
echo "  3. Para deploy completo: ./deploy_master.sh"
echo ""
echo -e "${GREEN}Ambiente pronto! 🚀${NC}"

# Abrir shell no diretório do projeto
exec bash
