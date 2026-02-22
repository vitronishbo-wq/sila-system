#!/bin/bash

# 🧹 SILA SYSTEM - EXECUTOR DO PLANO DE SANITIZAÇÃO SUSTENTÁVEL
# Data: 13 de Outubro de 2025
# Versão: 1.0

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Função para log
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

# Banner
show_banner() {
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    🧹 SILA SANITIZATION PLAN                 ║"
    echo "║              Sistema Integrado Local de Administração        ║"
    echo "║                                                              ║"
    echo "║  🎯 Fase 5: Testes de Sustentabilidade e Documentação Final  ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Verificar se estamos no diretório correto
check_environment() {
    if [ ! -f "PLANO_SANITIZACAO_SUSTENTAVEL.md" ]; then
        error "Este script deve ser executado no diretório raiz do projeto SILA"
        exit 1
    fi
    success "Ambiente verificado - Projeto SILA detectado"
}

# Fase 5: Testes de Sustentabilidade e Documentação Final
execute_phase5() {
    log "🚀 Iniciando Fase 5: Testes de Sustentabilidade e Documentação Final"

    # 5.1: Testes de Integração para Módulos Críticos
    log "📋 5.1: Implementando testes de integração para módulos críticos"
    python3 scripts/phase5_integration_tests.py

    # 5.2: Métricas de Cobertura de Testes
    log "📊 5.2: Implementando métricas de cobertura de testes"
    python3 scripts/phase5_test_coverage.py

    # 5.3: Guia de Contribuição
    log "📚 5.3: Criando guia de contribuição para desenvolvedores"
    python3 scripts/phase5_contribution_guide.py

    # 5.4: Diagrama Arquitetônico
    log "🏗️ 5.4: Gerando diagrama arquitetônico do sistema SILA"
    python3 scripts/phase5_architecture_diagram.py

    # 5.5: Documentação Técnica Final
    log "📖 5.5: Finalizando documentação técnica para novos times"
    python3 scripts/phase5_technical_docs.py

    # 5.6: Validação Final
    log "✅ 5.6: Executando validação final do sistema"
    python3 scripts/phase5_final_validation.py

    success "Fase 5 concluída com sucesso!"
}

# Executar fase específica
execute_phase() {
    local phase=$1

    case $phase in
        0)
            log "⚡ Executando Fase 0: Saneamento Arquitetônico Crítico"
            bash scripts/phase0_architectural_fix.sh
            ;;
        1)
            log "🔴 Executando Fase 1: Módulos Críticos"
            python3 scripts/phase1_critical_modules.py
            ;;
        2)
            log "🟡 Executando Fase 2: Módulos Importantes"
            python3 scripts/phase2_important_modules.py
            ;;
        3)
            log "🟢 Executando Fase 3: Módulos Secundários"
            python3 scripts/phase3_secondary_modules.py
            ;;
        4)
            log "🔵 Executando Fase 4: Módulos de Nicho"
            python3 scripts/phase4_niche_modules.py
            ;;
        5)
            execute_phase5
            ;;
        *)
            error "Fase $phase não reconhecida. Fases disponíveis: 0, 1, 2, 3, 4, 5"
            exit 1
            ;;
    esac
}

# Função principal
main() {
    show_banner
    check_environment

    # Verificar argumentos
    if [ $# -eq 0 ]; then
        info "Executando todas as fases do plano de sanitização..."
        for phase in 0 1 2 3 4 5; do
            execute_phase $phase
        done
    else
        # Processar argumentos
        while [[ $# -gt 0 ]]; do
            case $1 in
                --phase=*)
                    phase="${1#*=}"
                    execute_phase $phase
                    shift
                    ;;
                --help|-h)
                    echo "Uso: $0 [--phase=N]"
                    echo "Fases disponíveis:"
                    echo "  0 - Saneamento Arquitetônico Crítico"
                    echo "  1 - Módulos Críticos"
                    echo "  2 - Módulos Importantes"
                    echo "  3 - Módulos Secundários"
                    echo "  4 - Módulos de Nicho"
                    echo "  5 - Testes de Sustentabilidade e Documentação Final"
                    exit 0
                    ;;
                *)
                    error "Argumento desconhecido: $1"
                    exit 1
                    ;;
            esac
        done
    fi

    success "🎉 Plano de Sanitização executado com sucesso!"
    info "📊 Para verificar o progresso, execute: ./scripts/check_progress.sh"
}

# Executar função principal
main "$@"
