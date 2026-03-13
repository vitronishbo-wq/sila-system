#!/bin/bash
# 🔐 Script helper para testes de permissões SILA System
# Facilita a execução com variáveis de ambiente corretas

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configurações padrão
POSTGRES_USER="${POSTGRES_USER:-postgres}"
POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-postgres}"
POSTGRES_HOST="${POSTGRES_HOST:-localhost}"
POSTGRES_PORT="${POSTGRES_PORT:-5432}"
POSTGRES_DB="${POSTGRES_DB:-sila_db}"
API_URL="${API_URL:-http://localhost:8000}"
FRONTEND_URL="${FRONTEND_URL:-http://localhost:3000}"

# Funções
print_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Verificar argumentos
if [ $# -eq 0 ]; then
    print_error "Falta subcomando"
    echo ""
    echo "Uso: $0 {create|test|test-verbose|cleanup|full}"
    echo ""
    echo "Subcomandos:"
    echo "  create        - Criar usuários de teste"
    echo "  test          - Executar testes de permissões"
    echo "  test-verbose  - Executar testes com detalhes"
    echo "  cleanup       - Remover e recriar usuários"
    echo "  full          - Pipeline completo (cleanup + create + test)"
    echo ""
    echo "Variáveis de ambiente:"
    echo "  DATABASE_URL      - URL PostgreSQL (ex: postgresql+asyncpg://user:pass@host:port/db)"
    echo "  POSTGRES_USER     - Usuário PostgreSQL (padrão: postgres)"
    echo "  POSTGRES_PASSWORD - Senha PostgreSQL (padrão: postgres)"
    echo "  POSTGRES_HOST     - Host PostgreSQL (padrão: localhost)"
    echo "  POSTGRES_PORT     - Porta PostgreSQL (padrão: 5432)"
    echo "  POSTGRES_DB       - Nome do banco (padrão: sila_db)"
    echo "  API_URL           - URL da API (padrão: http://localhost:8000)"
    echo "  FRONTEND_URL      - URL do frontend (padrão: http://localhost:3000)"
    echo ""
    echo "Exemplos:"
    echo "  $0 create"
    echo "  $0 cleanup"
    echo "  $0 test"
    echo "  DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/sila_db $0 full"
    exit 1
fi

# Construir DATABASE_URL se não estiver definida
if [ -z "$DATABASE_URL" ]; then
    # URL-encode de caracteres especiais
    POSTGRES_PASSWORD_ENCODED="${POSTGRES_PASSWORD//%/%25}"
    POSTGRES_PASSWORD_ENCODED="${POSTGRES_PASSWORD_ENCODED//:/%3A}"
    POSTGRES_PASSWORD_ENCODED="${POSTGRES_PASSWORD_ENCODED//@/%40}"
    
    DATABASE_URL="postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD_ENCODED}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
fi

# Verificar Python
if ! command -v python3 &> /dev/null; then
    print_error "Python3 não encontrado. Instale Python 3.12+"
    exit 1
fi

# Definir PYTHONPATH
export PYTHONPATH="$(pwd)/apps/backend"

case "$1" in
    create)
        print_header "📝 Criando usuários de teste"
        echo "Configuração:"
        echo "  Database: ${POSTGRES_DB}@${POSTGRES_HOST}:${POSTGRES_PORT}"
        echo "  User: ${POSTGRES_USER}"
        echo ""
        
        DATABASE_URL="$DATABASE_URL" python3 scripts/create_test_users.py
        
        print_success "Usuários criados com sucesso!"
        ;;

    cleanup)
        print_header "🗑️  Removendo e recriando usuários"
        echo "Configuração:"
        echo "  Database: ${POSTGRES_DB}@${POSTGRES_HOST}:${POSTGRES_PORT}"
        echo ""
        
        DATABASE_URL="$DATABASE_URL" python3 scripts/create_test_users.py --cleanup
        
        print_success "Limpeza concluída!"
        ;;

    test)
        print_header "🧪 Executando testes de permissões"
        echo "Configuração:"
        echo "  API URL: ${API_URL}"
        echo "  Frontend URL: ${FRONTEND_URL}"
        echo ""
        
        API_URL="$API_URL" FRONTEND_URL="$FRONTEND_URL" python3 scripts/test_permissions.py
        
        print_success "Testes concluídos!"
        ;;

    test-verbose)
        print_header "🧪 Executando testes com detalhes"
        echo "Configuração:"
        echo "  API URL: ${API_URL}"
        echo "  Frontend URL: ${FRONTEND_URL}"
        echo ""
        
        API_URL="$API_URL" FRONTEND_URL="$FRONTEND_URL" python3 scripts/test_permissions.py --verbose
        
        print_success "Testes com detalhes concluídos!"
        ;;

    full)
        print_header "🔄 Pipeline completo"
        echo "Etapas:"
        echo "  1. Limpeza de usuários antigos"
        echo "  2. Criação de usuários de teste"
        echo "  3. Execução de testes automatizados"
        echo ""
        
        print_info "Etapa 1/3: Limpeza..."
        DATABASE_URL="$DATABASE_URL" python3 scripts/create_test_users.py --cleanup || print_error "Erro na limpeza"
        
        print_info "Etapa 2/3: Criação..."
        DATABASE_URL="$DATABASE_URL" python3 scripts/create_test_users.py || print_error "Erro na criação"
        
        echo ""
        print_info "Etapa 3/3: Testes..."
        sleep 2  # Dar tempo para os dados serem gravados
        API_URL="$API_URL" FRONTEND_URL="$FRONTEND_URL" python3 scripts/test_permissions.py
        
        print_success "Pipeline completo concluído!"
        ;;

    *)
        print_error "Subcomando desconhecido: $1"
        echo "Use: $0 {create|test|test-verbose|cleanup|full}"
        exit 1
        ;;
esac

exit 0
