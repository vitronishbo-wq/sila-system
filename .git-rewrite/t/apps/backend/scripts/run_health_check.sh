#!/bin/bash

# 🛡️ Script de Execução do Health Check - SILA System
# Executa verificações de saúde dos módulos com configurações otimizadas

set -e  # Para na primeira falha

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configurações padrão
DEFAULT_URL="http://127.0.0.1:8000"
DEFAULT_TIMEOUT="10"
DEFAULT_USERNAME="admin"
DEFAULT_PASSWORD="Truman1*Marcelo1*"
DEFAULT_OUTPUT="health_report.txt"
DEFAULT_FORMAT="txt"

# Função para mostrar ajuda
show_help() {
    cat << EOF
🛡️ SILA System - Health Check de Módulos

USO:
    $0 [OPÇÕES]

OPÇÕES:
    -u, --url URL          URL base da API (padrão: $DEFAULT_URL)
    -t, --timeout SECONDS  Timeout para requisições (padrão: $DEFAULT_TIMEOUT)
    --username USER        Usuário para autenticação (padrão: $DEFAULT_USERNAME)
    --password PASS        Senha para autenticação (padrão: $DEFAULT_PASSWORD)
    -o, --output FILE      Arquivo de saída do relatório (padrão: $DEFAULT_OUTPUT)
    -f, --format FORMAT    Formato do relatório: txt, json, html (padrão: $DEFAULT_FORMAT)
    -m, --modules LIST     Lista de módulos para testar (separados por vírgula)
    -v, --verbose          Modo verboso com mais detalhes
    -h, --help             Mostra esta ajuda

EXEMPLOS:
    # Execução básica
    $0

    # Testar apenas módulos específicos
    $0 --modules "auth,health,reports"

    # Gerar relatório HTML
    $0 --format html --output relatorio.html

    # Usar servidor remoto
    $0 --url http://192.168.1.100:8000 --username admin --password senha123

    # Execução com timeout maior
    $0 --timeout 30 --verbose

FORMATOS DE RELATÓRIO:
    txt     - Relatório em texto simples (padrão)
    json    - Relatório em formato JSON para integração
    html    - Relatório HTML interativo para visualização

MÓDULOS DISPONÍVEIS:
    auth, citizenship, commercial, health, reports, finance, urbanism,
    governance, education, justice, documents, notifications, monitoring, integration

EOF
}

# Função para verificar dependências
check_dependencies() {
    echo -e "${BLUE}🔍 Verificando dependências...${NC}"

    # Verifica Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 não encontrado. Instale Python 3.8+ para continuar.${NC}"
        exit 1
    fi

    # Verifica se está no diretório correto
    if [ ! -f "backend/scripts/run_health_check.py" ]; then
        echo -e "${RED}❌ Execute este script a partir da raiz do projeto SILA.${NC}"
        exit 1
    fi

    # Verifica dependências Python
    if ! python3 -c "import httpx, pytest" 2>/dev/null; then
        echo -e "${YELLOW}⚠️ Dependências Python não encontradas.${NC}"
        echo -e "${YELLOW}   Execute: pip install -r backend/requirements_test.txt${NC}"
        read -p "Deseja instalar automaticamente? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            pip install -r backend/requirements_test.txt
        else
            exit 1
        fi
    fi

    echo -e "${GREEN}✅ Dependências verificadas${NC}"
}

# Função para verificar se o servidor está rodando
check_server() {
    local url=$1
    echo -e "${BLUE}🌐 Verificando servidor em $url...${NC}"

    if curl -s --connect-timeout 5 "$url/docs" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Servidor está rodando${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️ Servidor não está respondendo em $url${NC}"
        echo -e "${YELLOW}   Certifique-se de que o servidor SILA está rodando:${NC}"
        echo -e "${YELLOW}   cd backend && python -m uvicorn app.main:app --reload${NC}"
        read -p "Continuar mesmo assim? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
        return 1
    fi
}

# Função para executar health check
run_health_check() {
    local args=()

    # Constrói argumentos
    [ "$URL" != "$DEFAULT_URL" ] && args+=(--url "$URL")
    [ "$TIMEOUT" != "$DEFAULT_TIMEOUT" ] && args+=(--timeout "$TIMEOUT")
    [ "$USERNAME" != "$DEFAULT_USERNAME" ] && args+=(--username "$USERNAME")
    [ "$PASSWORD" != "$DEFAULT_PASSWORD" ] && args+=(--password "$PASSWORD")
    [ "$OUTPUT" != "$DEFAULT_OUTPUT" ] && args+=(--output "$OUTPUT")
    [ "$FORMAT" != "$DEFAULT_FORMAT" ] && args+=(--format "$FORMAT")
    [ -n "$MODULES" ] && args+=(--modules "$MODULES")
    [ "$VERBOSE" = "true" ] && args+=(--verbose)

    echo -e "${BLUE}🚀 Executando health check...${NC}"

    # Executa o script Python
    python3 backend/scripts/run_health_check.py "${args[@]}"

    local exit_code=$?

    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}✅ Health check concluído com sucesso!${NC}"
        echo -e "${GREEN}📄 Relatório salvo em: $OUTPUT${NC}"
    else
        echo -e "${RED}❌ Health check falhou (exit code: $exit_code)${NC}"
        echo -e "${RED}   Verifique o relatório para detalhes dos problemas${NC}"
    fi

    return $exit_code
}

# Função para mostrar resumo
show_summary() {
    echo
    echo -e "${BLUE}📊 RESUMO DA EXECUÇÃO:${NC}"
    echo -e "   URL: $URL"
    echo -e "   Timeout: ${TIMEOUT}s"
    echo -e "   Usuário: $USERNAME"
    echo -e "   Formato: $FORMAT"
    echo -e "   Output: $OUTPUT"
    [ -n "$MODULES" ] && echo -e "   Módulos: $MODULES"
    [ "$VERBOSE" = "true" ] && echo -e "   Modo: Verboso"
}

# Parse dos argumentos
URL="$DEFAULT_URL"
TIMEOUT="$DEFAULT_TIMEOUT"
USERNAME="$DEFAULT_USERNAME"
PASSWORD="$DEFAULT_PASSWORD"
OUTPUT="$DEFAULT_OUTPUT"
FORMAT="$DEFAULT_FORMAT"
MODULES=""
VERBOSE="false"

while [[ $# -gt 0 ]]; do
    case $1 in
        -u|--url)
            URL="$2"
            shift 2
            ;;
        -t|--timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        --username)
            USERNAME="$2"
            shift 2
            ;;
        --password)
            PASSWORD="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT="$2"
            shift 2
            ;;
        -f|--format)
            FORMAT="$2"
            shift 2
            ;;
        -m|--modules)
            MODULES="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE="true"
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Opção desconhecida: $1${NC}"
            echo "Use --help para ver as opções disponíveis"
            exit 1
            ;;
    esac
done

# Validações
if [[ ! "$FORMAT" =~ ^(txt|json|html)$ ]]; then
    echo -e "${RED}❌ Formato inválido: $FORMAT. Use: txt, json, ou html${NC}"
    exit 1
fi

# Execução principal
main() {
    echo -e "${GREEN}🛡️ SILA System - Health Check de Módulos${NC}"
    echo "=================================================="

    show_summary

    # Verificações pré-execução
    check_dependencies
    check_server "$URL"

    echo
    echo -e "${BLUE}▶️ Iniciando execução...${NC}"

    # Executa health check
    run_health_check

    local exit_code=$?

    echo
    echo "=================================================="

    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}🎉 Execução concluída com sucesso!${NC}"

        # Sugere abrir o relatório se for HTML
        if [ "$FORMAT" = "html" ]; then
            echo -e "${BLUE}💡 Para visualizar o relatório:${NC}"
            echo -e "   open $OUTPUT"
        fi
    else
        echo -e "${RED}💥 Execução falhou!${NC}"
        echo -e "${YELLOW}   Verifique o relatório para identificar problemas${NC}"
    fi

    exit $exit_code
}

# Executa função principal
main
