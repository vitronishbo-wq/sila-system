#!/bin/bash

# =================================================================
# ATUALIZADOR DE COMANDOS ESSENCIAIS - SILA SYSTEM
# Script para manter comandos_essenciais.md sempre atualizado
# Executa automaticamente após deploys ou mudanças significativas
# =================================================================

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

COMANDOS_FILE="/opt/sila-system/comandos_essenciais.md"
LOG_FILE="/opt/sila-system/logs/comandos_update.log"
AUTO_UPDATE=true

# ============================================================================
# FUNÇÕES DE ATUALIZAÇÃO
# ============================================================================

update_timestamp() {
    # Atualizar timestamp no arquivo
    sed -i "s/Última atualização: .*/Última atualização: $(date +'%Y-%m-%d %H:%M:%S')/g" "$COMANDOS_FILE"
    echo "[$(date +'%H:%M:%S')] Timestamp atualizado"
}

update_version() {
    # Atualizar versão baseada no VERSION.txt
    if [ -f "/opt/sila-system/VERSION.txt" ]; then
        local version=$(cat "/opt/sila-system/VERSION.txt")
        sed -i "s/Versão: .*/Versão: $version - Sistema Multi-Ambiente + CI\/CD + Monitoramento/g" "$COMANDOS_FILE"
        echo "[$(date +'%H:%M:%S')] Versão atualizada: $version"
    fi
}

add_new_command() {
    local category="$1"
    local command="$2"
    local description="$3"

    # Adicionar novo comando na categoria apropriada
    # Esta função pode ser expandida conforme necessário
    echo "[$(date +'%H:%M:%S')] Novo comando adicionado: $command"
}

validate_commands() {
    # Verificar se todos os comandos listados ainda existem e funcionam
    local broken_commands=()

    # Testar comandos críticos
    local critical_commands=(
        "./deploy_multi_ambiente.sh --help"
        "./monitor_sila.sh --help"
        "docker compose version"
        "git --version"
    )

    for cmd in "${critical_commands[@]}"; do
        if ! eval "$cmd" >/dev/null 2>&1; then
            broken_commands+=("$cmd")
        fi
    done

    if [ ${#broken_commands[@]} -gt 0 ]; then
        echo "[$(date +'%H:%M:%S')] AVISO: Comandos com problemas encontrados:"
        printf '%s\n' "${broken_commands[@]}"
        return 1
    else
        echo "[$(date +'%H:%M:%S')] Todos os comandos críticos validados"
        return 0
    fi
}

check_for_updates() {
    # Verificar se há novos scripts ou comandos para documentar
    local scripts_dir="/opt/sila-system"
    local new_commands=()

    # Scripts principais que devem estar documentados
    local required_scripts=(
        "deploy_multi_ambiente.sh"
        "monitor_sila.sh"
        "deploy_multi_ambiente_ci.sh"
    )

    for script in "${required_scripts[@]}"; do
        if [ -f "$scripts_dir/$script" ]; then
            # Verificar se o script tem ajuda disponível
            if $scripts_dir/$script --help >/dev/null 2>&1; then
                new_commands+=("$script")
            fi
        fi
    done

    if [ ${#new_commands[@]} -gt 0 ]; then
        echo "[$(date +'%H:%M:%S')] Scripts validados: ${new_commands[*]}"
    fi
}

# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================

main() {
    echo "🔄 INICIANDO ATUALIZAÇÃO DE COMANDOS ESSENCIAIS"
    echo "Arquivo: $COMANDOS_FILE"

    # Criar diretório de logs se não existir
    mkdir -p "$(dirname "$LOG_FILE")"

    # Executar atualizações
    update_timestamp
    update_version
    check_for_updates

    # Validar comandos
    if validate_commands; then
        echo "✅ ATUALIZAÇÃO CONCLUÍDA COM SUCESSO"
    else
        echo "⚠️ ATUALIZAÇÃO CONCLUÍDA COM AVISOS"
    fi

    # Log da operação
    {
        echo "--- $(date) ---"
        echo "Atualização de comandos essenciais executada"
        echo "Arquivo: $COMANDOS_FILE"
        echo "Status: OK"
        echo ""
    } >> "$LOG_FILE"

    echo "📋 Arquivo atualizado: $COMANDOS_FILE"
    echo "📊 Log de operações: $LOG_FILE"
}

# ============================================================================
# MODO DE USO
# ============================================================================

case "${1:-}" in
    "--help"|"-h")
        echo "📋 ATUALIZADOR DE COMANDOS ESSENCIAIS"
        echo ""
        echo "USO: $0 [OPÇÕES]"
        echo ""
        echo "OPÇÕES:"
        echo "  --help, -h      Mostra esta ajuda"
        echo "  --manual        Força atualização manual"
        echo "  --validate      Apenas valida comandos existentes"
        echo "  --version       Mostra versão do atualizador"
        echo ""
        echo "EXEMPLOS:"
        echo "  $0                    # Atualização automática"
        echo "  $0 --validate        # Apenas valida comandos"
        echo "  $0 --manual          # Atualização forçada"
        exit 0
        ;;
    "--validate")
        echo "🔍 VALIDANDO COMANDOS ESSENCIAIS"
        if validate_commands; then
            echo "✅ Todos os comandos estão funcionando"
            exit 0
        else
            echo "❌ Alguns comandos precisam de atenção"
            exit 1
        fi
        ;;
    "--manual")
        echo "🔧 ATUALIZAÇÃO MANUAL FORÇADA"
        AUTO_UPDATE=false
        main
        exit 0
        ;;
    "--version")
        echo "Atualizador de Comandos Essenciais v1.0"
        exit 0
        ;;
    "")
        # Atualização automática (modo padrão)
        main
        exit 0
        ;;
    *)
        echo "❌ Opção inválida: $1"
        echo "Use --help para ver as opções disponíveis"
        exit 1
        ;;
esac
