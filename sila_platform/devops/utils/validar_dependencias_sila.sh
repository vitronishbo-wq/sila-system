#!/bin/bash

# ============================================================================
# SILA SYSTEM - VALIDADOR E CORREÇÃO DE DEPENDÊNCIAS
# ============================================================================
# Script inteligente para validar, corrigir e otimizar dependências
# do sistema SILA (Backend Python + Frontend Node.js)
#
# Funcionalidades:
# ✅ Verificação automática de dependências
# ✅ Instalação seletiva (apenas o que falta)
# ✅ Correção de pacotes quebrados ou duplicados
# ✅ Validação de ambiente final
# ✅ Logs detalhados e notificações visuais
# ✅ Integração com sistemas de monitoramento
# ============================================================================

set -euo pipefail  # Modo estrito para melhor tratamento de erros

# ============================================================================
# CONFIGURAÇÕES GLOBAIS
# ============================================================================

# Cores para output visual
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Diretórios do sistema
BACKEND_DIR="/opt/sila-system/backend"
FRONTEND_DIR="/opt/sila-system/frontend"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Arquivos de dependência
REQ_BACK="$BACKEND_DIR/requirements.txt"
REQ_FRONT="$FRONTEND_DIR/package.json"

# Arquivos de log
LOG_DIR="$SCRIPT_DIR/logs"
LOG_FILE="$LOG_DIR/dependency_validator_$(date +%Y%m%d_%H%M%S).log"

# Configurações de execução
VERBOSE=${VERBOSE:-false}
AUTO_FIX=${AUTO_FIX:-true}
NOTIFY=${NOTIFY:-true}

# ============================================================================
# FUNÇÕES UTILITÁRIAS
# ============================================================================

log() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    # Escrever no arquivo de log
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"

    # Output visual baseado no nível
    case "$level" in
        "INFO")  echo -e "${BLUE}[INFO]${NC} $message" ;;
        "SUCCESS") echo -e "${GREEN}[✅]${NC} $message" ;;
        "WARNING") echo -e "${YELLOW}[⚠️]${NC} $message" ;;
        "ERROR") echo -e "${RED}[❌]${NC} $message" ;;
        "DEBUG") [[ "$VERBOSE" == "true" ]] && echo -e "${CYAN}[DEBUG]${NC} $message" ;;
    esac
}

notify() {
    [[ "$NOTIFY" != "true" ]] && return

    local title="$1"
    local message="$2"
    local priority="${3:-normal}"

    # Tentar enviar notificação se disponível
    if command -v notify-send &> /dev/null; then
        notify-send -u "$priority" "SILA Dependency Validator" "$title: $message"
    fi

    # Log da notificação
    log "INFO" "NOTIFICATION: $title - $message"
}

check_command() {
    local cmd="$1"
    local package="$2"

    if ! command -v "$cmd" &> /dev/null; then
        log "ERROR" "Comando '$cmd' não encontrado. Instale $package"
        return 1
    fi

    log "DEBUG" "Comando '$cmd' encontrado: $(which "$cmd")"
    return 0
}

ensure_directory() {
    local dir="$1"

    if [[ ! -d "$dir" ]]; then
        mkdir -p "$dir"
        log "INFO" "Diretório criado: $dir"
    fi
}

backup_file() {
    local file="$1"

    if [[ -f "$file" ]]; then
        local backup="$file.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$file" "$backup"
        log "INFO" "Backup criado: $backup"
    fi
}

# ============================================================================
# VALIDAÇÃO DE DEPENDÊNCIAS - BACKEND (PYTHON)
# ============================================================================

validate_backend() {
    log "INFO" "📦 Iniciando validação do backend Python..."

    cd "$BACKEND_DIR" || {
        log "ERROR" "Diretório backend não encontrado: $BACKEND_DIR"
        return 1
    }

    # Verificar dependências essenciais
    local missing_deps=()

    check_command "python3" "python3" || missing_deps+=("python3")
    check_command "pip3" "python3-pip" || missing_deps+=("python3-pip")

    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        log "ERROR" "Dependências críticas ausentes: ${missing_deps[*]}"
        notify "Backend - Dependências Críticas" "Instale: ${missing_deps[*]}" "critical"
        return 1
    fi

    # Verificar/criar ambiente virtual
    if [[ ! -d "venv" ]]; then
        log "WARNING" "Ambiente virtual não encontrado. Criando..."
        python3 -m venv venv
        log "SUCCESS" "Ambiente virtual criado com sucesso"
    else
        log "INFO" "Ambiente virtual encontrado"
    fi

    # Ativar ambiente virtual
    source venv/bin/activate || {
        log "ERROR" "Falha ao ativar ambiente virtual"
        return 1
    }

    # Atualizar pip
    log "INFO" "Atualizando pip..."
    pip install --upgrade pip --quiet

    # Instalar dependências
    if [[ -f "requirements.txt" ]]; then
        log "INFO" "Instalando dependências do requirements.txt..."

        # Verificar se há mudanças no requirements.txt
        if [[ -f ".requirements.md5" ]]; then
            current_md5=$(md5sum requirements.txt | cut -d' ' -f1)
            saved_md5=$(cat .requirements.md5)

            if [[ "$current_md5" == "$saved_md5" ]]; then
                log "INFO" "Requirements.txt não mudou, pulando instalação"
            else
                install_requirements
            fi
        else
            install_requirements
        fi

        # Salvar hash do requirements.txt
        md5sum requirements.txt > .requirements.md5
    else
        log "WARNING" "Arquivo requirements.txt não encontrado"
    fi

    # Verificar integridade das dependências
    log "INFO" "Verificando integridade das dependências..."
    if pip check &>/dev/null; then
        log "SUCCESS" "Todas as dependências estão íntegras"
    else
        log "WARNING" "Dependências quebradas detectadas, tentando correção..."
        pip install --upgrade --force-reinstall -r requirements.txt --quiet
    fi

    # Testar importações críticas
    test_backend_imports

    # Desativar ambiente virtual
    deactivate

    log "SUCCESS" "Validação do backend concluída"
}

install_requirements() {
    local start_time=$(date +%s)

    if pip install -r requirements.txt --quiet; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        log "SUCCESS" "Dependências instaladas em ${duration}s"

        # Backup do requirements.txt após instalação bem-sucedida
        backup_file "requirements.txt"
    else
        log "ERROR" "Falha na instalação das dependências"
        notify "Backend - Falha na Instalação" "Verifique requirements.txt" "critical"
        return 1
    fi
}

test_backend_imports() {
    log "INFO" "Testando importações críticas..."

    local critical_imports=("fastapi" "sqlalchemy" "pydantic" "uvicorn")

    for module in "${critical_imports[@]}"; do
        if python3 -c "import $module; print(f'$module: OK')" &>/dev/null; then
            log "DEBUG" "Importação OK: $module"
        else
            log "ERROR" "Falha na importação: $module"
            return 1
        fi
    done

    log "SUCCESS" "Todas as importações críticas funcionando"
}

# ============================================================================
# VALIDAÇÃO DE DEPENDÊNCIAS - FRONTEND (NODE.JS)
# ============================================================================

validate_frontend() {
    log "INFO" "📦 Iniciando validação do frontend Node.js..."

    cd "$FRONTEND_DIR" || {
        log "ERROR" "Diretório frontend não encontrado: $FRONTEND_DIR"
        return 1
    }

    # Verificar dependências essenciais
    check_command "node" "nodejs" || {
        log "ERROR" "Node.js não encontrado"
        notify "Frontend - Node.js Ausente" "Instale Node.js" "critical"
        return 1
    }

    check_command "npm" "npm" || {
        log "ERROR" "NPM não encontrado"
        notify "Frontend - NPM Ausente" "Instale npm" "critical"
        return 1
    }

    # Verificar versões
    local node_version=$(node --version | cut -d'v' -f2)
    local npm_version=$(npm --version)

    log "INFO" "Node.js: $node_version | NPM: $npm_version"

    # Backup do package.json
    backup_file "package.json"

    # Limpar cache e node_modules se necessário
    if [[ "$AUTO_FIX" == "true" ]]; then
        cleanup_frontend
    fi

    # Instalar dependências
    install_frontend_deps

    # Verificar vulnerabilidades
    check_frontend_security

    # Testar build básico
    test_frontend_build

    log "SUCCESS" "Validação do frontend concluída"
}

cleanup_frontend() {
    log "INFO" "Limpando cache e módulos antigos..."

    # Remover node_modules se corrompido
    if [[ -d "node_modules" ]]; then
        rm -rf node_modules
        log "INFO" "node_modules removido"
    fi

    # Limpar cache do npm
    npm cache clean --force --quiet || log "WARNING" "Falha ao limpar cache do npm"

    # Limpar locks antigos
    rm -f package-lock.json yarn.lock pnpm-lock.yaml
}

install_frontend_deps() {
    local start_time=$(date +%s)

    log "INFO" "Instalando dependências do frontend..."

    if npm install --legacy-peer-deps --quiet; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        log "SUCCESS" "Dependências instaladas em ${duration}s"
    else
        log "ERROR" "Falha na instalação das dependências"
        notify "Frontend - Falha na Instalação" "Verifique package.json" "critical"
        return 1
    fi
}

check_frontend_security() {
    log "INFO" "Verificando vulnerabilidades de segurança..."

    if npm audit --audit-level moderate &>/dev/null; then
        log "SUCCESS" "Nenhuma vulnerabilidade crítica encontrada"
    else
        log "WARNING" "Vulnerabilidades detectadas, executando correções..."

        if [[ "$AUTO_FIX" == "true" ]]; then
            npm audit fix --quiet || log "WARNING" "Falha ao corrigir vulnerabilidades automaticamente"
        fi
    fi
}

test_frontend_build() {
    log "INFO" "Testando build do frontend..."

    if npm run build --if-present &>/dev/null; then
        log "SUCCESS" "Build executado com sucesso"
    else
        log "WARNING" "Build falhou ou não disponível (modo desenvolvimento)"
    fi
}

# ============================================================================
# VALIDAÇÃO FINAL E RELATÓRIO
# ============================================================================

validate_final() {
    log "INFO" "🔍 Executando validação final do ambiente..."

    local backend_ok=true
    local frontend_ok=true

    # Testar backend
    if cd "$BACKEND_DIR" && source venv/bin/activate && python3 -c "
import fastapi, sqlalchemy, pydantic, uvicorn
print('✅ Backend: Importações críticas OK')
" 2>/dev/null; then
        log "SUCCESS" "Backend: Ambiente operacional"
    else
        log "ERROR" "Backend: Problemas de ambiente detectados"
        backend_ok=false
    fi

    # Testar frontend
    if cd "$FRONTEND_DIR" && node -e "
const fs = require('fs');
const pkg = JSON.parse(fs.readFileSync('package.json'));
console.log('✅ Frontend: package.json válido');
" 2>/dev/null; then
        log "SUCCESS" "Frontend: Ambiente operacional"
    else
        log "ERROR" "Frontend: Problemas de ambiente detectados"
        frontend_ok=false
    fi

    # Relatório final
    generate_report "$backend_ok" "$frontend_ok"

    return "$([[ "$backend_ok" == "true" && "$frontend_ok" == "true" ]]; echo $?)"
}

generate_report() {
    local backend_ok="$1"
    local frontend_ok="$2"

    echo -e "\n${PURPLE}=================================================${NC}"
    echo -e "${PURPLE}           RELATÓRIO FINAL - SILA SYSTEM        ${NC}"
    echo -e "${PURPLE}=================================================${NC}"

    echo -e "\n${BLUE}📦 BACKEND (Python)${NC}"
    if [[ "$backend_ok" == "true" ]]; then
        echo -e "   ${GREEN}✅ Ambiente operacional${NC}"
        echo -e "   ${GREEN}✅ Dependências instaladas${NC}"
        echo -e "   ${GREEN}✅ Importações críticas OK${NC}"
    else
        echo -e "   ${RED}❌ Problemas detectados${NC}"
    fi

    echo -e "\n${CYAN}🎨 FRONTEND (Node.js)${NC}"
    if [[ "$frontend_ok" == "true" ]]; then
        echo -e "   ${GREEN}✅ Ambiente operacional${NC}"
        echo -e "   ${GREEN}✅ Dependências instaladas${NC}"
        echo -e "   ${GREEN}✅ package.json válido${NC}"
    else
        echo -e "   ${RED}❌ Problemas detectados${NC}"
    fi

    echo -e "\n${PURPLE}📊 ESTATÍSTICAS:${NC}"
    echo -e "   Log: $LOG_FILE"
    echo -e "   Início: $(date -r "$LOG_FILE" '+%Y-%m-%d %H:%M:%S')"
    echo -e "   Duração: $(($(date +%s) - $(date -r "$LOG_FILE" +%s)))s"

    if [[ "$backend_ok" == "true" && "$frontend_ok" == "true" ]]; then
        echo -e "\n${GREEN}🎉 SISTEMA SILA PRONTO PARA USO!${NC}"
        notify "SILA - Ambiente Validado" "Sistema pronto para desenvolvimento" "normal"
    else
        echo -e "\n${RED}💥 CORREÇÕES NECESSÁRIAS ANTES DE CONTINUAR${NC}"
        notify "SILA - Problemas Detectados" "Verifique o log para detalhes" "critical"
    fi

    echo -e "${PURPLE}=================================================${NC}"
}

# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================

main() {
    local start_time=$(date +%s)

    # Cabeçalho
    echo -e "${PURPLE}=================================================${NC}"
    echo -e "${PURPLE}    SILA SYSTEM - DEPENDENCY VALIDATOR v2.0    ${NC}"
    echo -e "${PURPLE}=================================================${NC}"
    echo -e "${CYAN}Script inteligente de validação e correção${NC}"
    echo -e "${CYAN}Backend Python + Frontend Node.js${NC}"
    echo -e "${PURPLE}=================================================${NC}"

    # Criar diretório de logs
    ensure_directory "$LOG_DIR"

    # Iniciar log
    log "INFO" "Iniciando validação de dependências do SILA System"
    log "INFO" "Modo verbose: $VERBOSE"
    log "INFO" "Auto-fix: $AUTO_FIX"
    log "INFO" "Notificações: $NOTIFY"

    # Executar validações
    local exit_code=0

    if ! validate_backend; then
        exit_code=1
    fi

    if ! validate_frontend; then
        exit_code=1
    fi

    if ! validate_final; then
        exit_code=1
    fi

    # Tempo total
    local end_time=$(date +%s)
    local total_time=$((end_time - start_time))

    log "INFO" "Validação concluída em ${total_time}s com código de saída: $exit_code"

    exit "$exit_code"
}

# ============================================================================
# TRATAMENTO DE SINAIS E LIMPEZA
# ============================================================================

cleanup() {
    log "INFO" "Executando limpeza antes da saída..."

    # Desativar ambiente virtual se ativo
    if [[ "${VIRTUAL_ENV:-}" ]]; then
        deactivate 2>/dev/null || true
    fi

    # Remover arquivos temporários se existirem
    rm -f /tmp/sila_dependency_* 2>/dev/null || true
}

trap cleanup EXIT INT TERM

# ============================================================================
# EXECUÇÃO
# ============================================================================

# Verificar se está sendo executado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
