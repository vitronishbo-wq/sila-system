#!/bin/bash

# =================================================================
# SILA NGINX MONITOR - Monitoramento Inteligente do Nginx
# Complemento ao script de automação principal
# =================================================================

# ============================================================================
# IMPORTAR BIBLIOTECAS COMUNS
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/colors.sh"
source "$SCRIPT_DIR/../lib/logging.sh"

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

LOG_FILE="$SCRIPT_DIR/logs/nginx_monitor_$(date +'%Y%m%d_%H%M%S').log"
CONTAINER_NAME="sila-demo-prod"
NGINX_URL="http://localhost:8080"

check_container_health() {
    log "Verificando saúde do container..."

    if docker ps --filter "name=$CONTAINER_NAME" --filter "status=running" | grep -q "$CONTAINER_NAME"; then
        success "Container Nginx está rodando"

        # Verificar se responde corretamente
        if curl -f -s "$NGINX_URL" > /dev/null; then
            success "Nginx respondendo corretamente"

            # Verificar se não está mostrando página padrão
            if ! curl -s "$NGINX_URL" | grep -q "Welcome to nginx"; then
                success "Nginx não está mostrando página padrão"
            else
                warn "Nginx ainda está mostrando página padrão!"
                return 1
            fi
        else
            warn "Nginx não está respondendo corretamente"
            return 1
        fi
    else
        warn "Container Nginx não está rodando"
        return 1
    fi

    return 0
}

check_logs() {
    log "Verificando logs do container..."

    if docker logs "$CONTAINER_NAME" 2>/dev/null | tail -20; then
        return 0
    else
        warn "Não foi possível obter logs do container"
        return 1
    fi
}

monitor_continuously() {
    echo -e "${CYAN}${BOLD}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║             MONITOR NGINX - SILA SYSTEM                 ║"
    echo "║              Monitoramento Contínuo                     ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"

    while true; do
        echo -e "\n${BOLD}=== VERIFICAÇÃO $(date +'%H:%M:%S') ===${NC}"

        if check_container_health; then
            success "Sistema saudável!"
        else
            warn "Problemas detectados! Execute o script de automação."
        fi

        echo "Próxima verificação em 30 segundos... (Ctrl+C para parar)"
        sleep 30
    done
}

show_status() {
    echo -e "${CYAN}${BOLD}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                STATUS NGINX - SILA SYSTEM               ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"

    echo -e "${BOLD}📊 Status do Container:${NC}"
    docker ps --filter "name=$CONTAINER_NAME" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

    echo -e "\n${BOLD}🏗️  Imagens Disponíveis:${NC}"
    docker images | grep nginx || echo "Nenhuma imagem nginx encontrada"

    echo -e "\n${BOLD}📁 Arquivos de Frontend:${NC}"
    if [[ -d "frontend/webapp/dist" ]]; then
        ls -la frontend/webapp/dist/
    else
        echo "Diretório frontend/webapp/dist não encontrado"
    fi

    echo -e "\n${BOLD}🌐 Teste de Acesso:${NC}"
    if curl -f -s "$NGINX_URL" > /dev/null; then
        success "Acesso bem-sucedido em $NGINX_URL"

        # Verificar se está servindo o frontend correto
        RESPONSE=$(curl -s "$NGINX_URL")
        if echo "$RESPONSE" | grep -q "Welcome to nginx"; then
            error "Ainda mostrando página padrão do Nginx!"
        else
            success "Servindo aplicação frontend corretamente"
        fi
    else
        error "Falha no acesso em $NGINX_URL"
    fi
}

# ============================================================================
# MENU PRINCIPAL
# ============================================================================

show_menu() {
    echo -e "${CYAN}${BOLD}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║              MENU - SILA NGINX MONITOR                  ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"

    echo "1) Verificar status atual"
    echo "2) Monitoramento contínuo (30s intervalos)"
    echo "3) Ver logs do container"
    echo "4) Executar automação completa"
    echo "5) Sair"
    echo ""
    echo -n "Escolha uma opção: "
}

# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================

main() {
    mkdir -p "$(dirname "$LOG_FILE")"

    case "${1:-}" in
        "status")
            show_status
            ;;
        "monitor")
            monitor_continuously
            ;;
        "logs")
            check_logs
            ;;
        "auto")
            log "Executando automação completa..."
            if [[ -f "nginx_automation.sh" ]]; then
                ./nginx_automation.sh
            else
                error "Script de automação não encontrado"
                exit 1
            fi
            ;;
        *)
            while true; do
                show_menu
                read -r choice

                case $choice in
                    1)
                        show_status
                        ;;
                    2)
                        monitor_continuously
                        ;;
                    3)
                        check_logs
                        ;;
                    4)
                        log "Executando automação completa..."
                        if [[ -f "nginx_automation.sh" ]]; then
                            ./nginx_automation.sh
                        else
                            error "Script de automação não encontrado"
                        fi
                        ;;
                    5)
                        success "Saindo..."
                        exit 0
                        ;;
                    *)
                        error "Opção inválida!"
                        ;;
                esac

                echo -e "\nPressione Enter para continuar..."
                read -r
            done
            ;;
    esac
}

main "$@"
